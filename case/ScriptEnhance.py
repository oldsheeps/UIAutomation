from factory.BranchFactory import branch
from common.DataBaseConfig import *

# 调用脚本
def call_script(driver,cfg_path,section):
    global index
    database = DataBase(cfg_path,section)
    script_data = database.query_every_data(table='testcase',field='*')
    # 二维列表
    for index,rows in enumerate(script_data):
        script = params_filter(rows)
        getattr(driver, branch(rows[1]))(**script)
    return index


# 数据过滤
def params_filter(steps):
    # 定义一个字典，用于接收excel中的所有参数内容
    steps_handle = {}
    steps_handle['index'] = steps[0]     # 可能是定位方法、变量处理条件
    steps_handle['action'] = steps[1]     # 可能是定位方法、变量处理条件
    steps_handle['method'] = steps[2]     # 可能是定位方法、变量处理条件  name
    steps_handle['value'] = steps[3]    # 可能是定位路径、变量处理条件    value
    steps_handle['params'] = steps[4]     # 步骤行为所需要的文本、参数   text
    steps_handle['desc'] = steps[5]   # 分支控制、变量新数据    # 0822:1856添加
    steps_handle['expect'] = steps[6]   # 预期结果、变量名
    steps_handle['result'] = steps[7]   # 预期结果、变量名
    steps_handle['branch'] = steps[8]   # 分支控制、变量新数据    # 0822:1856添加

    # 优化测试数据内容，将所有为None的数据全部从字典中清除
    for key in list(steps_handle.keys()):
        if steps_handle[key] is None or steps_handle[key] == '':
            del steps_handle[key]

    return steps_handle

# 循环次数数据处理
def foreach_data():
    pass

def log_mark(file_name,sheet_name):
    log.info(f'-'*70)
    log.info(f'-'*70)
    log.info('-----开始执行:{:^20s} --->>> {:^17s} 案例-----'.format(file_name,sheet_name))
    log.info(f'-'*70)
    log.info(f'-'*70)

