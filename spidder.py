# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import logging
logging.getLogger().setLevel(logging.INFO)


class Spidder:

    request_count = 10

    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.http', '127.0.0.1')
        profile.set_preference('network.proxy.http_port', 8080)
        profile.set_preference('network.proxy.ssl', '127.0.0.1')
        profile.set_preference('network.proxy.ssl_port', 8080)
        # profile.set_preference('network.proxy.socks', '127.0.0.1')
        # profile.set_preference('network.proxy.socks_port', 1080)
        profile.set_preference(
            "general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0")
        profile.update_preferences()
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless(False)
        self.driver = webdriver.Firefox(
            firefox_profile=profile, options=fireFoxOptions)

    def start_requests(self):
        self.driver.get('https://market.m.taobao.com/apps/market/content/index.html?ut_sk=1.Wy3W3r9w55ADAHidbZuj6sL1_21380790_1561272303791.Copy.33&wh_weex=true&contentId=229246104360&source=darenhome&data_prefetch=true&suid=834CDA17-8679-46B0-9FA0-AB5E3A1DBC06&wx_navbar_transparent=true&sourceType=other&wx_navbar_hidden=false&un=6c8d75f684aaced2e7c4cca5375f99dd&share_crt_v=1&sp_tk=77+lTzRHSllVQzhWWWLvv6U=&cpp=1&shareurl=true&spm=a313p.22.i3.1043979013407&short_name=h.egUbqzW&sm=e8a9a5&app=firefox')
        # 隐示等待，为了等待充分加载好网址
        self.driver.implicitly_wait(5)
        self.parse()

    def is_need_login(self):
        try:
            self.driver.switch_to.frame(self.driver.find_element_by_xpath(
                "//div[@class='J_MIDDLEWARE_FRAME_WIDGET']/iframe"))
            return True
        except Exception as err:
            logging.info("exception:%s", err)
            return False

    def parse(self):
        if self.is_need_login():
            try:
                logging.info("start parse")
                # self.driver.switch_to.frame(self.driver.find_element_by_xpath(
                #     "//div[@class='J_MIDDLEWARE_FRAME_WIDGET']/iframe"))
                # logger.error(driver.page_source)
                form_username = self.driver.find_element_by_xpath(
                    "//input[@id='username']")
                form_username.send_keys("xxxx")
                form_pwd = self.driver.find_element_by_xpath(
                    "//input[@id='password']")
                form_pwd.send_keys("xxxxxx")
                time.sleep(1)
                self.driver.find_element_by_xpath(
                    "//button[@id='btn-submit']").click()
                time.sleep(2)
                self.refresh()
            except Exception as err:
                logging.info("exception:%s", err)
            finally:
                time.sleep(2)
                self.driver.quit()
        else:
            self.refresh()
            self.driver.quit()

    def refresh(self):
        for i in range(0, self.request_count):
            self.driver.refresh()
            time.sleep(2)
