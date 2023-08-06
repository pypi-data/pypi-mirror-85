# coding=u8
from moz_sql_parser import parse, format as format_
import pandas as pd
from KE import KE

client3 = KE(host='kappy-prd.vivo.lan', port=8080, username='admin', password='kappy@111', version=3)
client4 = KE(host='10.193.147.131', version=4)


def get_all_projects_cubes():
    """{'project': ['cube1','cube2']"""
    result = {}

    projects = [p.name for p in client3.projects()]
    for p in projects:
        result[p['name']] = [each['realization'] for each in p['realizations'] if each['type'] == 'CUBE']

    return result


def replace_cube_sql(cube):
    """ 为了查KE4的 segment 的条数，需要用SQL来查，通过替换Model中自带的SQL来实现。也就是将select 字段部分替换为 count(1) """
    try:
        model = client4.models(name=cube)[0]
        sql = model.get_sql()

    except:
        return
    try:
        parsed = parse(sql)
    except:
        # print(sql)
        return ''
    parsed['select'] = {u'value': {u'count': 1}}
    new_sql = format_(parsed)
    return new_sql


# 输入要对比的projects
project_list = [  # 'ai_album',
    # 'ai_atlas',
    # 'ai_data_asset',
    # 'ai_engine',
    # 'ai_error_analysis',
    # 'ai_gomoku',
    # 'ai_jovi_picture',
    # 'ai_jovi_screen',
    # 'ai_jovi_voice',
    # 'ai_keops',
    'ai_message',
    'ai_msearch',
    'ai_scan',
    'ai_smart_favorites',
    'ai_smart_scene',
    'ai_user_travel',
    'ai_vivo_input',
    'ai_vshield',
    'ai_vtag',
    'ai_wplock',
    'ai_analysis_platform',
    'ai_smartboard']


def for_each_project():
    cubes = get_all_projects_cubes()
    data = []
    test_cubes_item = [('ai_atlas', ['da_atals_app_total_use_c'])]
    for project, cube_list in cubes.items():
        # for project, cube_list in test_cubes_item:
        # if project not in ['ai_vcode_hive', 'ai_keops_hive', 'ai_persona', 'ai_service_platform']:
        # continue
        if project in ['ai_common_game']:
            continue

        if project not in project_list:
            continue

        for cube in cube_list:

            new_sql = replace_cube_sql(cube)
            # print(new_sql)
            print(project)
            print(cube)
            cube3 = client3.cubes(project=project, name=cube)
            cube4 = client4.models(project=project, name=cube)
            if len(cube3) > 0 and len(cube4) > 0:
                # print(cube3[0].partition_desc)
                partition_desc = cube4[0].partition_desc
                if not partition_desc:
                    continue
                date_col = partition_desc.get('partition_date_column')
                if date_col:
                    print(date_col)
                    new_sql = "%s group by %s" % (new_sql, date_col)
                    new_sql = new_sql.replace('COUNT(1)', '%s, COUNT(1) ' % date_col)
                    print(new_sql)
                    query3 = client3.query(sql=new_sql, project=project, limit=1000)
                    query4 = client4.query(sql=new_sql, project=project, limit=1000)

                    df3 = query3.df
                    df4 = query4.df

                    if df3.shape[0] > 0 and df4.shape[0] > 0:
                        df3.columns = ['dt', 'count']
                        df4.columns = ['dt', 'count']
                        df3 = df3.sort_values('dt')
                        df4 = df4.sort_values('dt')

                        df = pd.merge(df3, df4, on=['dt'], how='outer')
                        df = df.fillna(0)
                        df['project'] = project
                        df['cube'] = cube
                        df['count_y'] = df['count_y'].astype(int)
                        df['count_x'] = df['count_x'].astype(int)
                        df['diff'] = df['count_y'] - df['count_x']
                        df = df.loc[df['diff'] != 0]
                        print(df)

                        df.to_csv('output/%s_%s.csv' % (project, cube))


if __name__ == '__main__':
    for_each_project()
