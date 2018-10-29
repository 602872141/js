# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from logging import getLogger
import string
import zipfile






class seleniumMiddleware(object):

    def __init__(self):
        # self.proxyHost = "http-dyn.abuyun.com"
        # self.proxyPort = "9020"
        #
        # # 代理隧道验证信息
        # self.proxyUser = "H01234567890123D"
        # self.proxyPass = "0123456789012345"
        # self.proxy_auth_plugin_path = self.create_proxy_auth_extension(
        #     proxy_host=self.proxyHost,
        #     proxy_port=self.proxyPort,
        #     proxy_username=self.proxyUser,
        #     proxy_password=self.proxyPass)
        self.chrome_options = Options()
        # self.chrome_options.add_argument("--start-maximized")
        # self.chrome_options.add_extension(self.proxy_auth_plugin_path)

        self.chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        self.chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        self.chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        self.chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        # chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        self.timeout= 10

        self.browser = webdriver.Chrome(chrome_options=self.chrome_options, )

        self.wait = WebDriverWait(self.browser, self.timeout)
        # self.browser = webdriver.Firefox()


    def process_request(self, request, spider):
        try:
            # print("***********1************")
            # print(request.meta['key'])
            # print("***********1************")

            self.browser.get(request.url)
            if self.isElementExist('//*[contains(@class,"radio-center")]/input'):
                input =  self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[contains(@class,"radio-center")]/input')))
                input.click()
                try:
                    if self.isElementExist('//*[contains(@class,"choose-ticket-row-action")]/a'):
                        submit =  self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, '//*[contains(@class,"choose-ticket-row-action")]/a')))
                        submit.click()
                        ww =  self.wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[contains(@class,"choose-ticket-prices-more-row  f-clear")]//input')))
                        ww.click()
                except TimeoutException:
                    return  HtmlResponse(url=request.url,body=self.browser.page_source,request=request,encoding='utf-8',status=200)
            # print(browser.page_source)

        except TimeoutException:
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)

        return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                            status=200)
    def isElementExist(self,element):
            try:
                WebDriverWait(self.browser, 2).until(
                    EC.element_to_be_clickable((By.XPATH, element)))
                print(True)
                return True
            except:
                print(False)
                return False

        # return HtmlResponse(url=request.url,body="",request=request,encoding='utf-8',status=200)
    # def create_proxy_auth_extension(self,proxy_host, proxy_port,
    #                                 proxy_username, proxy_password,
    #                                 scheme='http', plugin_path=None):
    #     if plugin_path is None:
    #         plugin_path = r'D:/{}_{}@http-dyn.abuyun.com_9020.zip'.format(proxy_username, proxy_password)
    #
    #     manifest_json = """
    #           {
    #               "version": "1.0.0",
    #               "manifest_version": 2,
    #               "name": "Abuyun Proxy",
    #               "permissions": [
    #                   "proxy",
    #                   "tabs",
    #                   "unlimitedStorage",
    #                   "storage",
    #                   "<all_urls>",
    #                   "webRequest",
    #                   "webRequestBlocking"
    #               ],
    #               "background": {
    #                   "scripts": ["background.js"]
    #               },
    #               "minimum_chrome_version":"22.0.0"
    #           }
    #           """
    #
    #     background_js = string.Template(
    #         """
    #         var config = {
    #             mode: "fixed_servers",
    #             rules: {
    #                 singleProxy: {
    #                     scheme: "${scheme}",
    #                     host: "${host}",
    #                     port: parseInt(${port})
    #                 },
    #                 bypassList: ["foobar.com"]
    #             }
    #           };
    #
    #         chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    #
    #         function callbackFn(details) {
    #             return {
    #                 authCredentials: {
    #                     username: "${username}",
    #                     password: "${password}"
    #                 }
    #             };
    #         }
    #
    #         chrome.webRequest.onAuthRequired.addListener(
    #             callbackFn,
    #             {urls: ["<all_urls>"]},
    #             ['blocking']
    #         );
    #         """
    #     ).substitute(
    #         host=proxy_host,
    #         port=proxy_port,
    #         username=proxy_username,
    #         password=proxy_password,
    #         scheme=scheme,
    #     )
    #
    #     with zipfile.ZipFile(plugin_path, 'w') as zp:
    #         zp.writestr("manifest.json", manifest_json)
    #         zp.writestr("background.js", background_js)
    #
    #     return plugin_path

    def __del__(self):
        self.browser.close()
class testMiddleware(object):

    def process_request(self, request, spider):
        print("***********2***********")
        print(request.meta['key'])
        print("***********2************")

