import time

from factory.BranchFactory import *


def actions(execute_func, driver, data):
    """
    根据不同的测试行为执行对应关键字并作出相应的回填
    :param execute_func: 当前页面行为所需要调用的关键字方法名称
    :param driver: 当前实例的浏览器对象
    :param data: 当前关键字所需要的参数
    :param result:当前步骤执行结果
    :return:返回当前步骤执行结果
    """
    assertResult = None
    acquireValue = None
    save_path = None
    # 断言可能不会只有一种，只要有assert关键字就是一个断言函数
    if str(branch(execute_func)).startswith('assert'):
        # 将断言结果回填到Excel表中
        assertResult = getattr(driver, branch(execute_func))(**data)

    # 只要有acquire关键字就是获取一些数据值的函数
    elif str(branch(execute_func)).startswith('acquire'):
        # 将获取到的数据回填到Excel表中
        acquireValue = getattr(driver, branch(execute_func))(**data)

    # 只要有screenshot关键字的就是截图函数
    elif str(branch(execute_func)).startswith('screenshot'):
        save_path = getattr(driver, branch(execute_func))(**data)

    # 可以被工厂类返回的函数
    elif branch(execute_func):
        getattr(driver, branch(execute_func))(**data)

    # 其他非自定义函数
    else:
        getattr(driver, execute_func)(**data)

    if assertResult:
        result = True
    elif acquireValue:
        result = acquireValue
    elif save_path:
        result = save_path
    elif assertResult == acquireValue == save_path == None:
        result = True
    else:
        result = False

    return result


def action_failed(caseName, caseIndex, driver):
    """
    如果发生异常，对当前产生错误的步骤截图保存
    :param caseName: 当前测试用例的名称
    :param caseIndex: 当前测试步骤的编号
    :param driver: 当前实例的浏览器对象
    :return: 返回截图路径
    """
    # 以Sheet页名称+用力步骤编号+时间戳命名错误截图
    errorImgName = f"{caseName}_{caseIndex[0]}_{str(int(time.time()))}"
    errorImgPath = driver.screenshot_save(errorImgName, False)
    return errorImgPath
