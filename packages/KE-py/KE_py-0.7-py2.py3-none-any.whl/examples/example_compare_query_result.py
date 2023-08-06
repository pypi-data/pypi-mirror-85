# coding=u8
"""
VIVO KE3 迁移到 KE4，上线前需要拿一部分历史查询，对比查询结果准确性。

输出一个general_result.csv (可转换为excel)：
1）一致性比对结果CSV文件（项目，SQL，查询状态（3X，4X），查询对象（3X，4X），查询ID（3X，4X），响应时间（3X，4X），结果条数（3X，4X），结果是否一致，结果不一致开始坐标（行列）按列遍历

对查询不一致的SQL 输出3x 4x 各一个结果明细的CSV：
结果不一致的查询每条查询生成2个CSV文件（查询ID_3X.csv,查询ID_4X.csv)，文件中为整个查询结果。

"""

import requests
import time
import os
import sys
import csv
from threading import Thread
from concurrent import futures
from collections import OrderedDict
from KE import KE
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(100)

try:
    from itertools import zip_longest
except:
    from itertools import izip_longest as zip_longest


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


client3 = KE(host=[], port=7080, username='admin',
             password='', version=3)
# client3=KE(host='kappy-prd.vivo.lan', port=8080, username='admin', password='kappy@111', version=3)

ke4_query_nodes = ['10.193.147.131', '10.193.148.3', '10.193.148.6', '10.193.148.7']
# client4=KE(host='kappy-nt.vivo.lan', port=8080, version=4)
client4 = KE(host=ke4_query_nodes, version=4)

# projects=['ai_album','ai_atlas','ai_data_asset','ai_engine',
# 'ai_error_analysis','ai_gomoku','ai_jovi_picture','ai_jovi_screen','ai_jovi_voice','ai_keops','ai_message','ai_msearch',
# 'ai_scan','ai_smart_favorites','ai_smart_scene','ai_user_travel','ai_vivo_input','ai_vshield','ai_vtag',
# 'ai_wplock','ai_analysis_platform','ai_smartboard']

# projects=['ai_album','ai_msearch','ai_service_platform','ai_vcode_hive','ai_keops_hive','ai_persona']

projects = ['ai_analysis_platform', 'ai_smartboard', 'ai_atlas', 'ai_common_game', 'ai_data_asset', 'ai_error_analysis',
            'ai_gomoku', 'ai_jovi_picture', 'ai_jovi_screen', 'ai_jove_voice', 'ai_message', 'ai_recommend', 'ai_scan',
            'ai_smart_favorites', 'ai_smart_scene', 'ai_user_travel', 'ai_vivo_input', 'ai_vshield', 'ai_wplock']

input_file='/home/kappy/script/query_logs/202006021436.csv'
df_input = pd.read_csv(input_file, sep='|',
                       names=['dt', 'query_id', 'sql', 'success', 'duration', 'project', 'cube'])

df_input = df_input.drop_duplicates(subset=['sql'])  # 过滤重复的SQL
df_input = df_input[['query_id', 'sql', 'project']]
print(df_input.shape)


def isfloat(value):
    if value is None:
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def compare_list(list1, list2):
    """
    比较两个List的数据
    :param list1:
    :param list2:
    :return:
    """
    index = 0
    is_list_same = True
    cells = ('', '')
    for e1, e2 in zip_longest(list1, list2):
        if isfloat(e1) and isfloat(e2):
            # (u'2.56922563470936500', u'2.569225634709') 这种算一样的
            e1 = round(float(e1), 2)
            e2 = round(float(e2), 2)

        if e1 != e2:
            is_list_same = False
            #print('value difference: ', e1, e2, type(e1))
            return is_list_same, index, (e1, e2)
        index += 1

    return is_list_same, index, cells


def compare_df(query_id, df1, df2):
    """比较两边返回的DataFrame数据"""
    is_same = True
    coordinate = ('', '')
    cells = ('', '')

    for col1, col2 in zip(df1, df2):
        data1 = sorted(['' if e is None else e for e in list(df1[col1])])
        data2 = sorted(['' if e is None else e for e in list(df2[col2])])

        # 对比每一列
        is_list_same, index, cells = compare_list(data1, data2)
        if not is_list_same:
            is_same = False
            # 如果两边详情不一致则保存DataFrame为CSV
            df1.to_csv('detail_csv/%s_v3.csv' % query_id, index=False, encoding='utf-8')
            df2.to_csv('detail_csv/%s_v4.csv' % query_id, index=False, encoding='utf-8')

            coordinate = (col1, index)
            return is_same, coordinate, cells

    if df1.shape != df2.shape:
        # 0和非0对比
        is_same = False

    return is_same, coordinate, cells


