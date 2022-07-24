import time

from selenium.common.exceptions import NoSuchElementException, TimeoutException, JavascriptException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from common.BranchFactory import *
from common.PictureDispose import *


# 缓存装饰器动态添加类属性（selnium webdriver类无限实例化控制成单浏览器）
class cached_class_property(object):
    def __init__(self, func):
        """
        默认构造函数
        :param func: 调用当前类的实例对象
        """
        self.func = func

    def __get__(self, obj, cls):
        """
        当一个类的类属性等于了另一个类实例的时候，
        且这个类实现了__get__(),__set__(),__delete__()三个其中一个，
        如果通过类属性访问，就会触发__get__()方法。
        :param obj: cls类的实例对象
        :param cls: 触发当前构造函数的类 <class '__main__.XXX'>
        :return: 触发当前构造函数的实例返回。
        如果没有return会抛出错误：AttributeError: 'NoneType' object has no attribute 'XX'
        """
        if obj is None:
            return self
        value = self.func(obj)
        setattr(cls, self.func.__name__, value)
        return value


class BrowserWrapper():
    """
    基于Selenium Web自动化工具进行二次封装的一个支持无限实例化webdriver类，
    但仍然可以保持使用同一个浏览器对象、支持使用自定义的方法、但同时又支持所有此类没有定义的方法。
    """

    def __init__(self, browser_name=None):
        """
        :param driver_name: 浏览器名字、数字或者字母
        """
        self.browser_name = '谷歌' if browser_name == None else browser_name

    @cached_class_property
    def driver(self):
        """
        将缓存装饰器注入进来，确保唯一实例时利用branch工厂创建对应的浏览器对象
        :return: 浏览器对象
        """
        driver = branch(self.browser_name)
        log.info(f'webdriver对象：启动浏览器[{self.browser_name}] --> 成功!')

        return driver

    def __getattr__(self, item):
        """
        想把其他的webdriver的操作方法直接添加进来，不再一个一个方法的写，然后调用driver属性的方法，不想一直搞冗余的代码。
        python先使用__getattribute__，查不到才会调用__getsttr__方法，利用这个特性，来实现将原生driver的属性到该类里面。
        :param item: 属性名
        :return: 调用item属性
        """
        # log.info('功能调用 --> 映射 --> ' + item)

        return getattr(self.browser_driver, item)

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # -----------------三种线程等待方式------------------- #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def sleep_wait(self, text):
        """
        强制等待
        :param text: 强制休眠秒数
        :return:     作用于线程
        """
        time.sleep(text)

    def hide_wait(self, name, value, timeout=10, frequency=0.5):
        """
        显示等待
        :param name:元素定位方法
        :param value:元素定位路径
        :param timeout:最大等待时长
        :param frequency:检测元素时间间隔
        :return:找到元素返回元素对象，否则抛出异常
        """
        hide_wait = WebDriverWait(driver=self.driver, timeout=timeout, poll_frequency=frequency)
        hide_wait.until(EC.visibility_of_element_located((name, value)))

    def implicit_wait(self, text):
        """
        隐式等待
        :param text:全局等待元素出现的秒数
        :return:作用于线程
        """
        self.driver.implicitly_wait(text)

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # ----------------执行JavaScript脚本----------------- #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def exec_script(self, text, *args):
        """
        执行指定Script脚本
        :param text: 需要执行的JavaScript脚本
        :param args: 其他适用于JavaScript的脚本
        :return:作用于页面
        """
        try:
            self.driver.execute_script(text, *args)
        except JavascriptException as e:
            log.error(f'webdriver对象：无法执行[{text}]script脚本!')
            pass

    def slide_scroll_to_bottom(self):
        """滑动滚动条至底部"""
        self.exec_script("window.scrollTo(0,document.body.scrollHeight)")

    def slide_scroll_to_yardage(self, text):
        """
        滑动滚动条至指定码数
        :param text: 滚动条下拉的码数
        :return: 作用于页面
        """
        self.exec_script(f"window.scrollTo(0,{text})")

    def HighLight(self, element):
        """
        基于元素定位关键字进行页面元素样式的更改，实现执行步骤的高亮显示
        :param element: 元素定位对象
        :return: 作用于页面某元素的样式
        """
        for i in range(0, 2):
            self.exec_script("arguments[0].setAttribute('style',arguments[1]);",
                             element, "background: pink; border:5px solid red;")
            self.sleep_wait(0.2)
            self.exec_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
            self.sleep_wait(0.2)

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # ---------------常规webdriver关键字----------------- #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def browser_visit(self, text):
        """
        在当前webdriver对象中访问url网页
        :param text: url
        :return: 作用于webdriver对象
        """
        log.info(f'webdriver对象：访问[{text}]地址!')
        self.driver.get(text)

    def browser_forward(self):
        """使当前webdriver对象前进到后一页url"""
        self.driver.forward()

    def browser_back(self):
        """使当前webdriver对象后退到前一页url"""
        self.driver.back()

    def browser_refresh(self):
        """使当前webdriver对象刷新url"""
        self.driver.refresh()

    def browser_label_close(self):
        """关闭当前webdriver对象所在标签页"""
        log.info(f'webdriver对象：关闭当前浏览器标签页!')
        self.driver.close()

    def browser_quit(self):
        """关闭浏览器"""
        log.info(f'webdriver对象：退出浏览器并销毁[webdriver]对象!')
        self.driver.quit()

    def locator_element(self, name, value):
        """
        使用当前webdriver对象以name方式在当前页面中定位value元素（一个元素）
        :param name: 元素定位方法
        :param value: 元素定位路径
        :return: 返回定位到的元素对象（一个）并执行高亮显示
        """
        try:
            log.info(f'webdriver对象：以[{name}]方式定位[{value}]元素!')
            self.hide_wait(name, value)
        except TimeoutException:
            log.info(f'webdriver对象：找不到元素，以[{name}]方式定位[{value}]元素定位失败!')
        finally:
            element = self.driver.find_element(name, value)
            self.HighLight(element)
            return element

    def locator_more_element(self, name, value):
        """
        使用当前webdriver对象以name方式在当前页面中定位value元素（多个元素）
        :param name: 元素定位方法
        :param value: 元素定位路径
        :return: 返回定位到的元素对象（多个）并执行高亮显示
        """
        try:
            log.info(f'webdriver对象：以[{name}]方式定位[{value}]一组元素!')
            self.hide_wait(name, value)
        except TimeoutException:
            log.info(f'webdriver对象：找不到元素，以[{name}]方式定位[{value}]一组元素定位失败!')
        finally:
            elements = self.driver.find_elements(name, value)
            self.HighLight(elements)
            return elements

    def input_element(self, name, value, text):
        """
        使用当前webdriver对象以name方式在当前页面中定位value元素，执行输入text文本
        :param name: 元素定位方法
        :param value: 元素定位路径
        :param text: 输入的文本值
        :return: 作用于元素对象
        """
        self.locator_element(name, value).send_keys(text)
        log.info(f'webdriver对象：以[{name}]方式定位[{value}]元素并输入[{text}]文本!')

    def clear_element(self, name, value):
        """
        使用当前webdriver对象以name方式在当前页面中定位value元素，执行清空预设值操作
        :param name: 元素定位方法
        :param value: 元素定位路径
        :return: 作用于元素对象
        """
        self.locator_element(name, value).clear()
        log.info(f'webdriver对象：以[{name}]方式定位[{value}]元素并清空预设值!')

    def click_element(self, name, value):
        """
        使用当前webdriver对象以name方式在当前页面中定位value元素，执行点击操作
        :param name: 元素定位方法
        :param value: 元素定位路径
        :return: 作用于元素对象
        """
        self.locator_element(name, value).click()
        log.info(f'webdriver对象：以[{name}]方式定位[{value}]元素并点击!')

    def screenshot_save(self, text, path=True):
        """
        截图保存到指定目录下
        :param text: 截图名称
        :param path: 默认为True存放proce_pic目录，False存放error_pic目录
        :return: 作用于本地目录
        """
        return Screenshot_(self.driver, text, path)

    def screenshot_draw(self, name, value, text):
        """
        这是一个特殊的方法，使用起来会比较困难，针对父元素截图并针对该元素中的子元素进行矩形标记
        :param name: 父元素，复数参数，定位元素的方法和路径，如xpath,//*[@id="1"]
        :param value: 子元素，复数参数，需要矩形标记的子元素定位方法和路径，需要标记几个元素就填写几个元素定位参数
        :param text: 处理后的图片保存路径
        :return: 作用于截图
        """
        return Pictureit(self, name, value, text)

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # -------------------获取某些信息--------------------- #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def acquire_title(self):
        """获取当前标签页名称"""
        return self.driver.title

    def acquire_url(self):
        """获取当前标签页的URL"""
        return self.driver.current_url

    def acquire_current_handles(self):
        """获取当前窗口的句柄"""
        return self.driver.current_window_handle

    def acquire_all_handles(self):
        """获取所有窗口的句柄"""
        return self.driver.window_handles

    def acquire_element_attr(self, name, value, text):
        """
        获取元素属性
        :param name: 定位元素方法
        :param value: 定位元素路径
        :param text: 获取元素指定属性（textContent、text、innerHTML、outerHTML）
        :return: 返回元素的相关属性
        """
        return self.locator_element(name, value).get_attribute(text)

    def acquire_element_text(self, name, value):
        """获取元素的文本（一个元素）"""
        return self.locator_element(name, value).text

    def acquire_elements_text(self, name, value):
        """获取元素的文本（多个元素）"""
        all_text = self.locator_element(name, value)
        text_list = []
        for one_text in all_text:
            text_list.append(one_text.text)
        return text_list

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # ---------------文本、属性、弹框断言------------------ #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def assert_text(self, name, value, expect):
        """
        元素对象的文本断言
        :param name:定位元素方法
        :param value: 定位元素路径
        :param expect: 预期值
        :return: 作用于用户判断行为
        """
        try:
            reality = self.locator_element(name, value).text
            assert expect == reality or expect in reality, '断言失败'
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    def assert_text_reverse(self, name, value, expect):
        """文本断言取反"""
        status = self.assert_text(name, value, expect)
        if status:
            return not status

    def assert_attr(self, name, value, text, expect):
        """
        元素对象的属性断言
        :param name:定位元素方法
        :param value: 定位元素路径
        :param text:获取元素指定属性（textContent、text、innerHTML、outerHTML）
        :param expect:期望值
        :return:作用于用户判断行为
        """
        try:
            reality = self.acquire_element_attr(name, value, text)
            assert expect == reality, '断言失败'
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    def assert_alert(self, name, expect):
        """
        页面弹出框断言
        :param name:弹出框类型（alert、confirm）
        :param expect: 期望值
        :return: 作用于用户判断行为
        """
        try:
            WebDriverWait(driver=self.driver, timeout=10).until(EC.alert_is_present())
            if name in ['alert', 'confirm']:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                assert expect == alert_text or expect in alert_text, '断言失败'
                return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    def assert_alert_reverse(self, name, expect):
        """弹出框断言取反"""
        status = self.assert_alert(name, expect)
        if status:
            return not status

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # -----------------窗口和Frame切换-------------------- #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def switch_to_frame(self, text=None, name=None, value=None):
        """
        指定id或name属性或使用元素定位切入框架
        :param text:指定Frame的id或name
        :param name:无id或neme，利用元素定位方法
        :param value:元素定位的路径
        :return:作用于Frame框架切换
        """
        if name and value:
            element = self.locator_element(name, value)
            WebDriverWait(self.driver, timeout=10).until(EC.frame_to_be_available_and_switch_to_it(element))
            log.info(f'webdriver对象：切入[{element}]Frame框架成功!')
        elif text:
            # 判断frame是否可切入，如果可切入就执行切入
            WebDriverWait(self.driver, timeout=10).until(EC.frame_to_be_available_and_switch_to_it(text))
            log.info(f'webdriver对象：切入[{text}]Frame框架成功!')
        else:
            log.info(f'webdriver对象：切入Frame框架失败，必须给定参数!')

    def switch_to_window(self, text):
        """切换到指定窗口"""
        self.driver.switch_to.window(text)

    def switch_to_parent_frame(self):
        """返回上一层frame框架"""
        self.driver.switch_to.parent_frame()

    def switch_to_default_content(self):
        """返回默认frame框架"""
        self.driver.switch_to.default_content()

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # -----------------Select下拉框处理------------------- #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def switch_to_select(self, stuff):
        """将元素对象转换成Select对象"""
        return Select(stuff)

    def select_choice(self, name, value, text, expect):
        """
        下拉框选择
        :param name:元素定位方法
        :param value: 元素定位路径
        :param text: 元素条件
        :param expect:下拉框类型（index、value、text）
        :return:
        """
        if expect in [1, 'index', '索引']:
            self.switch_to_select(self.locator_element(name, value)).select_by_index(text)
        elif expect in [2, 'value', '属性']:
            self.switch_to_select(self.locator_element(name, value)).select_by_value(text)
        elif expect in [3, 'text', '文本']:
            self.switch_to_select(self.locator_element(name, value)).select_by_visible_text(text)
        else:
            log.info(f'webdriver对象：以[{name}]方式定位[{value}]元素下拉选择{text}失败!')

    def select_choice_quit(self, name, value, text, expect):
        """
        取消下拉框选择
        :param name:元素定位方法
        :param value: 元素定位路径
        :param text: 元素条件
        :param expect:下拉框类型（index、value、text）
        :return:
        """
        if expect in [1, 'index', '索引']:
            self.switch_to_select(self.locator_element(name, value)).deselect_by_value(text)
        elif expect in [2, 'value', '属性']:
            self.switch_to_select(self.locator_element(name, value)).deselect_by_value(text)
        elif expect in [3, 'text', '文本']:
            self.switch_to_select(self.locator_element(name, value)).deselect_by_value(text)
        else:
            log.info(f'webdriver对象：以[{name}]方式定位[{value}]元素下拉选择取消{text}失败!')

    # 取消所有选择下拉框的备选项
    def select_choice_quit_all(self, name, value):
        return self.switch_to_select(self.locator_element(name, value)).deselect_all()

    def select_all_options(self, select_object):
        """获取下拉列表框所有备选项"""
        all_options = []
        if isinstance(select_object, Select):
            for item in select_object.options:
                all_options.append(item.text)
        else:
            for item in Select(select_object).options:
                all_options.append(item.text)
        return all_options

    def select_final_choice(self, select_object):
        """获取下拉列表框最终选择项"""
        selected_options = []
        if isinstance(select_object, Select):
            for item in select_object.all_selected_options:
                selected_options.append(item.text)
        else:
            for item in Select(select_object).all_selected_options:
                selected_options.append(item.text)
        return selected_options

    def select_is_multiple(self, select_object):
        """判断下拉列表框是否可以多选"""
        mark = False
        if isinstance(select_object, Select):
            mark = True if select_object.is_multiple else False
        return mark

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # ------------ActionChains鼠标键盘相关---------------- #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def mouse_hover(self, name, value):
        """鼠标悬停某元素"""
        return ActionChains(self.driver).move_to_element(self.locator_element(name, value)).perform()

    def mouse_double_click(self, name, value):
        """双击某元素"""
        return ActionChains(self.driver).double_click(self.locator_element(name, value)).perform()

    def mouse_right_click(self, name, value):
        """右击某元素"""
        return ActionChains(self.driver).context_click(self.locator_element(name, value)).perform()

    def mouse_drag(self, name, value):
        """将某元素拖拽到某元素"""
        start = driver.locator_element(*(str(name).split(',')))
        end = driver.locator_element(*(str(value).split(',')))
        return ActionChains(self.driver).drag_and_drop(start, end).perform()

    # -------------------------------------------------- #
    # -------------------------------------------------- #
    # --------------------用户行为关键字------------------ #
    # -------------------------------------------------- #
    # -------------------------------------------------- #
    def is_new_window(self, oldAllwindows, newAllwindows):
        """
        判断是否为新窗口
        :param oldAllwindows: 原窗口句柄
        :param newAllwindows: 现窗口句柄
        :return: 作用于窗口切换
        """
        if len(oldAllwindows) != newAllwindows:
            for window in newAllwindows:
                if window not in oldAllwindows:
                    new_window = window
                    return new_window
        else:
            return False

    def open_new_window(self):
        """打开新的标签页并将句柄切换过去"""
        old_headles = self.acquire_all_handles()
        self.exec_script("window.open('','_blank');")
        new_headles = self.acquire_all_handles()
        new_window = self.is_new_window(old_headles, new_headles)
        self.switch_to_window(new_window)

    def switch_to_new_window(self):
        """将句柄切换至新窗口"""
        old_headles = self.acquire_current_handles()
        new_headles = self.acquire_all_handles()
        index = new_headles.index(old_headles)
        self.switch_to_window(new_headles[index + 1])

    def is_element_exist(self, name, value):
        """
        判断某元素是否存在
        :param name: 元素定位方法
        :param value: 元素定位路径
        :return: 用于用户行为判断
        """
        try:
            self.locator_element(name, value)
        except NoSuchElementException:
            return False
        else:
            return True

    def foreach_element_click(self, name, value, text=None):
        """
        定位一组元素对象并遍历，根据条件点击元素对象
        :param name:元素定位方法
        :param value:元素定位路径
        :param text:点击第一个元素
        :return:作用于一组元素对象
        """
        elements = self.locator_more_element(name, value)
        for index, element in enumerate(elements):
            if text == None:
                element.click()
            else:
                if index == text:
                    element.click()

    def close_alert(self, name='alert', value=None):
        """
        关闭弹出框：如果是alert、confirm警告弹出框就直接点击确认，
        如果是prompt交互弹出框则判断是否需要填值，如果无值可填便取消；
        :param name:弹出框的类型，默认alert
        :param value: prompt弹出框是否需要输入文本
        :return: 作用于各类弹出框
        """
        try:
            WebDriverWait(driver=self.driver, timeout=10).until(EC.alert_is_present())
            if name in ['alert', 'confirm']:
                self.driver.switch_to.alert.accept()
            elif name == 'prompt':
                if value:
                    self.driver.switch_to.alert.send_keys(value)
                    self.driver.switch_to.alert.accept()
                else:
                    self.driver.switch_to.alert.dismiss()
            else:
                log.info(f'webdriver对象：请确认弹框的类型，暂不支持{name}类型!')
            log.info(f'webdriver对象：关闭{name}类型的弹框成功!')
        except Exception as e:
            log.info(f'webdriver对象：关闭{name}类型的弹框失败!')

    def click_and_jump(self, name, value):
        """
        点击元素对象并跳转至新窗口
        :param name: 元素定位方法
        :param value: 元素定位路径
        :return: 作用于webdriver对象句柄
        """
        old_handles = self.acquire_all_handles()  # 获取点击之前的所有窗口句柄
        self.click_element(name, value)
        # 判断新窗口是否打开
        WebDriverWait(self.driver, timeout=10, ).until(EC.new_window_is_opened(old_handles))
        new_handles = self.acquire_all_handles()  # 再次获取所有窗口的句柄
        self.switch_to_window(new_handles[-1])


if __name__ == '__main__':
    driver = BrowserWrapper()

    driver.browser_visit(r'http://www.baidu.com/')
    driver.input_element('id', 'kw', 'hhhhh')
    driver.click_element('id', 'su')
    driver.sleep_wait(2)
    driver.screenshot_save('test_1.png', False)
    driver.screenshot_save('test_22222.png')
