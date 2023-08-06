#!/usr/bin/env python3

"""spyhook - simple python (gitlab) webhook receiver"""

# stdlib
import argparse
import configparser
import logging
import re
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import uuid
from fnmatch import fnmatch
from functools import partial

# 3rd-party
from aiohttp import web

# spyhook
from spyhook.log import RequestLoggerAdapter
from spyhook.version import __version__


async def receive_hook(request):
    """retrieve webhook request

    receive, authenticate and validate webhook http request
    """
    request_id = str(uuid.uuid4())[:13]
    log = RequestLoggerAdapter.get_logger(request_id)
    protocol = f'HTTP/{request.version.major}.{request.version.minor}'
    log.info(f'received request "{protocol} {request.method} {request.path} from {request.remote}')
    token = request.headers.get('X-Gitlab-Token')
    if token is None or token != request.app['config'].get('auth', 'secret_token'):
        log.warning(f'request authentication failed: reject request (403)')
        raise web.HTTPForbidden
    log.info(f'request authentication sucessful')
    if request.content_type != 'application/json':
        log.warning(f'no valid json content found: reject request (405)')
        raise web.HTTPBadRequest
    log.info(f'adding request to queue for async processing')
    request.app.loop.run_in_executor(None,
                                     process_hook,
                                     await request.json(),
                                     request_id,
                                     request.app['hook_config'])
    log.info(f'accept request (200)')
    return web.Response(status=200)


def process_hook(hook, request_id, hook_config):
    """process webhook request

    validate request, find appropriate hook configuration, execute hook command
    """
    log = RequestLoggerAdapter.get_logger(request_id)
    try:
        git_info = {
            'branch_name': hook['ref'].rsplit('/', 1)[1],
            'project_name': hook['project']['name'],
            'project_name_stripped': re.findall(r'(?:\w+-)?(.+)',
                                                hook['project']['name'])[0],
        }
    except (KeyError, IndexError, TypeError):
        log.error(f'could not parse request')
        return

    for section in hook_config.sections():
        if fnmatch(git_info['project_name'], section):
            command_config = dict(hook_config.items(section))
            break
    else:
        log.warning(f'no configuration matches project {git_info["project_name"]}')
        return

    with tempfile.TemporaryDirectory() as tmp_dir:
        working_directory = command_config.get('working_directory', tmp_dir)
        command = command_config['command'].format(**git_info)

        try:
            log.info(f'execute command {command}')
            process_started = time.time()
            process = subprocess.Popen(command,
                                       cwd=working_directory,
                                       shell=True,
                                       close_fds=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            process_output = process.stdout.read().decode()
            process.wait()
            process_time = time.time() - process_started
            if process.returncode != 0:
                log.warning(f'command {command} failed in {process_time:.2f} seconds:\n'
                            f'{process_output}'.rstrip('\n\t :'))
            else:
                log.info(f'command {command} succeeded in {process_time:.2f} seconds:\n'
                         f'{process_output}'.rstrip('\n\t :'))
        except (OSError, subprocess.CalledProcessError) as exception:
            log.warning(f'command execution failed: {exception}')
            return


def setup():
    """spyhook startup

    initialize logging, read and verify configuration, start event loop
    """
    parser = argparse.ArgumentParser(description='a simple gitlab webhook receiver',
                                     prog='spyhook')
    parser.add_argument('-v', '--version',
                        action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-q', '--quiet', dest='loglevel',
                        help='ouptput warnings and errors only',
                        action='store_const', const=logging.WARN,
                        default=logging.INFO)
    parser.add_argument('--config', dest='config',
                        help='spyhook main configuration file (default: %(default)s)',
                        default='/etc/spyhook/spyhook.conf')
    parser.add_argument('--hooks', dest='hooks',
                        help='spyhook hooks configuration file (default: %(default)s)',
                        default='/etc/spyhook/hooks.conf')

    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stdout,
        level=args.loglevel,
        format='%(asctime)s.%(msecs)03d %(levelname)s - %(funcName)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    log = logging.getLogger('spyhook')

    try:
        config = configparser.SafeConfigParser()
        config.read(args.config)
        hook_config = configparser.SafeConfigParser()
        hook_config.read(args.hooks)

        # verify if all mandatory configuration options are set
        for auth_option in ['secret_token']:
            _ = config['auth'][auth_option]
        for server_option in ['ssl_certificate', 'ssl_key']:
            _ = config['server'][server_option]

    except (KeyError, OSError, configparser.Error) as exception:
        log.error(f'unable to read configuration: {exception}')
        exit(1)

    try:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.load_cert_chain(config['server']['ssl_certificate'],
                                    config['server']['ssl_key'])
    except (OSError, ssl.SSLError) as exception:
        log.error(f'unable to setup ssl certificate: {exception}')
        exit(1)

    app = web.Application()
    app['log'] = log
    app['config'] = config
    app['hook_config'] = hook_config
    app.router.add_post('/', receive_hook)

    try:
        port = config['server'].getint('port', 8443)
        assert 0 < port < 65536
    except (AssertionError, ValueError) as exception:
        port = 8443
        log.warning(f'invalid port configured, falling back to {port}')

    log.info(f'starting spyhook on port {port}')

    try:
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.bind(('::', port))
        web.run_app(app,
                    print=None,
                    sock=sock,
                    ssl_context=ssl_context,
                    access_log=None)
    except (OSError, RuntimeError) as exception:
        log.error(f'unable to start spyhook: {exception}')
        exit(1)