keys = ['qid', 'sql', 'project', 'realization3', 'realization4', 'duration3', 'duration4', 'isException3',
        'isException4', 'storageCacheUsed3', 'storageCacheUsed4', 'exceptionMessage3', 'exceptionMessage4',
        'id3', 'id4', 'server3', 'server4',
        'pushDown3', 'pushDown4', 'timeout3', 'timeout4', 'rows3', 'rows4', 'is_same',
        'coordinate_x', 'coordinate_y',
        'cell3', 'cell4']


def query_request(client, sql, project):
    try:
        res = client.query(sql, project=project, timeout=200)
        return res
    except requests.exceptions.ReadTimeout:
        return 'timeout'


def get_general(query_id, sql, project):
    """ 获取general的对比信息 """
    items = [(key, None) for key in keys]
    result = OrderedDict(items)
    result['qid'] = query_id
    result['sql'] = sql
    result['project'] = project

    res3 = None
    res4 = None

    #future1 = executor.submit(query_request, client3, sql, project)
    #res_t1 = future1.result()
    res_t1 = query_request(client3,sql,project)
    if not isinstance(res_t1, str):
        res3 = res_t1
    else:
        result['timeout3'] = 'timeout'
        return result

    #future2 = executor.submit(query_request, client4, sql, project)
    #res_t2 = future2.result()
    res_t2 = query_request(client4,sql,project)
    if not isinstance(res_t2, str):
        res4 = res_t2
    else:
        result['timeout4'] = 'timeout'
        return result

    result['realization3'] = res3.cube
    result['realization4'] = res4.realizations
    if res4.realizations is not None:

        if len(res4.realizations) > 0:
            result['realization4'] = [each['modelAlias'] for each in res4.realizations]

    result['duration3'] = res3.duration
    result['duration4'] = res4.duration

    result['isException3'] = res3.isException
    result['isException4'] = res4.isException

    result['storageCacheUsed3'] = res3.storageCacheUsed
    result['storageCacheUsed4'] = res4.storageCacheUsed

    result['exceptionMessage3'] = res3.exceptionMessage
    result['exceptionMessage4'] = res4.exceptionMessage

    result['id3'] = res3.id
    result['id4'] = res4.id

    result['server3'] = res3.server
    result['server4'] = res4.server

    result['pushDown3'] = res3.pushDown
    result['pushDown4'] = res4.pushDown

    result['timeout3'] = res3.timeout
    result['timeout4'] = res4.timeout

    result['rows3'] = res3.df.shape[0]
    result['rows4'] = res4.df.shape[0]

    is_same, coordinate, cells = compare_df(query_id, res3.df, res4.df)
    result['is_same'] = is_same
    result['coordinate_x'] = coordinate[0]
    result['coordinate_y'] = coordinate[1]
    result['cell3'] = ''
    result['cell4'] = ''

    result['cell3'] = cells[0]
    result['cell4'] = cells[1]

    if sys.version_info.major == 2:
        if type(cells[0]) == unicode:
            result['cell3'] = cells[0].encode('u8')

        if type(cells[1]) == unicode:
            result['cell4'] = cells[1].encode('u8')

    return result


general_csv_path = 'general_result.csv'
# 生成general_result.csv文件
if os.path.exists(general_csv_path):
    pass
else:
    with open(general_csv_path, 'w') as file:
        pass

general_csv = open(general_csv_path, 'r')
general_history = general_csv.read()
general_csv.close()


def check_qid_exist(qid):
    """ 判断query_id是否已经处理过"""
    if qid in general_history:
        print('%s  existed'% qid)
        return True
    return False


def write2csv():
    """写入对比结果到CSV"""
    with open(general_csv_path, 'a') as f:
        jobs = []
        for index, row in df_input.iterrows():
            query_id = row['query_id']
            sql = row['sql']
            project = row['project']
            if project in ['ai_keops','ai_vcode']:
                continue
            #if project not in projects:
                # 过滤出需要的project
                #continue
            exist1 = check_qid_exist(query_id)
            if exist1:
                #print('continue')
                continue
            else:
                print(len(jobs))

            jobs.append(executor.submit(get_general, query_id, sql, project))

        print('length of jobs',len(jobs))
        time.sleep(5)
        for job in futures.as_completed(jobs):
            # Read result from future
            result_done = job.result()

            writer = csv.DictWriter(f, result_done.keys(), delimiter='|')
            writer.writerow(result_done)
            print(result_done)
            print('number of jobs', len(jobs))




def convert_csv2excel():
    """将CSV转为Excel文件"""
    df = pd.read_csv('./general_result.csv', delimiter='|', names=keys)

    df.to_excel('general_result.xlsx', engine='openpyxl')


if __name__ == '__main__':
    #write2csv()
    convert_csv2excel()
