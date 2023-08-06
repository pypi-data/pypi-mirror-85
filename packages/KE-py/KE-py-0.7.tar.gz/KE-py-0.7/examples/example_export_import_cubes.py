# coding=u8
"""
脚本时间功能：
导出某个project的指定models，导出为zip文件；
通过zip文件导入model

可以通过此方式来备份models元数据；
或可作为测试环境到生产环境的model上线流程
"""


from KE import KE
from KE.client import KE4CONF as CONF

# host: KE实例主机名
# port: 端口，默认7070
# username: 用户名
# password: 密码
# version: 4代表KE4；3代表KE3
client = KE(host=CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=4)

# 获取project对象
# name为项目的名字
project = client.projects(name='learn_kylin')[0]

# 导出项目中指定的models;
# models: 导出的模型名字，如果多个model则以list的形式，如：['model1','model2']
# dest_path: 导出的zip文件名绝对路径
project.export_models(models='model1', dest_path='/tmp/20201001.zip')

# 导入models到指定的项目中; 注意：导入的models一定需要在导入环境中不存在model！
# models: 导入的模型名字，如果多个model则以list的形式，如：['model1','model2']
# dest_path: 导入的zip文件名绝对路径
project.import_models(models='model1', dest_path='/tmp/20201001.zip')


"""
注意：
export_models、import_models
一般两个方法需要放在两个不同的文件里，导出一个脚本；导入一个脚本。
因为导入导出是两个分开的过程。很有可能是两个完全隔离的环境。
通常，导出文件后则需要迁移zip文件到新的一个环境再导入。
"""