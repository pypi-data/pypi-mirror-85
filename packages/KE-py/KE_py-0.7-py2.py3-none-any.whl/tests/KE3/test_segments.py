# coding=u8
import unittest
from datetime import datetime
from KE import KE
from KE.v3.segment import Segment
from KE.client import KE3CONF as CONF


class SegmentsTestCase(unittest.TestCase):
    """

    """

    @classmethod
    def setUpClass(cls):
        cls._client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)
        cls._cube = cls._client.cubes('kylin_sales_cube')[0]
        cls._segments = cls._cube.segments()

    def test_segments_properties(self):
        self._segments

    def test_from_json(self):
        segments = self._segments
        print(self._cube)
        print(segments.client)
        print(segments.segment_count)

    def test_merge(self):
        segments = self._segments
        print(segments.cube_name)
        self._segments.merge(force=False)
        #self._segments.merge(force=True)

    def test_refresh(self):
        segments = self._segments
        segments.refresh()

    def test_drop(self):
        cube = self._client.cubes('kylin_sales_cube1_clone')[0]
        segments = cube.segments()
        print(segments)
        segments.drop()

    def test_list_segments(self):
        print(self._segments.size)
        seg_list = self._segments.list_segments()
        print(seg_list)
        # self.assertNotIsInstance(seg_list[0], Segment)



