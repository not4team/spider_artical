# -*- coding: utf-8 -*-
from selenium import webdriver
import time
import os
import configparser
import threading
import logging
logging.getLogger().setLevel(logging.INFO)


class Spidder(threading.Thread):

    def __init__(self, account):
        threading.Thread.__init__(self)
        self.account = account
        cur_path=os.path.dirname(os.path.realpath(__file__))
        setting_path = os.path.join(cur_path,'setting.conf')
        config=configparser.ConfigParser(allow_no_value=True)
        config.read(setting_path)
        self.target_url = config.get("market","target_url")
        self.request_count = int(config.get("market", "request_count"))
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

    def run(self):
        self.start_requests()
        
    def start_requests(self):
        self.driver.get(self.target_url)
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
                form_username.send_keys(self.account[0])
                form_pwd = self.driver.find_element_by_xpath(
                    "//input[@id='password']")
                form_pwd.send_keys(self.account[1])
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
