import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.WebDriverWrapper import BrowserWrapper
from common.LogWrapper import *


class SeleniumTools():

    def __init__(self, which_browser=None):
        self.driver = BrowserWrapper(which_browser)

    # --------------------------------------------------
    # --------------------------------------------------
    # -----------------三种等待加载方式--------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # 强制等等
    def sleep_wait(self, text):
        time.sleep(text)

    # 显示等待
    def hide_wait(self, name,value):
        hide_wait = WebDriverWait(driver=self.driver, timeout=10)
        hide_wait.until(lambda driver: driver.find_element(name,value))


    # 显示等待
    # def hide_wait(self,name,value):
    #     return WebDriverWait(driver=self.driver, timeout=10).until(lambda element:self.locator_element(name,value))

    # 隐式等待
    def implicit_wait(self, text):
        self.driver.implicitly_wait(text)

    # 执行指定Script脚本
    def exec_script(self, text,*args):
        self.driver.execute_script(text,*args)

    # 滚轮滑倒底部
    def slide_scroll_to_bottom(self):
        self.exec_script("window.scrollTo(0,document.body.scrollHeight)")


    def HighLight(self, element):
        for i in range(0, 2):
            self.exec_script("arguments[0].setAttribute('style',arguments[1]);",
                                  element, "background: pink; border:5px solid red;")
            self.sleep_wait(0.2)
            self.exec_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
            self.sleep_wait(0.2)
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------系统基础关键字--------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # 在已打开的浏览器进程中访问url网页
    def visit_url(self, text):
        log.info(f'访问[{text}]地址')
        self.driver.get(text)

    # 以name方式在当前页面中定位value元素（一个元素）
    def locator_element(self, name, value):
        try:
            log.info(f'以[{name}]方式定位[{value}]元素')
            self.hide_wait(name,value)
        except TimeoutException:
            log.error(f'找不到元素，以[{name}]方式定位[{value}]元素定位失败！')
        finally:
            element = self.driver.find_element(name, value)
            self.HighLight(element)
            return element


    # 以name方式在当前页面中定位value元素（多个元素）
    def locator_more_element(self, name, value):
        log.info(f'以[{name}]方式定位[{value}]元素')
        return self.driver.find_elements(name, value)

    # 以name方式在当前页面中定位value元素，执行输入text操作
    def input_element(self, name, value, text):
        self.locator_element(name, value).send_keys(text)
        log.info(f'以[{name}]方式定位[{value}]元素并输入[{text}]文本')

    # 以name方式在当前页面中定位value元素，执行清空操作
    def clear_element(self, name, value):
        self.locator_element(name, value).clear()

    # 以name方式在当前页面中定位value元素，执行点击操作
    def click_element(self, name, value):
        self.locator_element(name, value).click()
        log.info(f'以[{name}]方式定位[{value}]元素并点击')

    # 截图
    def screenshot_img(self, text):
        log.info(f'截图成功存放路径：[{text}]')
        return self.driver.get_screenshot_as_file(text)
        # driver.save_screenshot()
        # driver.get_screenshot_as_file()
        # driver.get_screenshot_as_png()


    # 关闭浏览器当前标签页
    def close_current_label(self):
        log.info(f'关闭当前浏览器标签页')
        self.driver.close()

    # 关闭浏览器
    def close_browser(self):
        log.info(f'退出浏览器并销毁[webdriver]对象')
        self.driver.quit()



    # --------------------------------------------------
    # --------------------------------------------------
    # ----------------文本断言和属性断言-------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # 文本断言
    def assert_text(self, name, value, expect):
        try:
            reality = self.locator_element(name, value).text
            assert expect == reality, '断言失败'
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False

    # 属性断言
    def assert_attr(self, name, value, text, expect):
        try:
            reality = self.locator_element(name, value).get_attribute(text)
            assert expect == reality, '断言失败'
            return True
        except Exception:
            log.error(traceback.format_exc())
            return False



    # --------------------------------------------------
    # --------------------------------------------------
    # -----------------获取页面文本信息--------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # 获取标签名称
    def acquire_title(self):
        return self.driver.title

    # 获取当前标签页的URL
    def acquire_url(self):
        return self.driver.current_url

    # 获取当前窗口的句柄
    def acquire_current_handles(self):
        return self.driver.current_window_handle

    # 获取所有窗口的句柄
    def acquire_all_handles(self):
        return self.driver.window_handles

    # 获取弹窗信息
    def acquire_alert(self):
        alert_info = self.driver.switch_to.alert
        alert_text = alert_info.text
        alert_info.accept()
        return alert_text





    # --------------------------------------------------
    # --------------------------------------------------
    # -----------------窗口和Frame切换--------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # 进入框架
    def switch_to_frame(self, text):
        self.driver.switch_to.frame(text)

    # 返回上一层frame框架
    def return_parent_frame(self):
        self.driver.switch_to.parent_frame()

    # 返回默认frame框架
    def return_default_content(self):
        self.driver.switch_to.default_content()

    # 切换到指定窗口
    def switch_to_window(self,text):
        self.driver.switch_to.window(text)



    # --------------------------------------------------
    # --------------------------------------------------
    # -----------------Select下拉框处理-------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # 将页面中的stuff转换成Select对象
    def switch_to_select(self, stuff):
        return Select(stuff)

    # 以index选择下拉框中的备选项
    def select_to_index(self, name, value, sid):
        return self.switch_to_select(self.locator_element(name, value)).select_by_index(sid)

    # 以text选择下拉框中的备选项
    def select_to_text(self, name, value, text):
        return self.switch_to_select(self.locator_element(name, value)).select_by_visible_text(text)

    # 以value选择下拉框中的备选项
    def select_to_value(self, name, value, value_text):
        return self.switch_to_select(self.locator_element(name, value)).select_by_value(value_text)

    # 以index取消选择下拉框中的备选项
    def deselect_to_index(self, name, value, sid):
        return self.switch_to_select(self.locator_element(name, value)).deselect_by_index(sid)

    # 以text取消选择下拉框中的备选项
    def deselect_to_text(self, name, value, text):
        return self.switch_to_select(self.locator_element(name, value)).deselect_by_visible_text(text)

    # 以value取消选择下拉框中的备选项
    def deselect_to_value(self, name, value, value_text):
        return self.switch_to_select(self.locator_element(name, value)).deselect_by_value(value_text)

    # 取消所有选择下拉框的备选项
    def deselect_to_all(self,name,value):
        return self.switch_to_select(self.locator_element(name,value)).deselect_all()

    # 获取下拉列表框所有备选项
    def pulldown_all_options(self, select_object):
        all_options = []
        if isinstance(select_object, Select):
            for item in select_object.options:
                all_options.append(item.text)
        else:
            for item in Select(select_object).options:
                all_options.append(item.text)
        return all_options

    # 获取下拉列表框最终选择项
    def pulldown_final_choice(self, select_object):
        selected_options = []
        if isinstance(select_object, Select):
            for item in select_object.all_selected_options:
                selected_options.append(item.text)
        else:
            for item in Select(select_object).all_selected_options:
                selected_options.append(item.text)
        return selected_options

    # 判断下拉列表框是否可以多选
    def pulldown_is_multiple(self, select_object):
        mark = False
        if isinstance(select_object, Select):
            mark = True if select_object.is_multiple else False
        return mark



    # --------------------------------------------------
    # --------------------------------------------------
    # ------------ActionChains鼠标键盘相关----------------
    # --------------------------------------------------
    # --------------------------------------------------
    # 鼠标悬停某元素
    def hover_element(self,name,value):
        return ActionChains(self.driver).move_to_element(self.locator_element(name,value)).perform()

    # 下拉到页面底部
    # ((JavascriptExecutor) webDriver).executeScript("window.scrollTo(0,document.body.scrollHeight)");
    # 上拉到页面顶端
    # ((JavascriptExecutor) webDriver).executeScript("window.scrollTo(document.body.scrollHeight,0)");
    # 下拉到页面1000位置
    # ((JavascriptExecutor) webDriver).executeScript("window.scrollTo(0,1000)");
    # 上拉到页面顶端 0,0位置
    # ((JavascriptExecutor) webDriver).executeScript("window.scrollTo(0,0)");






    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------用户行为关键字---------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # 判断是否为新窗口
    def is_new_window(self, oldAllwindows, newAllwindows):
        if len(oldAllwindows) != newAllwindows:
            for window in newAllwindows:
                if window not in oldAllwindows:
                    new_window = window
                    return new_window
        else:
            return False

    # 打开新的标签页并将句柄切换过去
    def open_new_window(self):
        old_headles = self.acquire_all_handles()
        self.exec_script("window.open('','_blank');")
        new_headles = self.acquire_all_handles()
        new_window = self.is_new_window(old_headles, new_headles)
        self.switch_to_window(new_window)

    # 将句柄切换至新窗口
    def switch_to_new_window(self):
        old_headles = self.acquire_current_handles()
        new_headles = self.acquire_all_handles()
        index = new_headles.index(old_headles)
        self.switch_to_window(new_headles[index+1])

    # 判断元素是否存在
    def is_element_exist(self, name, value):
        try:
            self.locator_element(name, value)
        except NoSuchElementException:
            return False
        else:
            return True


    # 遍历组内所有元素并点击
    def foreach_element_click(self,elements):
        for target in elements:
            target.click()




if __name__ == '__main__':
    st = SeleniumTools(2)
    st.visit_url('https://www.baidu.com/')
    st.input_element('id', 'kw', '虚竹')
    time.sleep(2)
    st.click_element('id', 'su')
    time.sleep(2)
    st.close_browser()
