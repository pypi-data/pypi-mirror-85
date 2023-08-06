# coding=u8
from KE import KE
from datetime import datetime, timedelta
from KE.client import KE3CONF, KE4CONF

client = KE(KE3CONF['host'], port=KE3CONF['port'], username=KE3CONF['username'], password=KE3CONF['password'],
            version=3)

"""
定时监控Job，将失败的job重启
"""

# 过滤出失败的job
failed_jobs = client.jobs(time_filter=4, status=8)

for job in failed_jobs:
    print('restarting failed job: %s' % job.id)
    job.resume()



