import os
import time
import unittest
from datetime import datetime
from KE import KE
from KE.client import KE3CONF as CONF


class JobTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)

    def test_job_properties(self):
        jobs = self._client.jobs(project='learn_kylin')
        job = jobs[0]
        print(job)
        self.assertIsInstance(job.duration, int)
        self.assertIsInstance(job.progress, float)
        self.assertIsInstance(job.steps, list)

    def test_job_pause_resume(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        job = cube.build(start_time=datetime(2013, 2, 6, 8, 0, 0), end_time=datetime(2013, 2, 7, 8, 0, 0))
        print(job)
        time.sleep(5)
        job.pause()
        job.resume()

    def test_cancel_job(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        job = cube.build(start_time=datetime(2013, 2, 7, 8, 0, 0), end_time=datetime(2013, 2, 8, 8, 0, 0))
        time.sleep(5)
        new_job = job.cancel()
        print(new_job)

    def test_drop_job(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        job = cube.build(start_time=datetime(2013, 2, 7, 8, 0, 0), end_time=datetime(2013, 2, 8, 8, 0, 0))
        time.sleep(5)
        job.cancel()
        new_job = job.drop()
        print(new_job)

    def test_refresh_job(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        job = cube.build(start_time=datetime(2013, 2, 7, 8, 0, 0), end_time=datetime(2013, 2, 8, 8, 0, 0))
        time.sleep(10)
        new_job = job.refresh()
        print(new_job.process)
