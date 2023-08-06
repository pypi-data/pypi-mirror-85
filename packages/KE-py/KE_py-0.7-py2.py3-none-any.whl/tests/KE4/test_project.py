from __future__ import with_statement, print_function
import os
import unittest
from datetime import datetime
from KE import KE, KE3, KE4
from KE.client import KE4CONF


class ProjectV4TestCase(unittest.TestCase):

    def setUp(self):
        self._client = KE(KE4CONF['host'], port=KE4CONF['port'], username=KE4CONF['username'], password=KE4CONF['password'], version=4, debug=True)

    def test_project_properties(self):
        project = self._client.projects(name='learn_kylin')[0]
        self.assertEqual(project.name, 'learn_kylin')

    def test_project_jobs(self):
        project = self._client.projects(name='learn_kylin')[0]
        jobs = project.jobs()
        print(jobs)

        jobs_last_week = project.jobs(time_filter=1)
        print(jobs_last_week)

        jobs_today = project.jobs(time_filter=0)
        print(jobs_today)

    def test_project_models(self):
        project = self._client.projects(name='learn_kylin')[0]
        models = project.models()
        self.assertIn('kylin_sales_cube', [m.name for m in models])

    def test_export_models(self):
        project = self._client.projects(name='SSB')[0]
        print(project)
        project.export_models('testtest')

    def test_import_models(self):
        project = self._client.projects(name='SSB')[0]
        print(project)
        project.import_models('testtest', dest_path=r"/Users/xifeng.li/PycharmProjects/KE-py/tests/KE4/SSB_['testtest'].zip")

    def test_upload_and_check_model_metadata(self):
        project = self._client.projects(name='SSB')[0]
        print(project)
        res = project.upload_and_check_model_metadata(file_path=r"/Users/xifeng.li/PycharmProjects/KE-py/tests/KE4/SSB_['testtest'].zip")
        print(res)

    def test_delete_project(self):
        project = self._client.projects(name='test1')[0]
        project.delete()

