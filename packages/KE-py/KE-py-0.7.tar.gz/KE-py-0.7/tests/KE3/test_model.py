from __future__ import with_statement, print_function
import os
import unittest
from datetime import datetime
from KE import KE3
from KE import KE
from KE.client import KE3CONF as CONF


class ModelV3TestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)

    def test_model_properties(self):
        models = self._client.models(name='kylin_sales_model')
        model = models[0]
        print(model.partition_desc)
        self.assertIsInstance(model.computed_columns, list)

    def test_models_list(self):
        models = self._client.models()
        self.assertIsInstance(models, list)

