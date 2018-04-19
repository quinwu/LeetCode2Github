import requests
import os

HOME = os.getcwd()
CONFIG_FILE = os.path.join(HOME, 'config.cfg')
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
    def __int__(self,questions):
        self.questions = questions

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
