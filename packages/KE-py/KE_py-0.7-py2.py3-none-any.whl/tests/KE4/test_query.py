from __future__ import with_statement
import os
import unittest
from datetime import datetime
from KE import KE3, KE4, KE
import pandas as pd
from KE.client import KE4CONF


class QueryTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE(KE4CONF['host'], port=KE4CONF['port'], username=KE4CONF['username'], password=KE4CONF['password'], version=4, debug=True)

    def test_query1(self):
        query = self._client.query(sql='select PART_DT, count(1) from kylin_sales group by PART_DT;', project='learn_kylin')
        print(query.df)
        self.assertIsInstance(query.df, pd.DataFrame)
