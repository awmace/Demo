import random
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')  # 给设置 的属性添加headless属性，使浏览器隐藏起来，不弹出。

# 调用环境变量创建浏览器对象
driver = webdriver.Chrome('G:\Pycharm\Demo\HXGG\sixct\chromedriver.exe', options=chrome_options)

# get方法会一直等到页面加载，然后才会继续程序，通常测试会在这里选择
driver.get('https://www.tianyancha.com/')
ActionChains(driver).move_by_offset(958, 290).click().perform()
time.sleep(0.3 + random.random())
driver.find_element_by_class_name('navi-btn').click()
time.sleep(0.5 + random.random())
driver.find_element_by_id('normalLogin').click()
driver.find_element_by_id('nameNormal').send_keys('13271317256')
driver.find_element_by_id('pwdNormal').send_keys('zqy521314')
time.sleep(1 + random.random())
slider = driver.find_element_by_id('nc_2_n1z')  # 滑块
ActionChains(driver).click_and_hold(slider).perform()  # 点击不松开
ActionChains(driver).move_by_offset(xoffset=326, yoffset=0).perform()
print(driver.page_source)
