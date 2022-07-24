import time

from common.BranchFactory import *
from common.ExcelConf import *


def actions(excel, sheet, path, values, data, driver):
    """
    根据不同的测试行为执行对应关键字并作出相应的回填
    :param excel:   当前加载测试用例文件的工作簿对象
    :param sheet:   当前加载测试用例文件的Sheet对象
    :param path:    当前加载的测试用例文件保存地址
    :param values:  当前加载的测试用例文件的执行数据
    :param data:    当前执行的测试步骤调用的关键字所需要的参数
    :param driver:  当前执行的浏览器对象
    :return:        作用于sheet对象后保存
    """
    # 断言可能不会只有一种，只要有assert关键字就是一个断言函数
    if str(branch(values[1])).startswith('assert'):
        # 将断言结果回填到Excel表中,由于位置形参传递不够，在此添加一个text参数
        assertResult = getattr(driver, branch(values[1]))(**data)
        if assertResult:
            pass_(cell=sheet.cell, row=values[0] + 1, column=8)
        else:
            failed_(cell=sheet.cell, row=values[0] + 1, column=8)

    # 只要有acquire关键字就是获取一些数据值的函数
    elif str(branch(values[1])).startswith('acquire'):
        # 将获取到的数据回填到Excel表中
        acquireValue = getattr(driver, branch(values[1]))(**data)
        if acquireValue:
            value_(cell=sheet.cell, row=values[0] + 1, column=8, value=acquireValue)

    # 只要有screenshot关键字的就是截图函数
    elif str(branch(values[1])).startswith('screenshot'):
        save_path = getattr(driver, branch(values[1]))(**data)
        # 将截图存放路径处理成超链接插入到Excel表中
        hyperlink_(cell=sheet.cell, row=values[0] + 1, column=8, path=save_path, fgColor='FFFF00')

    # 可以被工厂类返回的函数
    elif branch(values[1]):
        getattr(driver, branch(values[1]))(**data)
        pass_(cell=sheet.cell, row=values[0] + 1, column=8)

    # 其他函数
    else:
        getattr(driver, values[1])(**data)
        pass_(cell=sheet.cell, row=values[0] + 1, column=8)

    excel.save(path)


def action_failed(excel, sheet, path, values, sheetName, driver):
    """
    如果发生异常，直接将后续的步骤判定为Failed，并对当前产生错误的步骤截图保存到表
    :param excel:    当前加载数据的工作簿对象
    :param sheet:    当前加载数据的sheet页对象
    :param path:     当前加载数据的文件保存地址
    :param values:   当前加载数据的sheet页中的一行数据
    :param sheetName:当前加载数据的Sheet名称
    :return:         作用于sheet对象后保存
    """
    end_index = [i.value for i in sheet[sheet.max_row]][0]
    for i in range(int(values[0]) + 1, int(end_index) + 2):
        failed_(cell=sheet.cell, row=i, column=8)

    # 以Sheet页名称+用力步骤编号+时间戳命名错误截图
    errorImgName = f"{sheetName}_{values[0]}_{str(int(time.time()))}"
    errorImgPath = driver.screenshot_save(errorImgName, False)

    hyperlink_(cell=sheet.cell, row=values[0] + 1, column=8, path=errorImgPath, fgColor='FF0000')

    excel.save(path)
