# coding=u8
import unittest
from KE import KE, KE3, KE4
from KE.util import unify_timestamp
from datetime import date, datetime, timedelta


class UtilTestCase(unittest.TestCase):

    def test_unify_timestamp(self):
        today_d = date.today()
        tmp = unify_timestamp(today_d)
        self.assertEqual(len(tmp), 13)

        today_dt = datetime.today()
        tmp = unify_timestamp(today_dt)
        self.assertEqual(len(tmp), 13)
