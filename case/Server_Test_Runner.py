from selenium.common.exceptions import UnexpectedAlertPresentException

from base.WebDriver import Drivers
from biz.PageAction import *
from common.LoggerConfig import *


def excel_ruuner(*step):
    global driver
    case_result = None
    case_data = {}
    case_data['name'] = step[1]     # 定位方法
    case_data['value'] = step[2]    # 定位路径
    case_data['text'] = step[3]     # 输入文本
    case_data['expect'] = step[5]   # 定位方法
    for key in list(case_data.keys()):
        if case_data[key] is None:
            del case_data[key]
    try:
        # 判断是否实例化浏览器对象
        if step[0] in ('创建浏览器对象','启动浏览器','启动'):
            driver = Drivers(case_data['text'])
            driver.implicit_wait(20)
            case_result = True
        else:
            try:
                # 执行每个测试步骤
                case_result = actions(step[0], driver, case_data)
            except RecursionError:
                log.error(traceback.format_exc())
                log.error(f'webdriver：[RecursionError]映射失败,请检查[执行操作]是否填写错误!')
            except UnexpectedAlertPresentException:
                log.error(traceback.format_exc())
                log.error(f'webdriver：[UnexpectedAlertPresentException]意外弹框,请检查[定位方法]是否填写错误!')
            except Exception:
                case_result = action_failed('测试用例名称', '测试步骤编号', driver)
                # 异常处理后跳出循环，执行下一条用例
                log.error(traceback.format_exc())
    except Exception:
        log.error(traceback.format_exc())
    finally:
        return case_result


if __name__ == '__main__':
    print('这是excel读取的类')
    excel_ruuner('../case/关键字框架测试用例Demo-循环.xlsx')
