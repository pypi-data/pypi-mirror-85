#!/usr/bin/env python

import logging
from logging.handlers import RotatingFileHandler
from sallron.util import settings, discord
from datetime import datetime
import traceback
import logging
import sys
import os

def get_logname(directory, name, extension="txt"):
    ''' returns logs/master_2020-10-30.txt for instance'''
    if directory.endswith('/'):
        return f"{directory}{name}_{datetime.today().strftime('%Y-%m-%d')}.{extension}"
    else:
        return f"{directory}/{name}_{datetime.today().strftime('%Y-%m-%d')}.{extension}"

def setup_logger(level = logging.INFO):
    '''Prints logger info to terminal'''
    logger = logging.getLogger()
    logger.setLevel(level)
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def setup_master_logger(logdir, maxsize, maxbackups=5, level=logging.INFO):
    rfh = logging.handlers.RotatingFileHandler(
        filename=get_logname(logdir, 'master'), 
        mode='a',
        maxBytes=maxsize,
        backupCount=maxbackups,
        encoding=None,
        delay=0
    )
    logging.basicConfig(handlers=[rfh],
                                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                                datefmt='%H:%M:%S',
                                level=level)


# Global error_logger so all functions bellow can use it
error_logger = logging.getLogger('errors')

def setup_error_logger(logdir, maxsize):
    '''Basic handler setup for error_logger'''
    log_path = get_logname(logdir, 'errors')

    global error_logger
    error_logger = logging.getLogger('errors')
    try:
        handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=maxsize, backupCount=1) # stream=sys.stdout
    except FileNotFoundError:
        os.mkdir(logdir)
        handler = logging.handlers.RotatingFileHandler(log_path, maxBytes=maxsize, backupCount=1) # stream=sys.stdout
    error_logger.addHandler(handler)

def close_error_logger():
    error_logger.removeHandler(error_logger.handlers[0])
    return

def log_exception(exc_type, exc_value, exc_traceback):
    '''Log unhandled exceptions
    set sys.excepthook = logger.log_exception on main file for it to work'''
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    message = f'{exc_type}: {exc_value}'
    trace = ''.join(traceback.format_tb(exc_traceback))
    description = f"```\n{trace}\n```"
    discord.send_message(
        message=message,
        description=description)

    error_logger.info(str(datetime.now()))
    error_logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    error_logger.info('----------------<--->------------------') # '<--->' used so latest error parsing is easier
    close_error_logger()
    return

def log_error(message):
    '''Log handled errors'''
    discord.send_message(message=message, title='Error ocurred')
    error_logger.info(str(datetime.now()))
    error_logger.error(message)
    error_logger.info('----------------<--->------------------')
    return

def setup_logbook(name, logdir, maxsize, extension='.txt', level=logging.INFO):
    """Setup logger that writes to file, supports multiple instances with no overlap.
       Available levels: DEBUG|INFO|WARN|ERROR
       !Legacy, usage not recommended."""
    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d (%(name)s) - %(message)s', datefmt='%d-%m-%y %H:%M:%S')
    date = datetime.today().strftime('%Y-%m-%d')
    log_path = str(logdir + name +'_' + date + extension)
    try:
        handler = RotatingFileHandler(log_path, maxBytes=maxsize, backupCount=1)
    except FileNotFoundError:
        os.mkdir(logdir)
        handler = RotatingFileHandler(log_path, maxBytes=maxsize, backupCount=1)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger