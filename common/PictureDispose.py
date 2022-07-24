import cv2
import numpy as np

from common.LogWrapper import *


def Pictureit(driver, name, value, text):
    global final_path
    try:
        final_path = os.path.abspath(os.path.dirname(__file__)).split('common')[
                         0] + 'picture\proce_pic\\' + text + '.png'
        zero = driver.locator_element(*(str(name).split(',')))
        zero_loc = zero.location
        zero.screenshot(final_path)

        # 将复数参数利用推导式进行分裂，形成每个元素的定位方法和路径为单独列表的形式储存
        # 如标记两个：[['xpath','//*[@name="username"]'],['xpath','//*[@name="passwords"]']]
        value = str(value).split(',')
        mark_element = [value[i:i + 2] for i in range(0, len(value) - 1, 2)]
        # 循环定位需要标记的两个子元素，将坐标以元组形式添加到列表
        coordinates = []
        for element in mark_element:
            target = driver.locator_element(*element)
            target_loc = target.location
            target_size = target.size
            coordinates.append(
                (target_loc['x'], target_loc['y'], int(target_size['width']), int(target_size['height'])))

        # 读取父元素截图
        # image = cv2.imread(path)  # 无法读取中文路径
        image = cv2.imdecode(np.fromfile(final_path, dtype=np.uint8), 1)

        # 循环每个子元素的坐标进行矩形标记
        for coord in coordinates:
            left = int(coord[0]) - int(zero_loc['x'])
            top = int(coord[1]) - int(zero_loc['y'])
            right = int(left) + int(coord[2])
            bottom = int(top) + int(coord[3])
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 3)

        # 矩形标记后保存
        # cv2.imwrite(text, image)  # 同imread无法写入中文路径
        cv2.imencode('.jpg', image)[1].tofile(final_path)
        log.info(f'webdriver对象：截图并矩形标记成功，存放路径：[{final_path}]!')
        return final_path
    except AttributeError as e:
        log.error(f'webdriver对象：请检查[{text}]路径是否正确!')
        log.error(traceback.format_exc())


def Screenshot_(driver, text, path):
    global final_path
    try:
        if path:
            final_path = os.path.abspath(os.path.dirname(__file__)).split('common')[
                             0] + 'picture\proce_pic\\' + text + '.png'
        else:
            final_path = os.path.abspath(os.path.dirname(__file__)).split('common')[
                             0] + 'picture\error_pic\\' + text + '.png'
        driver.get_screenshot_as_file(final_path)
        log.info(f'webdriver对象：截图成功，存放路径：[{final_path}]!')
        return final_path
    except NameError:
        log.error(f'webdriver对象：请检查[{text}]文件名是否正确!')
