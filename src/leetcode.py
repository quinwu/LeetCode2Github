import requests
import os
import time
import json
from selenium import webdriver

COOKIE_PATH = 'cookies.json'
BASE_URL = 'https://leetcode.com'
# If you have proxy, change PROXIES below
PROXIES = None
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'leetcode.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36',  # NOQA
}


class Leetcode:
    def __int__(self,questions,CONFIG):
        self.questions = questions
        self.session = requests.session()
        self.session.headers.update(HEADERS)
        self.session.proxies = PROXIES
        self.session.cookies = None
        self.base_url = BASE_URL
        self.config = CONFIG

    def login(self):
        LOGIN_URL = self.base_url + '/accounts/login/'
        if not self.config['username'] or not self.config['password']:
            raise Exception(
                'Leetcode - Please input your username and password in config.cfg.'
            )

        usr = self.config['username']
        passwd = self.config['password']

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        executable_path = self.config.get('driverpath')
        driver = webdriver.Chrome(
            chrome_options=options,executable_path=executable_path
        )
        driver.get(LOGIN_URL)
        driver.find_element_by_id('id_login').send_keys(usr)
        driver.find_element_by_id('id_password').send_keys(passwd)
        driver.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(5)
        webdriver_cookies = driver.get_cookie()
        driver.close()

        if 'LEETCODE_SESSION' not in [
            cookie['name'] for cookie in webdriver_cookies
        ]:
            raise Exception('Please check your config or network')

        with open(COOKIE_PATH,'w') as f:
            json.dump(webdriver_cookies,f,indent=2)
        self.cookies = {
            str(cookie['name']): str(cookie['value'])
            for cookie in webdriver_cookies
        }
        self.session.cookies.update(self.cookies)


    def load_submissison(self):
        pass


    def _download_code(self):
        """
        download code by question
        :param
        :return:
        """
        pass


    def _get_code(self):
        pass

    def push_to_github(self):
        pass
