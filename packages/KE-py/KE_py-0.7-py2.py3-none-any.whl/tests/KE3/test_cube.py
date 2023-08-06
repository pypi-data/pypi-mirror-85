from __future__ import with_statement, print_function
import os
import unittest
from datetime import datetime
from KE import KE3
from KE import KE
from KE.v3 import Cube
from KE.client import KE3CONF as CONF


class CubeTestCase(unittest.TestCase):
    """

    """

    def setUp(self):
        self._client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)

    def test_cube_properties(self):
        cubes = self._client.cubes(name='kylin_sales_cube')
        cube = cubes[0]
        print(cube)
        print(cube.segment_count)
        print(cube.create_time_dt)

    def test_cube_segments(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        segments = cube.segments(start_time=datetime(2013, 1, 2, 8, 0, 0), end_time=datetime(2013, 1, 8, 8, 0, 0))
        print(segments)
        print(segments.list_segments())

    def test_build_with_ts(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        job1 = cube.build(start_time=1589040000000, end_time=1589126400000)
        name1 = 'BUILD CUBE - kylin_sales_cube - 20200509160000_20200510160000 - GMT+08:00 2020-05-18 20:06:20'
        self.assertEqual(job1.name, name1)
        job1.cancel()
        job2 = cube.build(start_time='1589040000000', end_time='1589126400000')
        name2 = 'BUILD CUBE - kylin_sales_cube - 20200509160000_20200510160000 - GMT+08:00 2020-05-18 20:02:06'
        self.assertEqual(job2.name, name2)
        job2.cancel()

    def test_build_with_datetime(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        # job = cube.build(start_time=datetime(2013, 1, 1, 8, 0, 0), end_time=datetime(2013, 1, 8, 8, 0, 0))
        # job = cube.build(start_time=datetime(2013, 1, 23, 8, 0, 0), end_time=datetime(2013, 1, 30, 8, 0, 0))
        job = cube.build(start_time=datetime(2013, 2, 21, 8, 0, 0), end_time=datetime(2013, 2, 22, 8, 0, 0))
        print(job)

    def test_clone_cube(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        new_cube = cube.clone()
        self.assertEqual(new_cube.name, 'kylin_sales_cube_clone')

    def test_disable_enable_cube(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        disabled_cube = cube.disable()
        enabled_cube = disabled_cube.enable()
        print(enabled_cube)

    def test_purge_cube(self):
        cube = self._client.cubes(name='kylin_sales_cube')[0]
        if cube.status == 'READY':
            cube = cube.disable()
        print(cube.purge())
