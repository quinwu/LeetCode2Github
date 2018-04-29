import requests
import os
import time
import json
from selenium import webdriver
from src.utils import rep_unicode_in_code
from src.question import Quiz

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

HOME = os.getcwd()
COOKIE_PATH = os.path.join(HOME,'config','cookies.json')

class Leetcode:

    def __init__(self,config):
        # self.questions = questions

        self.submissions = []

        self.session = requests.session()
        # print (type(self.session))
        self.session.headers.update(HEADERS)
        self.session.proxies = PROXIES
        self.cookies = None
        self.base_url = BASE_URL
        self.config = config


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
        webdriver_cookies = driver.get_cookies()
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

    @property
    def is_login(self):
        api_url = self.base_url + '/api/problems/algorithms/'
        if not os.path.exists(COOKIE_PATH):
            return False

        with open(COOKIE_PATH,'r') as f:
            webdriver_cookies = json.load(f)
        self.cookies = {
            str(cookie['name']) : str(cookie['value'])
            for cookie in webdriver_cookies
        }

        self.session.cookies.update(self.cookies)
        r = self.session.get(api_url,proxies = PROXIES)
        if r.status_code != 200:
            return False

        data = json.loads(r.text)
        return 'user_name' in data and data['user_name'] != ''

    def load_items_from_api(self,quizs):
        api_url = self.base_url + '/api/problems/algorithms/'
        r = self.session.get(api_url,proxies=PROXIES)

        assert r.status_code == 200

        rst = json.loads(r.text)

        if not rst['user_name']:
            raise Exception("Something wrong with your personal info.\n")

    def _generate_items_from_api(self,json_data,quizs):
        stat_staus_pairs = json_data['stat_status_pairs']
        for quiz in stat_staus_pairs:
            data = {}
            data['question_title_slug'] = quiz['stat']['question_title_slug']
            data['question_title'] = quiz['stat']['question_title']
            data['level'] = quiz['difficulty']['level']
            data['question_id'] = quiz['stat']['question_id']
            data['status'] = quiz['status']
            item = Quiz(**data)
            yield item

    def load_submission(self):
        """
        load all submissions
        :return: all submissions
        """
        limit = 20
        offset = 0

        while True:
            submissions_url = '{}/api/submissions/?format=json&limit={}&offset={}'.format(
                self.base_url, limit, offset
            )

            resp = self.session.get(submissions_url,proxies=PROXIES)
            # print (resp.status_code)

            assert resp.status_code == 200
            data = resp.json()

            if 'has_next' not in data.keys():
                raise  Exception ('Get submissions wrong ,Check network \n')

            self.submissions += data['submissions_dump']
            if data['has_next']:
                offset += limit
            else:
                break
        # print (self.submissions)

    def load(self):
        if not self.is_login:
            print ('not login')
            self.login()
        print ('has login')
        self.load_submission()
