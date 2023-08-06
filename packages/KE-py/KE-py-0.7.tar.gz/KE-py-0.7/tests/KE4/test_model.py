from __future__ import with_statement, print_function
import os
import unittest
from datetime import datetime
from KE import KE
from KE.client import KE4CONF


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self._client = KE(KE4CONF['host'], port=KE4CONF['port'], username=KE4CONF['username'], password=KE4CONF['password'], version=4, debug=True)

    def test_model_properties(self):
        model = self._client.models(name='kylin_sales_cube', project='learn_kylin')
        print(model)

    def test_models_list(self):
        models = self._client.models(project='learn_kylin')
        print(models)
        self.assertIsInstance(models, list)

        models = self._client.models(project='learn_kylin', name='kylin_sales_cube')
        self.assertIsInstance(models, list)

    def test_model_segments(self):
        models = self._client.models(project='learn_kylin', name='kylin_sales_cube')
        model = models[0]
        segments = model.segments()
        print(segments)

    def test_model_build_segments(self):
        model = self._client.models(project='learn_kylin', name='model1')[0]
        start = datetime(2020, 5, 2, 8)
        end = datetime(2020, 5, 3, 8)
        jobs = model.build(start_time=start, end_time=end)
        print(jobs)

    def test_model_sql(self):
        model = self._client.models(name='kylin_sales_cube', project='learn_kylin')[0]
        sql = model.get_sql()
        print(sql)
