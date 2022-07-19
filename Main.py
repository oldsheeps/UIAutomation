import os

from common import ReadExcel
from common.LogWrapper import log

if __name__ == '__main__':
    cases = []
    # 读取指定路径下的所有文件
    for path, dir, files in os.walk('./case/'):
        for file in files:
            # 获取文件的前后缀名
            file_type = os.path.splitext(file)[1]
            if file_type == '.xlsx':
                excel_path = path + file
                cases.append(excel_path)
            else:
                log.info(f"文件类型错误：{file}")

    for case in cases:
        log.info(f"运行{case}测试用例")
        ReadExcel.excel_ruuner(case)
