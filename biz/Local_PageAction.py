import time
from common.LoggerConfig import *
from factory.BranchFactory import *


def actions(excel_obj, sheet_obj, file_path, case_step, case_data, driver):
    """
    根据不同的测试行为执行对应关键字并作出相应的回填
    :param excel_obj:   当前加载测试用例文件的工作簿对象
    :param sheet_obj:   当前加载测试用例文件的Sheet对象
    :param file_path:   当前加载的测试用例文件保存地址
    :param case_step:   当前加载的测试用例文件的执行数据
    :param case_data:   当前执行的测试步骤调用的关键字所需要的参数
    :param driver:      当前执行的浏览器对象
    :return:            作用于sheet对象后保存
    """
    if str(branch(case_step[1])).startswith('if') \
            or str(branch(case_step[1])).startswith('elif') \
                or str(branch(case_step[1])).startswith('else'):
        branch_status = getattr(driver, branch(case_step[1]))(**case_data)
        if branch_status is False:
            branch_status = 'Continue'
            log.error(f'webdriver：执行[{case_step[1]}]分支时，条件不成立，跳过执行!')
        elif branch_status is True:
            branch_status = 'Pass'
            log.error(f'webdriver：执行[{case_step[1]}]分支时，条件成立，开始执行!')
        excel_obj.set_cell_value(sheet_obj=sheet_obj,sheet_row=case_step[0] + 1,sheet_col=8,cell_value=branch_status)
        excel_obj.save(file_path)
        return branch_status

    # 可以被工厂类返回的函数
    elif branch(case_step[1]):
        status = getattr(driver, branch(case_step[1]))(**case_data)
        if status not in (True,False) and os.path.exists(status):
            excel_obj.hyperlink_(sheet_obj=sheet_obj,sheet_row=case_step[0] + 1,sheet_col=8,file_path=status,fgColor='00FF00')
        elif status is False:
                excel_obj.failed_(sheet_obj=sheet_obj, sheet_row=case_step[0] + 1, sheet_col=8)
        elif status is True:
            excel_obj.pass_(sheet_obj=sheet_obj, sheet_row=case_step[0] + 1, sheet_col=8)
        else:
            excel_obj.set_cell_value(sheet_obj=sheet_obj,sheet_row=case_step[0] + 1,sheet_col=8,cell_value=status)

    # 其他非自定义函数
    else:
        getattr(driver, case_step[1])(**case_data)
        excel_obj.pass_(sheet_obj=sheet_obj, sheet_row=case_step[0] + 1, sheet_col=8)

    excel_obj.save(file_path)



def action_failed(excel_obj, sheet_obj, file_path, case_step, sheetName, driver):
    """
    如果发生异常，直接将后续的步骤判定为Failed，并对当前产生错误的步骤截图保存到表
    :param excel_obj:   当前加载数据的工作簿对象
    :param sheet_obj:   当前加载数据的sheet页对象
    :param file_path:   当前加载数据的文件保存地址
    :param case_step:   当前加载数据的sheet页中的一行数据
    :param sheetName:   当前加载数据的Sheet名称
    :param driver:      当前执行的浏览器对象
    :return:            作用于sheet对象后保存
    """
    end_index = [i.value for i in sheet_obj[sheet_obj.max_row]][0]
    for i in range(int(case_step[0]) + 1, int(end_index) + 2):
        excel_obj.failed_(sheet_obj=sheet_obj, sheet_row=i, sheet_col=8)

    # 以Sheet页名称+用力步骤编号+时间戳命名错误截图
    errorImgName = f"{sheetName}_{case_step[0]}_{str(int(time.time()))}"
    errorImgPath = driver.acquire_screenshot_save(params=errorImgName, path=False)

    excel_obj.hyperlink_(sheet_obj=sheet_obj,sheet_row=case_step[0] + 1,
                         sheet_col=8,file_path=errorImgPath,fgColor='FF0000')
    excel_obj.save(file_path)
