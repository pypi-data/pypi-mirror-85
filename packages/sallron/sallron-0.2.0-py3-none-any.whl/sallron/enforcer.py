from sallron.util import settings, logger, discord
import time
import sys
import psutil
import logging
from subprocess import Popen
from os.path import join, dirname, exists
from os import environ

_KILL_TIMEOUT = 3
_PID_FILE = 'sallron.pid'

enforcer_logger = logging.getLogger('enforcer')

def send_message():
    """
    To be implemented.
    The idea here is:
        1. overwrite standard exception flow with custom exception_logger found in util/logger.py
        2. send message with resulting logs on every restart
        3. accompany message with deploy + customer name
    """
    if exists(_PID_FILE):
        enforcer_logger.warning("Sallron had to be restarted, take a look at the error logs...")
        try:
            errorfile = logger.get_logname(settings.LOG_DIR, 'errors')
            with open(errorfile, 'r') as errf:
                fullfile = errf.read()
                last_traceback = fullfile.split('<--->')[-2]
                formatted_traceback = f'```{last_traceback[-1800:]}```'
                discord.send_message(
                    message='Take a look at the last traceback',
                    level='warn',
                    title='Sallron had to be restarted',
                    description=formatted_traceback
                    # description = 'Hello papai'
                    )
        except:
            discord.send_message(
                message='No traceback fetched',
                level='verbose',
                title='Sallron had to be restarted',
                description='Error fetching traceback file'
                )
    else:
        discord.send_message(
                    message=f'Interface: {settings.INTERFACE_NAME}',
                    level='success',
                    title='Sallron starting up',
                    description='Seems like a clean start, no sallron.pid file found.'
                    )
    pass

def write_pid(pid):
    with open(_PID_FILE, 'w') as w:
        w.write(pid)
    enforcer_logger.info(f'pid {pid} written in {_PID_FILE}')

def kill_pid(delete_file=True):
    '''Kill processes.'''
    with open(_PID_FILE, 'r') as rapid:
        pid = rapid.read()
    if delete_file:
        Popen(f'rm {_PID_FILE}', shell=True)
        enforcer_logger.info(f'{_PID_FILE} purged')
    Popen('kill %s' % pid, shell=True)
    enforcer_logger.info(f'pid {pid} killed')

def eternal_runner(filepath, test=False):
    while True:
        try:
            send_message()
            enforcer_logger.info(f'Running {filepath} file')
            p = Popen(f"python3 {filepath}", shell=True)
            if test:
                raise KeyboardInterrupt
            p.wait()
        except (KeyboardInterrupt):
            enforcer_logger.info('Exit signal received, shutting down.')
            time.sleep(_KILL_TIMEOUT)
            kill_pid()
            sys.exit()
            print("That's all folks.")