from selenium.common.exceptions import UnexpectedAlertPresentException

from base.WebDriver import Drivers
from biz.Local_PageAction import *
from case.ScriptEnhance import *
from common.ExcelConfig import *


def excel_ruuner(path):
    global driver
    global acquireValue
    excel = Excel(path)
    filename = path[str(path).rindex('/') + 1:str(path).rindex('.')]
    cfg_path = './config/database.cfg'
    cfg_section = 'uat'
    try:
        # 遍历所有的sheet页
        for sheetName in excel.get_all_sheet_name():
            # 如果sheet页名称是以调用-开头则不认为是用例
            if str(sheetName).startswith('@'):
                continue
            # 获取sheet对象
            sheet = excel.get_sheet_object(sheetName)
            # 提示语
            log_mark(filename, sheetName)
            # 遍历sheet页中所有的单元格
            rows_data = excel.get_sheet_rows(sheet)['rows_data']
            for values in rows_data:
                # 读取用例的执行部分内容 序号为int类型 并且 执行方法不为空
                if isinstance(values[0], int) and values[1] not in ["", None, False]:
                    logging.info('-')
                    log.info(f'执行测试用例第{values[0]}步骤：{values[5]}')

                    # 创建action行为参数字典
                    case_data = params_filter(values)

                    # 判断是否实例化浏览器对象
                    if values[1] in ('启动', '启动页面', '启动浏览器', '创建浏览器对象'):
                        driver = Drivers(values[4])
                        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                        screenshot_path = driver.acquire_screenshot_save(
                            params=f"Step_{values[0]}_{values[5]}_{current_time}")
                        excel.hyperlink_(sheet_obj=sheet,
                                         sheet_row=values[0] + 1,
                                         sheet_col=8,
                                         file_path=screenshot_path)
                    elif values[1] == '调用脚本':
                        # 假定此时拥有脚本id，根据id到数据库中查询，以列表形式返回
                        # 执行调用来的脚本，执行完毕后将返回步骤数量，回填到指定列
                        index = call_script(driver, cfg_path, cfg_section)
                        excel.set_cell_value(sheet, values[0] + 1, 8, index)

                    # 处理如果分支
                    elif str(values[8]).startswith('如果') and not str(values[1]).startswith('如果'):
                        status = driver.if_handles_status[values[8]]
                        if status:
                            acquireValue = actions(excel, sheet, path, values, case_data, driver)
                        else:
                            log.error(f'webdriver：[{values[0]}-{values[1]}]跳过执行!')
                            excel.continue_(sheet, values[0] + 1, 8)

                    elif str(values[8]).startswith('或者') and not str(values[1]).startswith('或者'):
                        index = values[8][2:]
                        var = driver.if_handles_status['如果' + index]
                        if var:
                            log.error(f'webdriver：[{values[0]}-{values[1]}]跳过执行!')
                            excel.continue_(sheet, values[0] + 1, 8)
                        else:
                            status = driver.elif_handles_status[values[8]]
                            if status:
                                acquireValue = actions(excel, sheet, path, values, case_data, driver)
                            else:
                                log.error(f'webdriver：[{values[0]}-{values[1]}]跳过执行!')
                                excel.continue_(sheet, values[0] + 1, 8)

                    elif str(values[8]).startswith('否则') and not str(values[1]).startswith('否则'):
                        index = values[8][2:]
                        var = driver.if_handles_status['如果' + index]
                        if var:
                            log.error(f'webdriver：[{values[0]}-{values[1]}]跳过执行!')
                            excel.continue_(sheet, values[0] + 1, 8)
                        else:
                            status = driver.else_handles_status[values[8]]
                            if status:
                                acquireValue = actions(excel, sheet, path, values, case_data, driver)
                            else:
                                log.error(f'webdriver：[{values[0]}-{values[1]}]跳过执行!')
                                excel.continue_(sheet, values[0] + 1, 8)

                    elif str(values[1]).startswith('循环'):
                        call_sheet_1 = excel.get_sheet_object(values[2])
                        call_rows_1 = excel.get_sheet_rows(call_sheet_1)['rows_data']
                        excel.pass_(sheet, values[0] + 1, 8)
                        log.error(f'@@@@@@@@@：调用[{values[2]}]脚本，执行循环步骤!')

                        for x in range(values[4]):
                            for row1 in call_rows_1:
                                log.info(f'执行[{values[2]}]脚本的第{row1[0]}步骤：{row1[5]}')
                                if str(row1[2]).startswith('@'):
                                    call_sheet_2 = excel.get_sheet_object(row1[2])
                                    call_rows_2 = excel.get_sheet_rows(call_sheet_2)['rows_data']
                                    excel.pass_(call_sheet_1, row1[0] + 1, 8)
                                    log.error(f'@@@@@@@@@：调用[{row1[2]}]脚本，执行循环步骤!')

                                    for y in range(row1[4]):
                                        for row2 in call_rows_2:
                                            log.info(f'执行[{row1[2]}]脚本的第{row2[0]}步骤：{row2[5]}')
                                            if str(row2[2]).startswith('@'):
                                                call_sheet_3 = excel.get_sheet_object(row2[2])
                                                call_rows_3 = excel.get_sheet_rows(call_sheet_3)['rows_data']
                                                excel.pass_(call_sheet_2, row2[0] + 1, 8)
                                                log.error(f'@@@@@@@@@：调用[{row2[2]}]脚本，执行循环步骤!')

                                                for z in range(row2[4]):
                                                    for row3 in call_rows_3:
                                                        log.info(f'执行[{row2[2]}]脚本的第{row3[0]}步骤：{row3[5]}')
                                                        call_case_data = params_filter(row3)
                                                        acquireValue = actions(excel, call_sheet_3, path, row3,
                                                                               call_case_data, driver)
                                            else:
                                                call_case_data = params_filter(row2)
                                                acquireValue = actions(excel, call_sheet_2, path, row2,
                                                                       call_case_data, driver)
                                else:
                                    call_case_data = params_filter(row1)
                                    acquireValue = actions(excel, call_sheet_1, path, row1, call_case_data, driver)
                    else:
                        try:
                            acquireValue = actions(excel, sheet, path, values, case_data, driver)
                        except RecursionError:
                            log.error(traceback.format_exc())
                            log.error(f'webdriver：[RecursionError]映射失败,请检查[执行操作]是否填写错误!')
                            break
                        except UnexpectedAlertPresentException:
                            log.error(traceback.format_exc())
                            log.error(f'webdriver：[UnexpectedAlertPresentException]意外弹框,请检查[定位方法]是否填写错误!')
                            break
                        except Exception:
                            log.error(traceback.format_exc())
                            # 异常处理后跳出循环，执行下一条用例
                            action_failed(excel, sheet, path, values, sheetName, driver)
                            break
    except Exception:
        log.error(traceback.format_exc())
    finally:
        excel.save(path)
        excel.close()  # 关闭excel


if __name__ == '__main__':
    # print('这是excel读取的类')
    # excel_ruuner('../data/关键字框架测试用例Demo-循环.xlsx')
    log_mark('hello world.xlsx', '哈喽世界')
