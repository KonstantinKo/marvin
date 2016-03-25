# -*- coding: utf-8-*-
import os

# Marvin main directory
LIB_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))

# DATA_PATH = os.path.join(APP_PATH, 'static')
# LIB_PATH = os.path.join(APP_PATH, 'client')
PLUGIN_PATH = os.path.join(LIB_PATH, 'modules')
HMM_PATH = os.path.join(LIB_PATH, os.pardir, 'hmms')

CONFIG_PATH = os.path.expanduser(os.getenv('JASPER_CONFIG', '~/.marvin'))


def config(*fname):
    return os.path.join(CONFIG_PATH, *fname)


def data(*fname):
    return os.path.join(DATA_PATH, *fname)
