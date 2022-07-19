# import logging

from selenium import webdriver

from base.OptionsWrapper import ChromeOptions
from common.LogWrapper import log


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
    1、基于selenium的二次封装，
    2、支持无限实例化此类，仍然保持使用同一个浏览器窗口。
    3、支持使用自定义的方法名字，同时直接性的支持使用所有此类中没有定义的方法，但在官方类中有的api方法，比如直接支持DriverWrapper().execute_script(script, *args)这种写法。
    4、其余想自定义名称的方法可以在这个类下面接着写或者继承这个类再添加其他更多方法
    """

    def __init__(self, browser_name=None):
        """
        :param driver_name: 浏览器名字、数字或者字母
        """
        self.browser_name = '谷歌' if browser_name == None else browser_name

    @cached_class_property
    def browser_driver(self):
        """
        将缓存装饰器注入进来，确保唯一实例时创建对应的浏览器对象
        :return: 浏览器对象
        """
        driver = None
        name = str(self.browser_name).lower() if not str(self.browser_name).isdigit() else self.browser_name
        if name in ['chrome', '谷歌', 1]:
            driver = webdriver.Chrome(options=ChromeOptions().conf_options())
            log.info('启动浏览器 --> Chrome')

        elif name in ['firefox', '火狐', 2]:
            driver = webdriver.Firefox()
            log.info('启动浏览器 --> Firefox')

        elif name in ["ie", 3]:
            driver = webdriver.Ie()
            log.info('启动浏览器 --> IE')

        elif name in ["edge", 4]:
            driver = webdriver.Edge()
            log.info('启动浏览器 --> Edge')

        else:
            print("\033[31m未找到您的浏览器配置，请使用其他浏览器...\033[0m'")
            log.info('启动浏览器 --> 失败')
        return driver

    def __getattr__(self, item):
        """
        想把其他的webdriver的操作方法直接添加进来，不一个一个的再写一个方法然后调用driver属性的方法，不想一直搞冗余的代码，可以这么做。
        python先使用__getattribute__，查不到才会调用__getsttr__方法，利用这个特性，来实现这个添加driver的属性到自己类里面。
        :param item: 属性名
        :return: 调用item属性
        """
        # print('item',item)
        # log.info('功能调用 --> 映射 --> ' + item)


        return getattr(self.browser_driver, item)


if __name__ == '__main__':
    driver_wrapper = BrowserWrapper()
    driver_wrapper.get('https://www.baidu.com')
