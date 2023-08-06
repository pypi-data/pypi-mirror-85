# KE-py
[![PyPI version](https://badge.fury.io/py/KE-py.svg)](https://badge.fury.io/py/KE-py)
[![Documentation Status](https://readthedocs.org/projects/ke-py/badge/?version=latest)](https://ke-py.readthedocs.io/en/latest/?badge=latest)

KE-py 是一个对Kyligence Enterprise Rest API 包装的Python SDK。
可以方便地通过使用Python对KE进行调用。为了更方便帮助KE开发者或维护者提供Python的对接和支持，
同时也可以通过IPython对KE进行实时交互。


## 安装
`pip install KE-py`

或者：

`pip install git+https://github.com/Kyligence/KE-py.git`

### Python环境
Python >= 3.6  or Python>=2.7

### 卸载
`pip uninstall ke-py`

## 快速入门 Getting Started
快速入门使用  [Quick Start](https://ke-py.readthedocs.io/en/latest/quick_start.html), 

关于安装和测试： [KE-py 安装与测试文档](https://ke-py.readthedocs.io/en/latest/install.html), 

使用案例以及最佳实践 [Examples](https://ke-py.readthedocs.io/en/latest/examples.html).



## 使用简介
### 连接KE服务
```text
from KE impot KE

client = KE('device2', username='ADMIN', password='KYLIN', version=3)
```

> For Developer, 对开发者如果需要debug，可以通过加debug参数打印debug信息
```text
client = KE('device2', username='ADMIN', password='KYLIN', version=3, debug=True)
```

### 操作项目
```text
projects = client.projects()
print(projects)

project = client.project('learn_kylin')
print(project)

# 获取当前project的所有 jobs
project.jobs()

# 获取当前project的所有cubes
project.cubes()
```

### 操作任务
```text
# 返回最近一周的jobs
jobs = client.jobs(time_filter=1)

job = jobs[0]
# 暂停job
job.pause()

# 获取更新的job progress
print(job.refresh(inplace=True).progress)

```

### 操作Cube
```text
cube = client.cubes(name='kylin_sales_cube')[0]
# 构建cube；会返回一个job对象。start_time  type 为datetime或timestamp
job = cube.build(start_time=datetime(2013, 2, 6, 8, 0, 0), end_time=datetime(2013, 2, 7, 8, 0, 0))

# 获取当前cube的所有segments
segments = cube.segments()
```

### 操作多个segment
```text
# 刷新segments
segments.refresh()

# 合并segments
segments.merge()
```

### 操作单个segment
```text
segment0 = cube.segments()[0]
# 查看单个segment创建时间
segment0.create_time_dt
```

### 查询
```text

qyery = client.query('select PART_DT, count(1) from kylin_sales group by PART_DT', project='learn_kylin')
# 返回pandas.DataFrame
query.df

       PART_DT COUNT(1)
0   2012-12-14       14
1   2012-08-28        7
2   2012-02-16       22
3   2013-10-19        8
4   2012-10-22       19
..         ...      ...
95  2012-02-20        9
96  2013-08-06       12
97  2013-06-27       18
98  2012-07-17        9
99  2013-10-12       11

[100 rows x 2 columns]

```

## 使用案例、实践

对于更多的实践和使用可以参考 [Examples文档](https://ke-py.readthedocs.io/en/latest/examples.html),
或者[Examples代码](examples)

## 文档 Document
更多文档请查阅 (latest development branch): [ReadTheDocs Documentation](https://ke-py.readthedocs.io/en/latest/)


## Reference
### API Document
- [KE3 Document](https://docs.kyligence.io/books/v3.3/zh-cn/rest/)
- [KE4 Document](https://docs.kyligence.io/books/v4.0/zh-cn/developer/v4/)