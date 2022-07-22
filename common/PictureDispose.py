import cv2
import numpy as np

from base.WebDriverWrapper import *


def picture_draw(origin, path, *elements):
    org_loc = origin.location
    origin.screenshot(path)

    coordinates = []
    for element in elements:
        ele_loc = element.location
        ele_size = element.size
        coordinates.append((ele_loc['x'], ele_loc['y'], int(ele_size['width']), int(ele_size['height'])))

    # image = cv2.imread(path)
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), 1)

    for tag in coordinates:
        left = int(tag[0]) - int(org_loc['x'])
        top = int(tag[1]) - int(org_loc['y'])
        right = int(left) + int(tag[2])
        bottom = int(top) + int(tag[3])
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 3)

    cv2.imencode('.jpg', image)[1].tofile(path)


if __name__ == '__main__':
    path = '../picture/test00000000.png'
    driver = BrowserWrapper()

    driver.browser_visit(r'file:\\E:\UIAutomation\common\message.html')
    origin = driver.locator_element('xpath', '/html/body/form/table/tbody')
    element = driver.locator_element('xpath', '/html/body/form/table/tbody/tr[2]/td[2]')
    element1 = driver.locator_element('xpath', '/html/body/form/table/tbody/tr[5]/td[2]/font/input')

    picture_draw(origin, path, element, element1)
