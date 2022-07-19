import openpyxl
import random
from base.SeleniumWrapper import SeleniumTools
from biz.PageAction import *
from common.LogWrapper import *
from common.PictureDispose import *

def excel_ruuner(path):
    global driver
    excel = openpyxl.load_workbook(path)

    try:
        # 获取所有的sheet页
        sheets = excel.sheetnames
        # 遍历所有的sheet页
        for sheet in sheets:
            sheet_temp = excel[sheet]

            # 遍历sheet页中所有的单元格
            log.info(f'---------------{sheet}---------------')
            for values in sheet_temp.values:
                # 读取用例的执行部分内容
                if type(values[0]) is int:
                    log.info(f'执行用例第{values[0]}步骤：{values[5]}')
                    # 定义一个字典，用于接收excel中的所有参数内容
                    data = {}
                    data['name'] = values[2]    # 定位方法
                    data['value'] = values[3]   # 定位路径
                    data['text'] = values[4]    # 输入文本
                    data['expect'] = values[6]  # 预期结果
                    # 优化测试数据内容，蒋所有为None的数据全部从data地点中清除
                    for key in list(data.keys()):
                        if data[key] is None:
                            del data[key]
                    # 判断是否实例化浏览器对象
                    if values[1] == '创建浏览器对象':
                        driver = SeleniumTools(values[4])
                        driver.implicit_wait(10)
                        pass_(sheet_temp.cell, values[0] + 1, 8)
                    else:
                        try:
                            # 执行每个测试步骤
                            actions(excel, sheet_temp, data, path, values, driver)
                        except Exception:
                            # log.error(traceback.format_exc())
                            randomNo = list((str(random.random())[-6:])[::-1])
                            errorImg = f"./picture/error_{values[5]}_{''.join(randomNo)}.png"
                            driver.screenshot_img(errorImg)
                            error_loc(sheet_temp,values,driver,errorImg)
                            # 如果发生异常，直接将后续的步骤判定为Failed后跳出循环，执行下一条用例
                            # end_index = [i.value for i in sheet_temp[sheet_temp.max_row]][0]
                            # for i in range(int(values[0]) + 1, int(end_index) + 2):
                            #     failed_(sheet_temp.cell, i, 8)
                            # randomNo = list((str(random.random())[-6:])[::-1])
                            # errorImg = f"./picture/error_{values[5]}_{''.join(randomNo)}.png"
                            # driver.screenshot_img(errorImg)
                            # hyperlink_(sheet_temp.cell, values[0] + 1, 8, errorImg,'FF0000')
                            excel.save(path)
                            break
    except Exception as e:
        log.error(traceback.format_exc())
    finally:
        excel.close()   # 关闭excel


if __name__ == '__main__':
    print('这是excel读取的类')
    excel_ruuner('../case/testcase.xlsx')
