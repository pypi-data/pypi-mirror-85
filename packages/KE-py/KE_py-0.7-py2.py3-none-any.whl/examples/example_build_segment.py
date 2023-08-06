# coding=u8
from KE import KE
from datetime import date, datetime, timedelta
import calendar
from KE.client import KE3CONF as CONF

client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=3)

# 获取cube对象
cube1 = client.cubes(name='kylin_sales_cube')[0]


def build_a_month(cube, year, month):
    """ 在某个Cube中批量构建一个月的segment

    :param cube:
    :param year:
    :param month:
    :return:
    """
    num_days = calendar.monthrange(year, month)[1]
    days = [date(year, month, day) for day in range(1, num_days + 1)]
    days = [str(d).replace('-', '') for d in days]

    # 构造开始日期
    start = datetime(2020, 4, 1, 8, 1)

    # 构造结束日期
    end = datetime(2020, 4, 30, 8, 0)

    # 获取segments对象
    segments = cube.segments(start_time=start, end_time=end)

    # 过滤出已存在的segment
    existed_segment = []

    for s in segments.list_segments():
        segment_start = s.name.split('_')[0][:8]
        if segment_start in days:

            existed_segment.append(segment_start)

    for day in days:
        if day in existed_segment:
            print('segment 已存在')
        else:
            # 构建的开始\结束时间
            build_start = datetime.strptime(day, '%Y%m%d')
            build_end = build_start + timedelta(days=1)
            # 要加8小时
            build_start = build_start + timedelta(hours=8)
            build_end = build_end + timedelta(hours=8)

            print(build_start)
            print(build_end)

            # 构建一天的segment
            print('building segment')
            job = cube.build(start_time=build_start, end_time=build_end)
