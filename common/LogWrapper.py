import datetime
import logging
import os
import traceback  # 回溯模块


# 通过装饰器完成单例模式
def singleton(cls):
    # 使用字典存储类对象
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            # 如果类没有被创建过，那就new个新对象并存储到字典中
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


class Log():

    def __init__(self):
        '''创建日志器'''
        self.log = logging.getLogger()
        # 设置日志信息等级
        self.log.setLevel(level='INFO')

    def console_handle(self):
        '''创建控制台处理器'''
        self.console_handler = logging.StreamHandler()
        # 设置格式器
        self.console_handler.setFormatter(self.get_formatter()[0])
        # 返回作用给日志器使用
        return self.console_handler

    def file_handle(self):
        '''创建文件处理器'''
        # 当前文件的绝对路径去除当前文件所在目录加上日志文件存放目录
        log_path = os.path.abspath(os.path.dirname(__file__)).split('common')[0] + '\logs'
        now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        fold_name = '\执行日志 ' + now_date + '.log'
        try:
            # 判断今天是否生成了日志文件
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            if not os.path.exists(log_path + fold_name):
                open(log_path + fold_name, mode='a')
        except OSError:
            pass
        self.file_handler = logging.FileHandler(filename=log_path + fold_name, mode='a', encoding='utf-8')
        # 设置格式器
        self.file_handler.setFormatter(self.get_formatter()[1])
        # 返回作用给日志器使用
        return self.file_handler

    def get_formatter(self):
        '''格式器'''
        self.console_fmt = logging.Formatter(
            fmt='%(asctime)s --> %(filename)-20s [line:%(lineno)-3d] --> %(levelname)-5s --> %(message)s')
        self.file_fmt = logging.Formatter(
            fmt='%(asctime)s --> %(filename)-20s [line:%(lineno)-3d] --> %(levelname)-5s --> %(message)s')
        # 返回作用给控制台处理器、文件处理器使用
        return self.console_fmt, self.file_fmt

    @singleton
    def get_log(self):
        '''日志器添加处理器'''
        self.log.addHandler(self.console_handle())
        self.log.addHandler(self.file_handle())
        return self.log


log = Log().get_log()

if __name__ == '__main__':
    log = Log().get_log()
    log.info('提示信息')
    log.error('错误信息')
    try:
        int('hello world')
    except ValueError as e:
        print('在此处进行异常的处理')
        # 将错误信息写入日志文件
        log.error(traceback.format_exc())
        print('1')

    print('hello world hhh')
