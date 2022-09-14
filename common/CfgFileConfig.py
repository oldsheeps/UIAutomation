import configparser

from common.LoggerConfig import *


class Config(object):
    """配置文件工具类封装"""

    def __init__(self, path: str):
        self.path = path
        self.config = self._acquire_config_object(path)

    def __get__(self):
        return self.config

    # 获取配置文件读取对象
    def _acquire_config_object(self, path: str):
        config = configparser.RawConfigParser()
        if os.path.exists(path):
            config.read(filenames=path, encoding='utf-8')
            return config
        else:
            log.info(f'cfgConfig：创建cfgConfig对象失败，请检查配置文件路径[{path}]是否有误！')
            return False

    # 获取所有的section节点
    def acquire_all_section(self):
        return self.config.sections()

    # 获取指定section节点下指定option选项的value
    def acquire_section_option(self, section: str, option: str):
        return self.config.get(section, option)

    # 获取指定section节点下所有option选项的value
    def acquire_all_section_option(self, section: str):
        try:
            return self.config.items(section)
        except configparser.NoSectionError:
            log.info(f'cfgConfig：在[{self.path}]配置文件中未找到[{section}]节点!')
            log.error(traceback.format_exc())
            return False

    # 修改指定section节点下option选项的value
    def modify_section_option(self, path: str, section: str, option: str, value: str):
        try:
            self.config.set(section, option, value)
            with open(file=path, mode='w', encoding='utf-8') as f:
                self.config.write(f)
                return True
        except configparser.NoSectionError:
            log.info(f'cfgConfig：在[{self.path}]配置文件中未找到[{section}]节点!')
            log.error(traceback.format_exc())
            return False


if __name__ == '__main__':
    path = '../config/database.cfg'
    cg = Config(path)
    print('获取配置文件中所有的节点：', cg.acquire_all_section())
    print('获取配置文件中所有的节点和值：', cg.acquire_all_section_option('uat'))
    print('获取配置文件中指定的节点和值：', cg.acquire_section_option('uat', 'port'))
    print("修改指定节点的值：", cg.modify_section_option(path, 'uat', 'password', 'root123'))
