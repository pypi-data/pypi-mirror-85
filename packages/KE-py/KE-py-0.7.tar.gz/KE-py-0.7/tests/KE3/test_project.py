from __future__ import with_statement, print_function
import os
import unittest
from datetime import datetime
from KE import KE, KE3, KE4
from KE.client import KE3CONF as CONF


class ProjectV3TestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)

    def test_project_properties(self):
        project = self._client.projects(name='learn_kylin')
        self.assertIsInstance(project.tables, list)
        self.assertEqual(project.name, 'learn_kylin')

    def test_project_jobs(self):
        project = self._client.projects(name='learn_kylin')
        jobs = project.jobs()
        print(jobs)

        jobs_last_week = project.jobs(time_filter=1)
        print(jobs_last_week)

        jobs_today = project.jobs(time_filter=0)
        print(jobs_today)

    def test_project_cubes(self):
        project = self._client.projects(name='learn_kylin')
        cubes = project.cubes()
        self.assertIn('kylin_sales_cube', [c.name for c in cubes])
