import random
import time
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

while 1:
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')  # 给设置 的属性添加headless属性，使浏览器隐藏起来，不弹出。

    # 调用环境变量创建浏览器对象
    driver = webdriver.Chrome('/Crawl/Industry/chromedriver.exe', options=chrome_options)

    # get方法会一直等到页面加载，然后才会继续程序，通常测试会在这里选择
    driver.get('https://www.jianchacha.com/')

    time.sleep(5)
    driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[7]/div/div/div[2]/i').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="__layout"]/div/div[2]/div[2]/div[1]/div[2]/button').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="tab-password"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="pane-password"]/form/div[1]/div/div/input').send_keys('13271317256')
    driver.find_element_by_xpath('//*[@id="pane-password"]/form/div[2]/div/div/input').send_keys('zqy521314')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="captchaPass"]/div/div[3]/span[2]').click()
    time.sleep(2)
    slideblock = driver.find_element_by_xpath('//*[@id="JianCC"]/div[5]/div[2]/div[1]/div/div[1]/div[2]/div[2]')
    # 鼠标点击圆球不松开
    ActionChains(driver).click_and_hold(slideblock).perform()
    # 将圆球滑至相对起点位置的最右边
    ActionChains(driver).move_by_offset(xoffset=195, yoffset=0).perform()
    # 截取全屏
    driver.get_screenshot_as_file('G:\Pycharm\Demo\Crawl\company\qp.jpg')
    element = driver.find_element_by_xpath(
        '//*[@id="JianCC"]/div[5]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]')  # 百度一下的按钮
    print("获取元素坐标：")
    location = element.location
    print(location)
    print("获取元素大小：")
    size = element.size
    print(size)
    # 计算出元素上、下、左、右 位置
    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']
    im = Image.open('/Crawl/company/qp.jpg')
    im = im.crop((left, top, right, bottom))
    im.save('G:\Pycharm\Demo\Crawl\company\jt.png')
    # 放开圆球
    ActionChains(driver).release(slideblock).perform()


    def match_source(image):
        # imagea = Image.open(r'G:\Pycharm\Demo\Crawl\company\1.png')
        imageb = Image.open(r'/Crawl/company/2.png')
        # imagec = Image.open(r'G:\Pycharm\Demo\Crawl\company\3.png')
        imaged = Image.open(r'/Crawl/company/4.png')
        imagee = Image.open(r'/Crawl/company/5.png')
        imagef = Image.open(r'/Crawl/company/6.png')
        list = [imageb, imaged, imagee, imagef]
        # 通过像素差遍历匹配本地原图
        for i in list:
            # 本人电脑原图与缺口图对应滑块图片横坐标相同，纵坐标原图比缺口图大88px，可根据实际情况修改
            pixel1 = image.getpixel((0, 0))
            pixel2 = i.getpixel((0, 0))
            # pixel[0]代表R值，pixel[1]代表G值，pixel[2]代表B值
            if abs(pixel1[0] - pixel2[0]) < 5:
                return i
        return image


    quekouimg = Image.open(r'/Crawl/company/jt.png')
    # 匹配本地对应原图
    sourceimg = match_source(quekouimg)
    if sourceimg == quekouimg:
        driver.close()
        continue


    # 计算滑块位移距离
    def get_diff_location(image1, image2):
        # （825,1082）（335,463）为滑块图片区域，可根据实际情况修改
        for i in range(255):
            for j in range(55, 155):
                # 遍历原图与缺口图像素值寻找缺口位置
                if is_similar(image1, image2, i, j) == False:
                    if i > 32:
                        return i
        return -1


    # 对比RGB值得到缺口位置
    def is_similar(image1, image2, x, y):
        pixel1 = image1.getpixel((x, y))
        pixel2 = image2.getpixel((x, y))
        # 截图像素也许存在误差，50作为容差范围
        # if abs(pixel1[0] - pixel2[0]) >= 50 and abs(pixel1[1] - pixel2[1]) >= 50 and abs(pixel1[2] - pixel2[2]) >= 50:
        #     return False
        if pixel2[0] >= 50 and pixel2[0] <= 80:
            return False
        return True


    # 获取缺口位置
    visualstack = get_diff_location(sourceimg, quekouimg) - 7
    # 获取移动距离loc，827为滑块起点位置
    time.sleep(3)
    ActionChains(driver).click_and_hold(slideblock).perform()


    def get_track(distance):
        track = []
        current = 0
        mid = distance * 3 / 4
        t = random.randint(2, 3) / 10
        v = 0
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track


    # 生成拖拽移动轨迹，加3是为了模拟滑过缺口位置后返回缺口的情况
    track_list = get_track(visualstack + 3)
    time.sleep(2)
    ActionChains(driver).click_and_hold(slideblock).perform()
    time.sleep(0.2)
    # 根据轨迹拖拽圆球
    for track in track_list:
        ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
    # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
    imitate = ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
    time.sleep(0.015)
    imitate.perform()
    time.sleep(random.randint(6, 10) / 10)
    imitate.perform()
    time.sleep(0.04)
    imitate.perform()
    time.sleep(0.012)
    imitate.perform()
    time.sleep(0.019)
    imitate.perform()
    time.sleep(0.033)
    ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
    # 放开圆球
    ActionChains(driver).pause(random.randint(6, 14) / 10).release(slideblock).perform()
    time.sleep(2)
    # 务必记得加入quit()或close()结束进程，不断测试电脑只会卡卡西
    driver.close()
