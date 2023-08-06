"""This module contains utilities used by the InstaClient"""
import functools
from functools import wraps
import logging
import time
import random

def get_logger():
    """
    Creates a logging object and returns it

    Returns:
        logger:logging.Log: Log object
    """

    logger = logging.getLogger('INSTACLIENT')
    logger.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
 
    # log format
    c_handler.setFormatter(c_format)
 
    logger.addHandler(c_handler)
    return logger
 
 
def exception(func):
    """
    Exception logging decorator

    Args:
        func:function: Function to wrap

    Returns:
        wrapper:function: Wrapper function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            # log the exception
            msg = "Exception in method {}".format(func.__name__)
            logger = get_logger('debug.log')
            logger.exception(msg)
 
    return wrapper
