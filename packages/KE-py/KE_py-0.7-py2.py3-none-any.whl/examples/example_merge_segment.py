# coding=u8
from KE import KE
from datetime import datetime, timedelta
import calendar
from KE.client import KE3CONF as CONF

client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=4)

"""
对某个project的某个cube进行定时构建。每个月5号将上个月所有的segment合并
"""

# 获取当前日期
today = datetime.today().date()
# convert date to datetime
today = datetime.fromordinal(today.toordinal())

# 获取KE 的某个cube对象
cube1 = client.cubes(name='kylin_sales_cube')[0]


def merge_week_by_month(cube, year, month):
    """
    根据某月按周合并segment，如果出现夸月的segment则放弃合并
    :param cube:
    :param year:
    :param month:
    :return:
    """

    week_start_end_list = []

    # 构造某个月的start 日期
    start = datetime(year, month, 1, 0, 0)

    # 获取第一个星期一
    if start.weekday() != 0:
        start = start + timedelta(days=(7 - start.weekday()))

    for i in range(4):
        # end of a week
        end = start + timedelta(days=7)
        if end.month != month:
            # 已夸月
            break
        start_end = (start, end)
        week_start_end_list.append(start_end)

        start = end

    # 开始合并操作
    for start, end in week_start_end_list:
        # 获取segments对象
        segments = cube.segments(start_time=start, end_time=end, size=1000)

        # 检查下segments的个数
        seg_list = segments.list_segments()
        print('segment numbers %s' % len(seg_list))

        if len(seg_list) < 7:
            print('不够7个segment')
            continue

        # 合并segments; 返回一个job对象
        job = segments.merge(force=True)

        # 查看job进度
        job.refresh(inplace=True).progress


def merge_last_week(cube, ymd):
    """合并某天的上个星期的segments

    :param cube:
    :param ymd: 日期，比如 20200501
    :return:
    """
    ymd = datetime.strptime(ymd, '%Y%m%d')
    print(ymd)

    # 构造自然周的start 日期， 星期一
    start = ymd + timedelta(days=-ymd.weekday(), weeks=-1)

    # 构造自然周的start 日期， 星期日
    end = start + timedelta(days=7)

    # 处理时区问题
    start = start + timedelta(hours=8)
    end = end + timedelta(hours=8)

    # start 要加一分钟 过滤出上个月的segment。（KE API问题）
    start = start + timedelta(minutes=1)

    print(start)
    print(end)
    # 获取segments对象
    segments = cube.segments(start_time=start, end_time=end, size=1000)

    # 检查下segments的个数
    seg_list = segments.list_segments()
    print('segment numbers %s' % len(seg_list))

    if len(seg_list) <= 1:
        print('Note! segment number should be more than 1')
        return

    # 合并segments; 返回一个job对象
    job = segments.merge(force=True)

    # 查看job进度
    job.refresh(inplace=True).progress
    return job


def merge_month(cube, year, month):
    """合并某个月的segments

    :param cube: Cube object
    :param year:  2020
    :param month: 3
    :return:
    """

    # 构造某个月的start 日期
    start = datetime(year, month, 1, 0, 0)

    # 构造某个月的最后一天 end
    end = start.replace(day=calendar.monthrange(year, month)[1])

    # 处理时区问题
    start = start + timedelta(hours=8)
    end = end + timedelta(hours=8)

    # start 要加一分钟 过滤出上个月的segment。（KE API问题）
    start = start + timedelta(minutes=1)

    print(start)
    print(end)
    # 获取segments对象
    segments = cube.segments(start_time=start, end_time=end, size=1000)

    # 检查下segments的个数
    seg_list = segments.list_segments()
    print('segment numbers %s' % len(seg_list))

    if len(seg_list) <= 1:
        print('Note! segment number should be more than 1')
        return

    # 合并segments; 返回一个job对象
    job = segments.merge(force=True)

    # 查看job进度
    job.refresh(inplace=True).progress
    return job


# 每个月5号merge上个月的segments
if today.day == 5:
    day_last_month = today - timedelta(days=30)
    merge_month(cube1, day_last_month.year, day_last_month.month)
