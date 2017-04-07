# encoding=utf-8

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from yumdama import identify

reload(sys)
sys.setdefaultencoding('utf8')
IDENTIFY = 1  # 验证码输入方式:        1:看截图aa.png，手动输入     2:云打码
dcap = dict(DesiredCapabilities.PHANTOMJS)  # PhantomJS需要使用老版手机的user-agent，不然验证码会无法通过
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
)
logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING，太烦人


"""
输入你的微博账号和密码，可去淘宝买。
建议买几十个，微博限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myWeiBo = [
    {'no': 'jiadieyuso3319@163.com', 'psw': 'a123456'},
    {'no': 'shudieful3618@163.com', 'psw': 'a123456'},
]


def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    loginURL = 'https://weibo.cn/login/'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        try:
            browser = webdriver.PhantomJS(desired_capabilities=dcap)
            browser.get(loginURL)
            time.sleep(1)

            failure = 0
            while "微博" in browser.title and failure < 5:
                failure += 1
                browser.save_screenshot("aa.png")
                username = browser.find_element_by_name("mobile")
                username.clear()
                username.send_keys(account)

                psd = browser.find_element_by_xpath('//input[@type="password"]')
                psd.clear()
                psd.send_keys(password)
                try:
                    code = browser.find_element_by_name("code")
                    code.clear()
                    if IDENTIFY == 1:
                        code_txt = raw_input("请查看路径下新生成的aa.png，然后输入验证码:")  # 手动输入验证码
                    else:
                        from PIL import Image
                        img = browser.find_element_by_xpath('//form[@method="post"]/div/img[@alt="请打开图片显示"]')
                        x = img.location["x"]
                        y = img.location["y"]
                        im = Image.open("aa.png")
                        im.crop((x, y, 100 + x, y + 22)).save("ab.png")  # 剪切出验证码
                        code_txt = identify()  # 验证码打码平台识别
                    code.send_keys(code_txt)
                except Exception, e:
                    pass

                commit = browser.find_element_by_name("submit")
                commit.click()
                time.sleep(3)
                if "我的首页" not in browser.title:
                    time.sleep(4)
                if '未激活微博' in browser.page_source:
                    print '账号未开通微博'
                    return {}

            cookie = {}
            if "我的首页" in browser.title:
                for elem in browser.get_cookies():
                    cookie[elem["name"]] = elem["value"]
                if len(cookie) > 0:
                    logger.warning("Get Cookie Successful: %s" % account)
                    cookies.append(cookie)
                    continue
            logger.warning("Get Cookie Failed: %s!" % account)
        except Exception, e:
            logger.warning("Failed %s!" % account)
        finally:
            try:
                browser.quit()
            except Exception, e:
                pass
    return cookies


cookies = getCookies(myWeiBo)
logger.warning("Get Cookies Finish!( Num:%d)" % len(cookies))
