import pyautogui  # 界面
from selenium.common.exceptions import NoSuchElementException, JavascriptException  # 异常
from selenium.webdriver.common.action_chains import ActionChains  # 鼠标
from selenium.webdriver.common.keys import Keys  # 键盘
from selenium.webdriver.support import expected_conditions as EC  # 显示等待需要的条件包
from selenium.webdriver.support.select import Select  # 下拉框
from selenium.webdriver.support.ui import WebDriverWait  # 显示等待

from base.WebBranchHandle import *
from base.WebOperation import *
from base.WebScreenshot import *


class Command(object):

    def __init__(self, driver):
        self.driver = driver  # 浏览器驱动
        self.global_variable_list = {}  # 用例过程中的全局变量
        self.if_handles_status = {}     # if如果分支判断状态
        self.elif_handles_status = {}   # elif或者分支判断状态
        self.else_handles_status = {}   # else否则分支判断状态
        self.current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    """ ------------------------------------------------------------
        -----------------------三种线程等待方式-----------------------
        ------------------------------------------------------------
        ------------------强制等待、隐式等待、显示等待------------------ 
        ------------------------------------------------------------ """

    def sleep_wait(self, **kwargs):
        """
        强制等待指定秒数级时间
        params: 必填项，整数类型，强制等待时间
        return: 等待指定时间后返回True
        """
        if int(kwargs['params']) > 0:
            time.sleep(int(kwargs['params']))
            log.info(f"webdriver：强制等待[{int(kwargs['params'])}]秒!")
        return True

    def implicit_wait(self, **kwargs):
        """
        隐式等待全局元素加载到DOM树中
        params: 必填项，整数类型，隐式等待最长时间
        return: 等待指定时间后返回True
        """
        self.driver.implicitly_wait(int(kwargs['params']))
        log.info(f"webdriver：隐式等待[{int(kwargs['params'])}]秒!")
        return True

    def is_element_exist(self, timeout=10, frequency=0.5, **kwargs):
        """
        显示等待某个元素在指定时间内出现在DOM树中并可见
        timeout:   必填项，数字类型，默认10秒，显示最长等待时间
        frequency: 必填项，数字类型，默认0.5秒，轮询频率
        method:    必填项，字符类型，元素定位方法
        value:     必填项，字符类型，元素定位路径
        return：   成功等待返回True，否则返回False
        """
        try:
            start = datetime.datetime.now()
            hide_wait = WebDriverWait(driver=self.driver, timeout=timeout, poll_frequency=frequency)
            hide_wait.until(EC.visibility_of_element_located((kwargs['method'], kwargs['value'])))
            end = datetime.datetime.now()
            if int(str(end - start)[-9:-7]) > 0:
                log.info(f"webdriver：显示等待[{str(end - start)[-9:-7]}]秒!")
        except:
            return False
        else:
            return True

    """ ------------------------------------------------------------
        -----------------------JavaScript脚本-----------------------
        ------------------------------------------------------------ 
        ---------------执行、滚至底部、滚动指定码数、闪烁----------------
        ------------------------------------------------------------ """

    def exec_script(self, params, *args, **kwargs):
        """
        执行指定JavaScript脚本
        params: 必填项，字符类型，需要执行的JavaScript脚本
        args:   非必填，元组类型，其他适用于JavaScript的附加参数
        kwargs: 非必填，字典类型，略
        return: 成功作用于页面返回True，否则返回False
        """
        try:
            self.driver.execute_script(params, *args)
            return True
        except JavascriptException as e:
            log.error(f'webdriver：无法执行[{params}]script脚本!')
            return False

    def slide_scroll_to_bottom(self, **kwargs):
        """滑动滚动条至底部"""
        self.exec_script("window.scrollTo(0,document.body.scrollHeight)")
        log.info(f'webdriver：将滚动条滑动至页面底部!')
        return True

    def slide_scroll_to_yardage(self, **kwargs):
        """
        滑动滚动条至指定码数位置
        params: 必填项，数字类型，滚动条下拉的码数
        return: 成功作用于页面则返回True
        """
        self.exec_script(f"window.scrollTo(0,{kwargs['params']})")
        log.info(f"webdriver：将滚动条滑动至[{kwargs['params']}]码数位置!")
        return True

    def high_light(self, element):
        """
        基于元素定位关键字进行页面元素样式的更改，实现执行步骤的高亮显示
        element: 必填项，元素定位对象
        return:  作用于页面某元素的样式
        """
        for i in range(0, 2):
            self.exec_script("arguments[0].setAttribute('style',arguments[1]);",
                             element, "background: pink; border:5px solid red;")
            self.sleep_wait(params=0.2)
            self.exec_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
            self.sleep_wait(params=0.2)

    def step_high_light_screenshot(self,element=None,**kwargs):
        """
        实现每一步用例高亮显示并截图保存
        element:必填项，默认为None，元素定位对象，如element为None表示不需要或无法更改页面样式则直接截图
        index:  必填项，字符类型，当前用例步骤编号
        desc：  必填项，字符类型，当前用例步骤描述
        return: 截图完成后返回路径
        """
        save_path = f"step_{kwargs['index']}_{kwargs['desc']}_{self.current_time}"
        if element:
            self.exec_script("arguments[0].setAttribute('style',arguments[1]);", element,
                             "background: pink; border:5px solid red;")
            self.sleep_wait(params=0.2)
            save_path = self.acquire_screenshot_save(params=save_path)
            self.exec_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
        else:
            save_path = self.acquire_screenshot_save(params=save_path)
        return save_path

    """ ------------------------------------------------------------
        ---------------------常规webdriver关键字---------------------
        ---------------访问、前进、后退、刷新、关闭标签页----------------
        ---------------退出浏览器、定位、输入、清空、点击----------------
        ------------------------------------------------------------ """

    def browser_visit(self, **kwargs):
        """通过webdriver对象访问指定url网页"""
        params = kwargs['params']
        self.driver.get(params)
        log.info(f'webdriver：访问[{params}]地址!')
        self.implicit_wait(params=20)
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def browser_forward(self, **kwargs):
        """使当前webdriver对象前进到后一页url"""
        log.info(f'webdriver：在{self.driver.title}页面执行[前进]!')
        self.driver.forward()
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def browser_back(self, **kwargs):
        """使当前webdriver对象后退到前一页url"""
        log.info(f'webdriver：在{self.driver.title}页面执行[后退]!')
        self.driver.back()
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def browser_refresh(self, **kwargs):
        """使当前webdriver对象刷新url"""
        log.info(f'webdriver：在{self.driver.title}页面执行[刷新]!')
        self.driver.refresh()
        self.sleep_wait(params=2)
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def browser_label_close(self, **kwargs):
        """关闭当前webdriver对象所在标签页"""
        log.info(f'webdriver：关闭[{self.driver.title}]标签页!')
        self.driver.close()
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def browser_quit(self):
        """关闭浏览器"""
        self.driver.quit()
        log.info(f'webdriver：退出浏览器并销毁[webdriver]对象!')
        return True

    def locator_element(self, **kwargs):
        """
        使用当前webdriver对象以method方式在当前页面中定位value元素（单元素）
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        return: 返回定位到的元素对象（一个）并执行高亮显示
        """
        method = kwargs['method']
        value = kwargs['value']
        # 检查元素定位方式是否正确
        if method not in (
                'id', 'name', 'class_name', 'link text',
                'partial link text', 'tag name', 'xpath', 'css selector'):
            raise TypeError(f"webdriver：无法以[{method}]方式定位元素！")
        # 利用显示等待机制定位一个元素并通过JS高亮闪烁元素
        if self.is_element_exist(method=method, value=value):
            log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功!')
            element = self.driver.find_element(method, value)
            self.high_light(element)
            return element
        else:
            raise NoSuchElementException(f'webdriver：找不到元素，以[{method}]方式定位[{value}]元素定位失败!')

    def locator_more_element(self, **kwargs):
        """
        使用当前webdriver对象以method方式在当前页面中定位value元素（多元素）
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        return: 返回定位到的元素对象（多个）并执行高亮显示
        """
        method = kwargs['method']
        value = kwargs['value']
        # 检查元素定位方式是否正确
        if method not in (
                'id', 'name', 'class_name', 'link text',
                'partial link text', 'tag name', 'xpath', 'css selector'):
            raise TypeError(f"webdriver：无法以[{method}]方式定位元素！")
        # 利用显示等待机制定位一组元素并通过JS高亮闪烁元素
        if self.is_element_exist(method=method, value=value):
            log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功!')
            elements = self.driver.find_elements(method, value)
            self.high_light(elements)
            return elements
        else:
            raise NoSuchElementException(f'webdriver：找不到元素，以[{method}]方式定位[{value}]元素定位失败!')

    def input_element(self, **kwargs):
        """
        使用当前webdriver对象以method方式在当前页面中定位value元素，执行输入text文本
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        params: 必填项，字符类型，输入的文本值
        return: 执行在指定元素中输入文本并截图后返回保存路径
        """
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params']
        element = self.locator_element(method=method, value=value)
        # 执行输入前先清空预设值
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.BACK_SPACE)
        # 处理要输入的文本，检查是否为变量
        text = input_text_handle(params, self.global_variable_list)
        element.send_keys(str(text))
        log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功并输入[{text}]文本!')
        save_path = self.step_high_light_screenshot(element,**kwargs)
        return save_path

    def clear_element(self, **kwargs):
        """
        使用当前webdriver对象以method方式在当前页面中定位value元素，执行清空预设值操作
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        return: 执行清空指定元素中的预设值并截图后返回保存路径
        """
        method = kwargs['method']
        value = kwargs['value']
        element = self.locator_element(method=method, value=value)
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.BACK_SPACE)
        log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功并清空预设值!')
        save_path = self.step_high_light_screenshot(element,**kwargs)
        return save_path

    def click_element(self, **kwargs):
        """
        使用当前webdriver对象以method方式在当前页面中定位value元素，执行点击操作
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        return: 执行点击指定元素并截图后返回保存路径
        """
        method = kwargs['method']
        value = kwargs['value']
        element = self.locator_element(method=method, value=value)
        log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功并点击!')
        save_path = self.step_high_light_screenshot(element,**kwargs)
        element.click()
        return save_path

    """ ------------------------------------------------------------
        --------------------------截图保存---------------------------
        ------------------------------------------------------------ 
        --------------------截图保存、截图标记保存---------------------
        ------------------------------------------------------------ """

    def acquire_screenshot_save(self, path=True, **kwargs):
        """
        截图保存到指定目录下
        params: 必填项，字符类型，截图名称
        path:   必填项，布尔类型，默认为True，区分步骤截图和异常截图的标志参数
        return: 作用于本地目录上，True存放steps_screenshot目录，False存放error_screenshot目录
        """
        params = kwargs['params']
        return web_screenshot(self.driver, params, path)

    def acquire_screenshot_draw(self, **kwargs):
        """
        这是一个特殊的方法，使用起来会比较困难;
        用于针对父元素截图并针对该父元素中的子元素进行矩形标记；
        method: 必填项，字符类型，父元素定位元素的方法和路径，格式如：xpath,//*[@id="1"]
        value:  必填项，字符类型，子元素定位元素的方法和路径，需要标记几个子元素就填写几个子元素定位参数
        params: 必填项，字符类型，图片保存名称
        return: 返回图片处理后的路径
        """
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params']
        return draw_picture(self, method, value, params)

    """ ------------------------------------------------------------
        --------------------获取页面、元素、窗口信息--------------------
        --------------标题、网址、当前窗口句柄、所有窗口句柄--------------
        ----------元素属性值、元素文本值（一个）、元素文本值（多个）--------
        ------------------------------------------------------------ """
    def acquire_title(self, **kwargs):
        """获取当前标签页名称，以expect为key值保存于变量字典中"""
        expect = kwargs['expect']
        self.global_variable_list[expect] = self.driver.title
        log.info(f'webdriver：当前标签页名称[{self.driver.title}]!')
        return self.global_variable_list[expect]

    def acquire_url(self, **kwargs):
        """获取当前标签页的URL，以expect为key值保存于变量字典中"""
        expect = kwargs['expect']
        self.global_variable_list[expect] = self.driver.current_url
        log.info(f'webdriver：当前标签页地址[{self.driver.current_url}]!')
        return self.global_variable_list[expect]

    def acquire_current_handles(self, **kwargs):
        """获取当前窗口的句柄"""
        return self.driver.current_window_handle

    def acquire_all_handles(self, **kwargs):
        """获取所有窗口的句柄"""
        return self.driver.window_handles

    def acquire_element_attr(self, **kwargs):
        """
        获取元素属性值
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        params: 必填项，字符类型，默认为value，获取属性类型，如：value、textContent、text、innerHTML、outerHTML
        expect: 必填项，字符类型，变量名
        return: 返回元素的属性值，以expect为key值保存于变量字典中
        """
        method = kwargs['method']
        value = kwargs['value']
        expect = kwargs['expect']
        if 'params' not in kwargs.keys():
            params = 'value'
        else:
            params = kwargs['params']
        element = self.locator_element(method=method, value=value)
        element_attr = element.get_attribute(params)
        self.global_variable_list[str(expect)] = element_attr
        log.info(f'webdriver：获取元素属性成功，将值存入变量[${str(expect)}$={element_attr}]!')
        save_path = self.step_high_light_screenshot(element,**kwargs)
        return save_path

    def acquire_element_text(self, **kwargs):
        """
        获取元素的文本（单元素）
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        expect: 必填项，字符类型，变量名
        return: 返回元素的文本值，以expect为key值保存于变量字典中
        """
        method = kwargs['method']
        value = kwargs['value']
        expect = kwargs['expect']
        element = self.locator_element(method=method, value=value)
        element_text = element.text
        # 检查text方式是否可以获取到文本值，如若不能则尝试通过js再获取一次
        if not element_text:
            element_text = self.driver.execute_script("return arguments[0].value", element)
        self.global_variable_list[str(expect)] = element_text
        log.info(f'webdriver：获取元素文本成功，将值存入变量[${str(expect)}$={element_text}]!')
        save_path = self.step_high_light_screenshot(element,**kwargs)
        return save_path

    def acquire_elements_text(self, **kwargs):
        """获取元素的文本（多个元素）"""
        method = kwargs['method']
        value = kwargs['value']
        expect = kwargs['expect']
        elements = self.locator_more_element(method=method, value=value)
        save_path = self.step_high_light_screenshot(elements,**kwargs)
        text_list = []
        # 遍历组元素获取每个元素的text文本值
        for one_text in elements:
            text_list.append(one_text.text)
        self.global_variable_list[str(expect)] = text_list
        log.info(f'webdriver：获取多个元素文本成功，将值存入变量[${str(expect)}$={text_list}]!')
        return save_path

    """ -----------------------------------------------------------
        ---------------------文本、属性、弹框断言---------------------
        ---------------元素文本断言存在、元素文本断言不存在--------------
        ---------------元素属性断言存在、元素属性断言不存在--------------
        --------------弹出框文本断言存在、弹出框文本断言不存在------------
        ------------------------------------------------------------ """

    def assert_text(self, **kwargs):
        """
        元素对象的文本断言
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        expect: 必填项，字符类型，预期值
        return: 作用于用户判断行为，元素定位文本与预期值一直返回True，否则返回False
        """
        method = kwargs['method']
        value = kwargs['value']
        expect = kwargs['expect']
        try:
            reality = self.locator_element(method=method, value=value).text
            assert expect == reality or expect in reality, '断言失败'
            log.info(f'webdriver：文本断言成功，[{expect}] in [{reality}]!')
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    def assert_text_reverse(self, **kwargs):
        """文本断言取反"""
        method = kwargs['method']
        value = kwargs['value']
        expect = kwargs['expect']
        try:
            reality = self.locator_element(method=method, value=value).text
            assert expect != reality or expect not in reality, '断言失败'
            log.info(f'webdriver：文本断言成功，[{expect}] not in [{reality}]!')
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    def assert_attr(self, **kwargs):
        """
        元素对象的属性断言
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        params: 必填项，字符类型，属性类型
        expect: 必填项，字符类型，预期值
        return: 作用于用户判断行为，元素定位文本与预期值一直返回True，否则返回False
        """
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params']
        expect = kwargs['expect']
        try:
            reality = self.acquire_element_attr(method=method, value=value, params=params)
            # assert expect == reality, '断言失败'
            assert expect == reality or expect in reality, '断言失败'
            log.info(f'webdriver：属性断言成功，[{expect}] in [{reality}]!')
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    def assert_attr_reverse(self, **kwargs):
        """属性断言取反"""
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params']
        expect = kwargs['expect']
        try:
            reality = self.acquire_element_attr(method=method, value=value, params=params)
            assert expect != reality or expect not in reality, '断言失败'
            log.info(f'webdriver：属性断言成功，[{expect}] not in [{reality}]!')
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    def assert_alert(self, **kwargs):
        """
        页面弹出框断言
        method: 必填项，字符类型，弹出框类型（alert、confirm）
        expect: 必填项，字符类型，期望值
        return: 作用于用户判断行为，弹出框文本与预期值一直返回True，否则返回False
        """
        method = kwargs['method']
        expect = kwargs['expect']
        try:
            WebDriverWait(driver=self.driver, timeout=10).until(EC.alert_is_present())
            if method in ['alert', 'confirm']:
                alert = self.driver.switch_to.alert
                time.sleep(1)
                alert_text = alert.text
                time.sleep(1)
                alert.accept()
                assert expect == alert_text or expect in alert_text, '断言失败'
                log.info(f'webdriver：弹出框断言成功，[{expect}] in [{alert_text}]!')
                return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    def assert_alert_reverse(self, **kwargs):
        """弹出框断言取反"""
        method = kwargs['method']
        expect = kwargs['expect']
        try:
            WebDriverWait(driver=self.driver, timeout=10).until(EC.alert_is_present())
            if method in ['alert', 'confirm']:
                alert = self.driver.switch_to.alert
                time.sleep(1)
                alert_text = alert.text
                time.sleep(1)
                alert.accept()
                assert expect != alert_text or expect not in alert_text, '断言失败'
                log.info(f'webdriver：弹出框断言成功，[{expect}] not in [{alert_text}]!')
                return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    """ ------------------------------------------------------------
        --------------------页面窗口、Frame框架切换--------------------
        ------------------------------------------------------------ 
        ----------切入框架、切入窗口、返回上层框架、返回默认框架-----------
        ------------------------------------------------------------ """

    def switch_to_frame(self, **kwargs):
        """
        切换frame框架，1.通过定位切入；2.通过frame的id或name切入
        method: 非必填，字符类型，元素定位方法
        value:  非必填，字符类型，元素定位路径
        params: 非必填，字符类型，通过frame的id或name切入
        return: 切换成功后返回True
        """
        method = kwargs['method'] if 'method' in kwargs.keys() else None
        value = kwargs['value'] if 'value' in kwargs.keys() else None
        params = kwargs['params'] if 'params' in kwargs.keys() else None
        if method and value:
            element = self.locator_element(method=method, value=value)
            WebDriverWait(self.driver, timeout=10).until(EC.frame_to_be_available_and_switch_to_it(element))
            log.info(f'webdriver：切入[{method}-{value}]Frame框架成功!')
        elif params:
            WebDriverWait(self.driver, timeout=10).until(EC.frame_to_be_available_and_switch_to_it(params))
            log.info(f'webdriver：切入[{params}]Frame框架成功!')
        else:
            log.info(f'webdriver：切入Frame框架失败，必须给定切入方式和参数!')
            return False
        return True

    def switch_to_assign_window(self, **kwargs):
        """切换到指定窗口"""
        params = kwargs['params']
        handles = self.acquire_all_handles()
        self.driver.switch_to.window(handles[-int(params)])
        log.info(f'webdriver：跳转至倒数第{params}个窗口成功!')
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def switch_to_window(self, new_windows):
        """切换到指定窗口"""
        self.driver.switch_to.window(new_windows)
        return True

    def switch_to_parent_frame(self, **kwargs):
        """返回上一层frame框架"""
        self.driver.switch_to.parent_frame()
        log.info(f'webdriver：返回上一次进入的Frame框架!')
        return True

    def switch_to_default_content(self, **kwargs):
        """返回默认frame框架"""
        self.driver.switch_to.default_content()
        log.info(f'webdriver：进入[{self.driver.title}]页面的默认Frame框架!')
        return True

    """ ------------------------------------------------------------
        -----------------------Select下拉框处理-----------------------
        ---------对象转换、下拉选择、下拉选择取消、下拉选择取消所有---------
        -----获取下拉所有选择项、获取最终选择项、判断下拉框是否可以多选------
        ------------------------------------------------------------ """

    def switch_to_select(self, stuff):
        """将元素对象转换成Select对象"""
        return Select(stuff)

    def select_choice(self, **kwargs):
        """
        下拉框选择
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        params: 必填项，字符类型，元素下拉选择的值
        expect: 必填项，字符类型，元素下拉类型，如：index、value、text
        return: 执行下拉选择成功后并截图后返回保存路径
        """
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params']
        expect = kwargs['expect']
        element = self.locator_element(method=method, value=value)
        select_obj = self.switch_to_select(element)
        if expect in [1, 'index', '索引']:
            select_obj.select_by_index(params)
            log.info(f'webdriver：以[{method}]方式定位[{value}]下拉框成功，选择{params}成功!')
        elif expect in [2, 'value', '属性']:
            select_obj.select_by_value(params)
            log.info(f'webdriver：以[{method}]方式定位[{value}]下拉框成功，选择{params}成功!')
        elif expect in [3, 'text', '文本']:
            select_obj.select_by_visible_text(params)
            log.info(f'webdriver：以[{method}]方式定位[{value}]下拉框成功，选择{params}成功!')
        else:
            log.info(f'webdriver：无法以[{expect}]方式，选择下拉框的内容!')
        save_path = self.step_high_light_screenshot(element,**kwargs)
        return save_path

    def select_choice_quit(self, **kwargs):
        """取消下拉框选择，反选（deselect）取消操作只适用于添加了multiple的下拉框，否则会报错"""
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params']
        expect = kwargs['expect']
        element = self.locator_element(method=method, value=value)
        if expect in [1, 'index', '索引']:
            self.switch_to_select(element).deselect_by_index(params)
            log.info(f'webdriver：以[{method}]方式定位[{value}]下拉框成功，取消{params}成功!')
        elif expect in [2, 'value', '属性']:
            self.switch_to_select(element).deselect_by_value(params)
            log.info(f'webdriver：以[{method}]方式定位[{value}]下拉框成功，取消{params}成功!')
        elif expect in [3, 'text', '文本']:
            self.switch_to_select(element).deselect_by_visible_text(params)
            log.info(f'webdriver：以[{method}]方式定位[{value}]下拉框成功，取消{params}成功!')
        else:
            log.info(f'webdriver：无法以[{expect}]方式，取消下拉框的选择!')
        save_path = self.step_high_light_screenshot(element, **kwargs)
        return save_path

    def select_choice_quit_all(self, **kwargs):
        """取消所有选择下拉框的备选项"""
        method = kwargs['method']
        value = kwargs['value']
        element = self.locator_element(method=method, value=value)
        self.switch_to_select(element).deselect_all()
        log.info(f'webdriver：取消所有以[{method}]方式定位[{value}]下拉选择元素!')
        save_path = self.step_high_light_screenshot(element, **kwargs)
        return save_path

    # 暂时未使用
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

    """ ------------------------------------------------------------
        ------------------ActionChains鼠标键盘相关--------------------
        --------------鼠标悬停、鼠标双击、鼠标右击、鼠标拖拽--------------
        -------键盘全选、键盘复制、键盘粘贴、键盘剪切、键盘光标组合键-------
        ------------------------------------------------------------ """

    def mouse_hover(self, **kwargs):
        """鼠标悬停某元素"""
        method = kwargs['method']
        value = kwargs['value']
        element = self.locator_element(method=method, value=value)
        ActionChains(self.driver).move_to_element(element).perform()
        log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功并模拟鼠标悬停至该元素上!')
        save_path = self.step_high_light_screenshot(element, **kwargs)
        return save_path

    def mouse_double_click(self, **kwargs):
        """双击某元素"""
        method = kwargs['method']
        value = kwargs['value']
        element = self.locator_element(method=method, value=value)
        log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功并模拟鼠标执行双击!')
        save_path = self.step_high_light_screenshot(element, **kwargs)
        ActionChains(self.driver).double_click(element).perform()
        return save_path

    def mouse_right_click(self, **kwargs):
        """右击某元素"""
        method = kwargs['method']
        value = kwargs['value']
        element = self.locator_element(method=method, value=value)
        log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功并模拟鼠标执行右击!')
        ActionChains(self.driver).context_click(element).perform()
        save_path = self.step_high_light_screenshot(element, **kwargs)
        return save_path

    def mouse_drag(self, **kwargs):
        """将某元素拖拽到某元素"""
        method = kwargs['method'].split(',')
        value = kwargs['value'].split(',')
        start = self.locator_element(method=method[0], value=method[1])
        # 让鼠标移动到起点元素上
        pyautogui.moveTo(start.location['x'] + 10, start.location['y'] + 80)
        # 定位要拖拽到的位置元素
        end = self.locator_element(method=value[0], value=value[1])
        # 实现拖拽功能
        pyautogui.dragTo(end.location['x'] + 10, end.location['y'] + 80, duration=1)
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def text_edit_options(self, **kwargs):
        """
        全选、复制、粘贴、剪切
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        params: 必填项，字符类型，功能类型，如：全选a、复制c、粘贴v、剪切x
        return: 功能完成后返回True
        """
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params']
        element = self.locator_element(method=method, value=value)
        if str(params) == '全选':
            element.send_keys(Keys.CONTROL, 'a')
        elif str(params) == '复制':
            element.send_keys(Keys.CONTROL, 'c')
        elif str(params) == '粘贴':
            element.send_keys(Keys.CONTROL, 'v')
        elif str(params) == '剪切':
            element.send_keys(Keys.CONTROL, 'x')
        log.info(f'webdriver：针对[{method}]方式定位[{value}]的元素进行[{params}]文本编辑!')
        save_path = self.step_high_light_screenshot(element, **kwargs)
        return save_path

    def keyboard_control(self, **kwargs):
        """
        键盘控制光标方向、位置
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        params: 必填项，字符类型，功能类型，如：dict字典
        expect: 非必填，数字类型，params执行次数
        return: 功能完成后返回True
        """
        """键盘控制输入"""
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params']
        expect = kwargs['expect'] if 'expect' in kwargs.keys() else None
        dict = {
            '上': Keys.UP, '下': Keys.DOWN, '左': Keys.LEFT, '右': Keys.RIGHT,
            '行首': Keys.HOME, '行尾': Keys.END,
            '退格': Keys.BACK_SPACE, '回车': Keys.ENTER,
            '上翻': Keys.PAGE_UP, '下翻': Keys.PAGE_DOWN, '上档': Keys.SHIFT,
        }
        element = self.locator_element(method=method, value=value)
        if expect:
            element.send_keys(dict.get(params) * expect)
            log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功，模拟键盘操作[{params}按键*{expect}]!')
        else:
            element.send_keys(dict.get(params))
            log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功，模拟键盘操作[{params}]按键!')
        save_path = self.step_high_light_screenshot(element, **kwargs)
        return save_path

    """ ------------------------------------------------------------
        ------------------------------------------------------------
        ---------------if、elif、else、foreach分支处理----------------
        ------------------------------------------------------------
        ------------------------------------------------------------ """
    def if_branch(self, **kwargs):
        return if_branch_handle(self, **kwargs)

    def elif_branch(self, **kwargs):
        return elif_branch_handle(self, **kwargs)

    def else_branch(self, **kwargs):
        return else_branch_handle(self, **kwargs)

    def foreach_branch(self, **kwargs):
        return True

    """ ------------------------------------------------------------
        ------------------------------------------------------------
        --------------------用户操作行为相关关键字----------------------
        --------判断是否为新窗口、打开新标签页并进入、切换句柄至新窗口-------
        -----遍历一组元素点击、关闭弹出框、点击元素并跳转新窗口、变量处理-----
        ------------------------------------------------------------ """

    def is_new_window(self, oldAllwindows, newAllwindows):
        """
        判断是否为新窗口
        oldAllwindows: 必填项，列表类型，原所有窗口句柄
        newAllwindows: 必填项，列表类型，现所有窗口句柄
        return: 如果存在新窗口，则返回新窗口，否则返回False
        """
        if len(oldAllwindows) != newAllwindows:
            for window in newAllwindows:
                if window not in oldAllwindows:
                    new_window = window
                    return new_window
        else:
            return False

    def open_new_window(self, **kwargs):
        """打开新的标签页并将句柄切换过去"""
        old_headles = self.acquire_all_handles()
        self.exec_script("window.open('','_blank');")
        new_headles = self.acquire_all_handles()
        new_window = self.is_new_window(old_headles, new_headles)
        self.switch_to_window(new_window)
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def switch_to_new_window(self, **kwargs):
        """将句柄切换至新窗口"""
        old_headles = self.acquire_current_handles()
        new_headles = self.acquire_all_handles()
        index = new_headles.index(old_headles)
        self.switch_to_window(new_headles[index + 1])
        log.info(f'webdriver：跳转至倒数第{index+1}个窗口成功!')
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def foreach_element_click(self, **kwargs):
        """
        定位一组元素对象并遍历，根据条件点击元素对象
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        params: 必填项，字符类型，默认为None，需要点击的元素索引，格式如1,2,3...
        return: 如果params为None则点击每一个，否则点击params中的索引，执行完毕后截图返回路径
        """
        method = kwargs['method']
        value = kwargs['value']
        params = kwargs['params'] if 'params' in kwargs.keys() else None
        elements = self.locator_more_element(method=method, value=value)
        for index, element in enumerate(elements):
            if params == None:
                element.click()
            else:
                # text.split(',') ['1','2','3'...]
                if str(index) in params.split(','):
                    element.click()
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def close_alert(self, **kwargs):
        """
        关闭弹出框：如果是alert、confirm警告弹出框就直接点击确认，
        如果是prompt交互弹出框则判断是否需要填值，如果无值可填便取消；
        method: 非必填，字符类型，默认为alert，弹出框的类型
        params: 非必填，字符类型，默认为None，prompt弹出框是否需要输入文本
        return: 作用于各类弹出框，关闭后返回True
        """
        method = kwargs['method'] if 'method' in kwargs.keys() else 'alert'
        params = kwargs['params'] if 'params' in kwargs.keys() else None
        try:
            WebDriverWait(driver=self.driver, timeout=10).until(EC.alert_is_present())
            if method in ['alert', 'confirm']:
                self.driver.switch_to.alert.accept()
            elif method == 'prompt':
                if params:
                    self.driver.switch_to.alert.send_keys(params)
                    self.driver.switch_to.alert.accept()
                else:
                    self.driver.switch_to.alert.dismiss()
            else:
                log.info(f'webdriver：请确认弹框的类型，暂不支持{method}类型!')
            log.info(f'webdriver：关闭{method}类型的弹框成功!')
        except Exception as e:
            log.info(f'webdriver：关闭{method}类型的弹框失败!')
            return False
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def click_and_jump(self, **kwargs):
        """
        点击元素对象并跳转至新窗口
        method: 必填项，字符类型，元素定位方法
        value:  必填项，字符类型，元素定位路径
        return: 点击后出现新窗口，将句柄切换过去，返回True
        """
        method = kwargs['method']
        value = kwargs['value']
        old_handles = self.acquire_all_handles()  # 获取点击之前的所有窗口句柄
        self.click_element(method=method, value=value)
        # 判断新窗口是否打开
        WebDriverWait(self.driver, timeout=10, ).until(EC.new_window_is_opened(old_handles))
        new_handles = self.acquire_all_handles()  # 再次获取所有窗口的句柄
        self.switch_to_window(new_handles[-1])
        log.info(f'webdriver：以[{method}]方式定位[{value}]元素成功，执行点击并跳转至新窗口!')
        save_path = self.step_high_light_screenshot(**kwargs)
        return save_path

    def variable_create(self, **kwargs):
        """
        创建变量、变量声明，储存于global_variable_list字典中（程序意义上存在）
        params: 必填项，常规类型，变量值
        expect: 必填项，字符类型，变量名
        return: 如变量名已存在则返回Fasle（如需重新赋值有其他方法），否则返回True
        """
        params = kwargs['params']
        expect = kwargs['expect']
        if expect in self.global_variable_list.keys():
            log.info(f'webdriver：变量名[{str(expect)}]已存在，无法继续创建!')
            return False
        else:
            self.global_variable_list[str(expect)] = params
            log.info(f'webdriver：创建[{str(expect)}]变量成功，结果为[%{str(expect)}%={params}]!')
            return True

    def acquire_variable_name(self, **kwargs):
        """获取所有变量名,以变量名=变量值的形式展示"""
        variable = ''
        for k, v in self.global_variable_list.items():
            variable += f"%{k}%={v},"
        if variable.endswith(','):
            variable = variable[:-1]
        log.info(f'webdriver：查看所有的变量，结果为[{variable}]!')
        return variable

    def acquire_variable_handle_result(self, **kwargs):
        # 保留原来的key，用于得出新结果时覆盖原变量
        variable_key = "params" in kwargs and kwargs["params"] or ""
        # 此时的kwargs["params"]就是字典中的key值，通过此key值可以获取对应的变量数据
        if str(variable_key).startswith('$') and str(variable_key).endswith('$'):
            variable_key = kwargs['params'][1:-1]
        else:
            variable_key = kwargs['params']
        # 如果获取到key值则表明需要变量处理
        if variable_key:
            # 将本次需要处理的变量从数据字典中取出来，赋值给本次参数字典，kwargs['params']由key变成了value
            kwargs['params'] = self.global_variable_list[variable_key]
            kwargs['key'] = variable_key
        # 调用变量处理方法
        variable = variable_handle(**kwargs)
        # 将返回的处理结果绑定于当前key，完成更新数据
        self.global_variable_list[variable_key] = variable
        return variable
