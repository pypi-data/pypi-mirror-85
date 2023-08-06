# coding=u8
import logging
from KE import KE
import csv
import time
import queue
import configparser
from datetime import datetime, timedelta
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(10)
q = queue.Queue()
client3 = KE(host='device2', username='admin', password='Kyligence@2020', version=3, debug=True)
client = KE(host=['10.1.3.63'], port=7171, username='ADMIN', password='KYLIN', version=4, debug=True)


config = configparser.ConfigParser()

config.read('../KE/KE.ini')


print(config)

