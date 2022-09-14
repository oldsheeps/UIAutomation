import os

from case import Local_Test_Runner
from common.LoggerConfig import log


def _main():
    search_path = os.path.abspath(os.path.dirname(__file__)) + '/data/'

    cases = []
    # 读取指定路径下的所有文件
    for path, dir, files in os.walk(search_path):
        for file in files:
            # 获取文件的前后缀名
            file_type = os.path.splitext(file)[1]
            if file_type == '.xlsx':
                excel_path = path + file
                cases.append(excel_path)
            else:
                log.info(f"文件类型错误：{file}")

    for case in cases:
        log.info(f"加载[{case}]测试用例文件...")
        Local_Test_Runner.excel_ruuner(case)



if __name__ == '__main__':
    _main()
