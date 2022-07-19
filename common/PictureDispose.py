from time import sleep
import numpy as np
import cv2
from common.ExcelConf import *
from base.SeleniumWrapper import SeleniumTools
import random
from common.BranchFactory import *


def error_loc(sheet,values,driver,path):
    end_index = [i.value for i in sheet[sheet.max_row]][0]
    for i in range(int(values[0]) + 1, int(end_index) + 2):
        failed_(sheet.cell, i, 8)
    # randomNo = list((str(random.random())[-8:])[::-1])
    # current_path = os.path.abspath(os.path.dirname(__file__)).split('common')[0][0:-1] + '\picture\\'

    # errorImg = f"./picture/{values[5]}_{''.join(randomNo)}.png"
    # print('errorImgerrorImg:',errorImg)
    # print(current_path+errorImg)
    # errorImg = f"./picture/error_1.png"
    # errorImg = f"./{''.join(randomNo)}.png"
    # driver.screenshot_img(path)
    row = [i.value for i in sheet[values[0]]]
    if not driver.is_element_exist(row[2],row[3]):
        driver.click_element(link="确定")
    element = driver.locator_element(row[2],row[3])
    draw(path,element)
    hyperlink_(sheet.cell, values[0] + 1, 8, path, 'FF0000')




def draw(path, *element):
    # image = cv2.imread(path)
    image = cv2.imdecode(np.fromfile(path,dtype=np.uint8),1)
    print(path)
    for item in element:
        left = item.location['x']
        top = item.location['y']
        right = item.location['x'] + item.size['width']
        bottom = item.location['y'] + item.size['height']
        print((left, top), (right, bottom))
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)

    # cv2.imwrite(path, image)
    cv2.imencode('.jpg', image)[1].tofile(path)


if __name__ == '__main__':
    path = '../picture/test00000000.png'
    driver = SeleniumTools()

    driver.visit_url(r'file:\\E:\UIAutomation\common\message.html')
    ele1 = driver.locator_element('xpath', '/html/body/form/table/tbody/tr[2]/td[2]')
    # ele2 = driver.locator_element('xpath', '/html/body/form/table/tbody/tr[3]/td[2]')
    # driver.screenshot_img(path)
    draw(path, ele1)
