import argparse, sys, os
from loguru import logger as logu
import time

dtstr = time.strftime("%Y-%m-%d", time.localtime())
lvlist = ['INFO', 'DEBUG', 'ERROR']

def init(p_name,p_path):

    for lv in lvlist:
        filename = p_name + "_" + dtstr + "_" + lv + ".log"
        file_path = p_path +  filename
        fmt = "{time:YYYY-MM-DD-HH:mm:ss}  |  {level}  |  {message}"
        logu.add(file_path, level=lv, format=fmt)


def logger(message,level):
    if level == 'INFO':
        logu.info(message)
    elif level == 'DEBUG':
        logu.debug(message)
    elif level == 'ERROR':
        logu.error(message)
    else:
        logu.info(message)
