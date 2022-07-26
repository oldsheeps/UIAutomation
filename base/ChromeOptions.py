from selenium import webdriver


class ChromeOptions():

    def conf_options(self):
        # 配置Chrome启动项
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')  # 设置中文
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"')  # 设置请求头

        # 使用headless无界面模式
        # options.add_argument('--headless')
        # 如果不加这个选项，无界面模式有时定位会出现问题
        # options.add_argument('--disable-gpu')

        # 浏览器窗口大小配置
        # options.add_argument('--window-size=1920,1080') # 窗口分辨率
        options.add_argument('start-maximized')  # 窗口最大化

        # 屏蔽自动化受控提示 && 开发者提示
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'load-extension'])
        # 禁用“管理员已禁用加载未打包的扩展”的消息提示
        options.add_experimental_option('useAutomationExtension', False)

        # 屏蔽'保存密码'提示框
        prefs = {}
        prefs["credentials_enable_service"] = False
        prefs["profile.password_manager_enabled"] = False
        options.add_experimental_option("prefs", prefs)

        # 隐身模式
        # options.add_argument('incognito')
        # 默认浏览器启动的坐标位置
        # options.add_argument('window-position=200,400')
        return options
