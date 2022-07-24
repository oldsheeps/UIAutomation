import openpyxl
from selenium.common.exceptions import UnexpectedAlertPresentException

from base.WebDriverWrapper import BrowserWrapper
from biz.PageAction import *
from common.LogWrapper import *


def excel_ruuner(path):
    global driver
    excel = openpyxl.load_workbook(path)
    filename = path[str(path).rindex('/') + 1:str(path).rindex('.')]

    try:
        # 获取所有的sheet页
        sheetNames = excel.sheetnames
        # 遍历所有的sheet页
        for sheetName in sheetNames:
            sheet = excel[sheetName]
            # 遍历sheet页中所有的单元格
            log.info(f'------------------------------------------------------------')
            log.info(f'------------------------------------------------------------')
            log.info(f'----------开始执行：[{filename}] --->>> [{sheetName}] 用例----------')
            log.info(f'------------------------------------------------------------')
            log.info(f'------------------------------------------------------------')
            for values in sheet.values:
                # 读取用例的执行部分内容
                if type(values[0]) is int:
                    log.info(f'执行用例第{values[0]}步骤：{values[5]}')
                    # 定义一个字典，用于接收excel中的所有参数内容
                    data = {}
                    data['name'] = values[2]    # 定位方法
                    data['value'] = values[3]   # 定位路径
                    data['text'] = values[4]    # 输入文本
                    data['expect'] = values[6]  # 预期结果
                    # 优化测试数据内容，将所有为None的数据全部从data字典中清除
                    for key in list(data.keys()):
                        if data[key] is None:
                            del data[key]
                    # 判断是否实例化浏览器对象
                    if values[1] == '创建浏览器对象':
                        driver = BrowserWrapper(values[4])
                        driver.implicit_wait(10)
                        pass_(sheet.cell, values[0] + 1, 8)
                    else:
                        try:
                            # 执行每个测试步骤
                            actions(excel, sheet, path, values, data, driver)
                        except RecursionError:
                            log.error(traceback.format_exc())
                            log.error(f'webdriver对象：[RecursionError]映射失败,请检查[执行操作]是否填写错误!')
                            break
                        except UnexpectedAlertPresentException:
                            log.error(traceback.format_exc())
                            log.error(f'webdriver对象：[UnexpectedAlertPresentException]意外弹框,请检查[定位方法]是否填写错误!')
                            break
                        except Exception:
                            log.error(traceback.format_exc())
                            # 异常处理后跳出循环，执行下一条用例
                            action_failed(excel, sheet, path, values, sheetName, driver)
                            break
    except Exception:
        log.error(traceback.format_exc())
    finally:
        excel.close()  # 关闭excel


if __name__ == '__main__':
    print('这是excel读取的类')
    excel_ruuner('../case/testcase.xlsx')
