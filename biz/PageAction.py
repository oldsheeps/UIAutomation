from common.BranchFactory import *
from common.ExcelConf import *


def actions(excel, sheet, data, path, values, driver):

    # 断言可能不会只有一种，只要有assert关键字就是一个断言函数
    if str(branch(values[1])).startswith('assert'):
        # 将断言结果回填到Excel表中
        assertResult = getattr(driver, branch(values[1]))(**data)
        if assertResult:
            pass_(sheet.cell, values[0] + 1, 8)
        else:
            failed_(sheet.cell, values[0] + 1, 8)
        excel.save(path)    # 保存写入

    # 只要有acquire关键字就是获取一些数据值的函数
    elif str(branch(values[1])).startswith('acquire'):
        # 将获取到的数据回填到Excel表中
        acquireValue = getattr(driver, branch(values[1]))(**data)
        if acquireValue:
            value_(sheet.cell, values[0] + 1, 8, acquireValue)
        excel.save(path)    # 保存写入

    # 只要有screenshot关键字的就是截图函数
    elif str(branch(values[1])).startswith('screenshot'):
        getattr(driver, branch(values[1]))(**data)
        # 将截图存放路径处理成超链接插入到Excel表中
        hyperlink_(sheet.cell, values[0] + 1, 8, values[4],'FFFF00')
        excel.save(path)    # 保存写入


    # 可以被工厂类返回的函数
    elif branch(values[1]):
        getattr(driver, branch(values[1]))(**data)
        pass_(sheet.cell, values[0] + 1, 8)
        excel.save(path)
    # 其他函数
    else:
        getattr(driver, values[1])(**data)
        pass_(sheet.cell, values[0] + 1, 8)
        excel.save(path)