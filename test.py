from time import sleep

from selenium import webdriver


def HighLight(driver, element):
    for i in range(0,2):
        driver.execute_script("arguments[0].setAttribute('style',arguments[1]);",
                              element, "background: pink; border:5px solid red;")
        sleep(0.2)
        driver.execute_script("arguments[0].setAttribute('style',arguments[1]);", element, "")
        sleep(0.1)



driver = webdriver.Chrome()
driver.implicitly_wait(10)
driver.maximize_window()
driver.get("https://www.baidu.com/")
input_search = driver.find_element('id','kw')
HighLight(driver, input_search)
input_search.send_keys('百度一下')

sleep(3)
btn_go = driver.find_element('id','su')
HighLight(driver, btn_go)
btn_go.click()


sleep(5)
driver.quit()