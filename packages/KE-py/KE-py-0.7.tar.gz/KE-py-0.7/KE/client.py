# -*- coding: utf-8 -*-
from __future__ import with_statement, print_function, absolute_import
from KE.v3.client import KE3
from KE.v4.client import KE4
import os
import configparser
from pathlib import Path

path = Path(__file__).parents[0]

if os.path.exists(os.path.join(path, 'KE.ini')):
    path = os.path.join(path, 'KE.ini')
elif os.path.exists(os.path.join(path, 'KE.ini.example')):
    path = os.path.join(path, 'KE.ini.example')

config = configparser.ConfigParser()

config.read(path)

try:
    KE3CONF = config['KE3']
    KE4CONF = config['KE4']
except KeyError:
    KE3CONF = None
    KE4CONF = None


class KE(object):
    def __new__(cls, host='localhost', port=7070, username='ADMIN', password='KYLIN', version=3,
                debug=False, ssl=False, verify=True, *args, **kwargs):
        if version == 3:
            return KE3(host, port=port, username=username, password=password,
                       debug=debug, ssl=ssl, verify=verify, *args, **kwargs)
        elif version == 4:
            return KE4(host, port=port, username=username, password=password,
                       debug=debug, ssl=ssl, verify=verify, *args, **kwargs)

    def __repr__(self):
        return "<KE Host: {host} Version: {version}>".format(host=self.host, version=self.version)

