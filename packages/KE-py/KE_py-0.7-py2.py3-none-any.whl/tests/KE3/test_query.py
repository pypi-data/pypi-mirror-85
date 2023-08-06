from __future__ import with_statement
import os
import unittest
from datetime import datetime
from KE import KE3, KE4, KE
import pandas as pd
from KE.client import KE3CONF as CONF


class QueryTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)

    def test_query1(self):
        res = self._client.query(sql='select count(1) from kylin_sales group by PART_DT;', project='learn_kylin')
        print(res.df)
