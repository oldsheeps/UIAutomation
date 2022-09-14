from base.WebCommand import *
from factory.BranchFactory import *


class cached_class_property(object):
    """
        自定义动态缓存注入装饰器，作用于selenium webdriver类无限实例化控制成单例
    """

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


class Drivers(Command):
    """
        基于Selenium Web自动化工具进行二次封装的自动化工具；
        它支持无限实例化webdriver类，但仍可以保持统一浏览器对象；
        它支持使用自定义的方法、它非继承但又支持所有基类定义的方法；
    """

    def __init__(self, browser_name=None):
        """
        浏览器对象默认构造函数，默认启动浏览器名称为谷歌；
        :param driver_name: 浏览器名字、数字或者字母
        """
        self.browser_name = '谷歌' if browser_name == None else browser_name
        super().__init__(self.driver)  # 将本类的driver实例传递给父类使用

    @cached_class_property
    def driver(self):
        """
        将缓存装饰器注入进来，确保唯一实例时利用branch工厂创建对应的浏览器对象;
        注意：方法名称必须使用driver，其用意为了后续使用getattr能够直接映射到webdriver类
        :return: selenium webdriver对象
        """
        log.info(f'webdriver：启动浏览器[{self.browser_name}] --> 成功!')
        return branch(self.browser_name)

    def __getattr__(self, item):
        """
        想把其他webdriver的方法添加进来，又不想一个一个方法的写出来，不想一直搞冗余的代码。
        python会优先使用__getattribute__调用自定义方法，查不到才会调用__getsttr__方法，如果再查不到则会抛出AttributeError；
        利用这个特性，来实现将原生driver的属性添加到该类。
        :param item: 即将被调用的方法名
        :return: 利用getattr带入webdriver的实例对象访问某方法
        """
        log.info('webdriver: --> 映射 --> ' + item)

        return getattr(self.driver, item)


if __name__ == '__main__':
    driver = Drivers()
    driver.get(r'http://www.baidu.com/')
    # driver.input_element('id', 'kw', 'hhhhh')
    # click = driver.find_element('id', 'su')
    # click.click()
    # driver.sleep_wait(2)
    # driver.screenshot_save('test_1.png', False)
    # driver.screenshot_save('test_22222.png')
