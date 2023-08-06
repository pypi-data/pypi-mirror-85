# coding=u8
import unittest
from KE import KE, KE3, KE4
from KE.v3.job import Job
from KE.exceptions import ResourceUnavailable
from KE.client import KE3CONF as CONF


class ClientTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)
        print(self._client)

    def test_projects(self):
        projects = self._client.projects()
        print(projects)

    def test_fetch_json(self):
        client = KE('device2', username='admin', password='wrongpassword', version=3)
        with self.assertRaises(ResourceUnavailable):
            client.fetch_json('/projects/')

        json_obj = self._client.fetch_json('/projects/')
        self.assertIsInstance(json_obj, dict)

    def test_jobs(self):
        jobs = self._client.jobs()
        print(jobs)
        job = jobs[0]
        self.assertIsInstance(job, Job)

        project_jobs = self._client.jobs(project='learn_kylin')
        job = project_jobs[0]
        self.assertEqual(job.project_name, 'learn_kylin')

    def test_cubes(self):
        cubes = self._client.cubes(name="kylin_sales_cube")
        cube = cubes[0]
        self.assertEqual(cube.name, 'kylin_sales_cube')

        project_cubes = self._client.cubes(project='learn_kylin')
        self.assertIn(cube, project_cubes)

    def test_models(self):
        models = self._client.models(name='kylin_sales_model')
        print(models)

    def test_users(self):
        users = self._client.users()
        print(users)
