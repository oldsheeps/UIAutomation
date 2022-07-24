import functools

from base.OptionsWrapper import *


def value_dispatch(func):
    """
    规避大量if.else.分支的工厂
    利用语法糖实现相等值转换；如需要可以简单处理即可实现比较运算
    :param func:调用该装饰器的实例
    :return: 作用于调用该装饰器的实例
    """
    registry = {}

    @functools.wraps(func)  # 保留被装饰函数的原有名称和属性
    def wrapper(arg0, *args, **kwargs):
        """
        将数据作为key添加到字典
        :param arg0: 常规形参1
        :param args: 列表形参n
        :param kwargs: 字典形参n
        :return: 作用于调用该装饰器的实例
        """
        try:
            delegate = registry[arg0]
        except KeyError:
            pass
        else:
            return delegate(arg0, *args, **kwargs)
        return func(arg0, *args, **kwargs)

    # 登记数据
    def register(value):
        """
        register将所有被装饰过的实例返回值传递进来，
        wrap将所有被register装饰的实例传递进来，利用字典key不可重复的特性进行等值转换；
        :param value: 所有使用装饰器实例的返回值
        :return: 将对应的返回值作用于被装饰的函数
        """

        def wrap(func):
            if value in registry:
                raise ValueError(
                    f'@value_dispatch: there is already a handler '
                    f'registered for {value!r}'
                )
            registry[value] = func
            return func

        return wrap

    wrapper.register = register
    return wrapper


@value_dispatch
def branch(some):
    return None


@branch.register('创建浏览器对象')
def branch_to(some):
    return "open_browser"


@branch.register('等待')
def branch_to(some):
    return "sleep_wait"


@branch.register('访问')
def branch_to(some):
    return "browser_visit"


@branch.register('前进')
def branch_to(some):
    return "browser_forward"


@branch.register('后退')
def branch_to(some):
    return "browser_back"


@branch.register('刷新')
def branch_to(some):
    return "browser_refresh"


@branch.register('关闭标签页')
def branch_to(some):
    return "browser_label_close"


@branch.register('关闭浏览器')
def branch_to(some):
    return "browser_quit"


@branch.register('定位')
def branch_to(some):
    return "locator_element"


@branch.register('输入')
def branch_to(some):
    return "input_element"


@branch.register('清空')
def branch_to(some):
    return "clear_element"


@branch.register('点击')
def branch_to(some):
    return "click_element"


@branch.register('截图')
def branch_to(some):
    return "screenshot_save"


@branch.register('矩形标记')
def branch_to(some):
    return "screenshot_draw"


@branch.register('获取标题')
def branch_to(some):
    return "acquire_title"


@branch.register('获取URL')
def branch_to(some):
    return "acquire_url"


@branch.register('获取元素属性')
def branch_to(some):
    return "acquire_element_attr"


@branch.register('获取元素文本')
def branch_to(some):
    return "acquire_element_text"


@branch.register('获取一组元素文本')
def branch_to(some):
    return "acquire_elements_text"


@branch.register('文本断言')
def branch_to(some):
    return "assert_text"


@branch.register('文本断言不存在')
def branch_to(some):
    return "assert_text_reverse"


@branch.register('属性断言')
def branch_to(some):
    return "assert_attr"


@branch.register('弹框断言')
def branch_to(some):
    return "assert_alert"


@branch.register('弹框断言不存在')
def branch_to(some):
    return "assert_alert_reverse"


@branch.register('进入框架')
def branch_to(some):
    return "switch_to_frame"


@branch.register('进入窗口')
def branch_to(some):
    return "switch_to_window"


@branch.register('返回上层框架')
def branch_to(some):
    return "switch_to_parent_frame"


@branch.register('返回默认框架')
def branch_to(some):
    return "switch_to_default_content"


# 下拉框
@branch.register('下拉选择')
def branch_to(some):
    return "select_choice"


@branch.register('下拉选择取消')
def branch_to(some):
    return "select_choice_quit"


@branch.register('下拉选择取消所有')
def branch_to(some):
    return "select_choice_quit_all"


@branch.register('滑动滚动条至底部')
def branch_to(some):
    return "slide_scroll_to_bottom"


@branch.register('滑动滚动条至指定码数')
def branch_to(some):
    return "slide_scroll_to_yardage"


@branch.register('鼠标悬停')
def branch_to(some):
    return "mouse_hover"


@branch.register('鼠标双击')
def branch_to(some):
    return "mouse_double_click"


@branch.register('鼠标右击')
def branch_to(some):
    return "mouse_right_click"


@branch.register('鼠标拖拽')
def branch_to(some):
    return "mouse_drag"


@branch.register('新建标签页')
def branch_to(some):
    return "open_new_window"


@branch.register('跳转新窗口')
def branch_to(some):
    return "switch_to_new_window"


@branch.register('关闭弹框')
def branch_to(some):
    return "close_alert"


@branch.register('点击并跳转')
def branch_to(some):
    return "click_and_jump"


@branch.register('点击一组')
def branch_to(some):
    return "foreach_element_click"


@branch.register(1)
@branch.register('Chrome')
@branch.register('谷歌')
def branch_to(some):
    return webdriver.Chrome(options=ChromeOptions().conf_options())


@branch.register(2)
@branch.register('firefox')
@branch.register('火狐')
def branch_to(some):
    return webdriver.Firefox()


@branch.register(3)
@branch.register('ie')
def branch_to(some):
    return webdriver.Ie()


@branch.register(4)
@branch.register('Edge')
def branch_to(some):
    return webdriver.Edge()


if __name__ == '__main__':
    # print(branch('创建浏览器对象'))
    # print(branch('访问'))
    print(branch('谷歌'))
    # print(branch('2'))
    # print(branch('3'))
    driver = branch('谷歌')
    driver.get('http://www.baidu.com')
    driver.implicitly_wait(4)
