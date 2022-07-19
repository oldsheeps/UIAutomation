import functools


def value_dispatch(func):

    registry = {}

    @functools.wraps(func)
    def wrapper(arg0, *args, **kwargs):
        try:
            delegate = registry[arg0]
        except KeyError:
            pass
        else:
            return delegate(arg0, *args, **kwargs)
        return func(arg0, *args, **kwargs)

    def register(value):
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

@branch.register('访问')
def branch_to(some):
    return "visit_url"

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
    return "screenshot_img"

@branch.register('关闭当前标签页')
def branch_to(some):
    return "close_current_label"

@branch.register('关闭浏览器')
def branch_to(some):
    return "close_browser"

@branch.register('文本断言')
def branch_to(some):
    return "assert_text"

@branch.register('属性断言')
def branch_to(some):
    return "assert_attr"

@branch.register('强制等待')
def branch_to(some):
    return "sleep_wait"

@branch.register('进入框架')
def branch_to(some):
    return "switch_to_frame"

@branch.register('返回上层框架')
def branch_to(some):
    return "return_parent_frame"

@branch.register('返回默认框架')
def branch_to(some):
    return "return_default_content"




# 下拉框


@branch.register('滑动滚动条至底部')
def branch_to(some):
    return "slide_scroll_to_bottom"

@branch.register('打开新的标签页')
def branch_to(some):
    return "open_new_window"

@branch.register('切换至新窗口')
def branch_to(some):
    return "switch_to_new_window"


@branch.register('鼠标悬停')
def branch_to(some):
    return "hover_element"

@branch.register('获取当前URL')
def branch_to(some):
    return "acquire_url"

@branch.register('获取标题')
def branch_to(some):
    return "acquire_title"

if __name__ == '__main__':

    print(branch('测试'))
    print(branch('访问'))