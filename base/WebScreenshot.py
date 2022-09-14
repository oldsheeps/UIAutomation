import cv2
import numpy as np

from common.LoggerConfig import *

# 目录
directory = os.path.abspath(os.path.dirname(__file__)).split('base')[0] + 'picture\\'
# 文件
error_folder = 'error_screenshot\\'
steps_folder = 'steps_screenshot\\'


def draw_picture(driver, method, value, params):
    """
    这是一个特殊的方法，使用起来会比较困难;
    用于针对父元素截图并针对该父元素中的子元素进行矩形标记；
    method: 必填项，字符类型，父元素定位元素的方法和路径，格式如：xpath,//*[@id="1"]
    value:  必填项，字符类型，子元素定位元素的方法和路径，需要标记几个子元素就填写几个子元素定位参数
    params: 必填项，字符类型，图片保存名称
    return: 返回图片处理后的路径
    """
    global final_path
    try:
        # 检查截图保存名称是否有后缀，并拼接出最终保存路径
        pic_name = check_text_suffix(params)
        final_path = directory + steps_folder + pic_name

        # 矩形标记的起始元素零点坐标（父元素）
        loc_name,loc_path = str(method).split(',')
        zero = driver.locator_element(method=loc_name,value=loc_path)
        zero_loc = zero.location
        zero_size = zero.size
        mark = (zero_loc['x'], zero_loc['y'],
                     int(zero_size['width']), int(zero_size['height']))
        # 首先将父元素进行截图，作为草图备用
        zero.screenshot(final_path)
        log.info(f'webdriver：定位父元素，获取可以标记的坐标，画布大小[{mark}]!')

        # 将复数参数利用推导式进行分裂，形成每个元素的定位方法和路径为单独列表的形式储存
        # 如标记两个：[['xpath','//*[@name="username"]'],['xpath','//*[@name="passwords"]']]
        value = str(value).split(',')
        mark_element = [value[i:i + 2] for i in range(0, len(value) - 1, 2)]
        # 循环定位需要标记的子元素，将坐标以元组形式添加到列表
        coordinates = []
        for element in mark_element:
            target = driver.locator_element(method=element[0],value=element[1])
            target_loc = target.location
            target_size = target.size
            draw_site = (target_loc['x'], target_loc['y'],
                          int(target_size['width']), int(target_size['height']))
            coordinates.append(draw_site)
            log.info(f'webdriver：定位子元素，获取矩形标记的坐标，[{draw_site}]!')

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
            log.info(f'webdriver：在父元素的截图上，将子元素标记出来，标记坐标[{(left, top), (right, bottom)}]!')

        # 矩形标记后保存
        # cv2.imwrite(text, image)  # 同imread无法写入中文路径
        cv2.imencode('.jpg', image)[1].tofile(final_path)
        log.info(f'webdriver：矩形标记子元素成功，存放路径[{final_path}]!')
        return final_path
    except AttributeError as e:
        log.error(f'webdriver：请检查[{params}]路径是否正确!')
        log.error(traceback.format_exc())


def web_screenshot(driver, text, path):
    """
    截图保存到指定目录下
    params: 必填项，字符类型，截图名称
    path:   必填项，布尔类型，默认为True，区分步骤截图和异常截图的标志参数
    return: 作用于本地目录上，True存放steps_screenshot目录，False存放error_screenshot目录
    """
    try:
        # 根据path判断存放哪个目录下
        folder = steps_folder if path else error_folder
        # 检查截图保存名称是否有后缀，并拼接出最终保存路径
        pic_name = check_text_suffix(text)
        final_path = directory + folder + pic_name
        # 执行截图
        driver.get_screenshot_as_file(final_path)
        if path:
            log.info(f'webdriver：用例执行截图成功，存放路径：[{final_path}]!')
        else:
            log.info(f'webdriver：异常定位截图成功，存放路径：[{final_path}]!')
        return final_path
    except NameError:
        log.error(f'webdriver：请检查[{text}]文件名是否正确!')


def check_text_suffix(params):
    # 判断是否指定文件名后缀
    if params[str(params).rfind('.'):] not in ('.png', '.jpeg', '.jpg'):
        return params + '.png'
    else:
        return params
