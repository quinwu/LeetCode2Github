import os
import configparser
from collections import namedtuple
import re

ProgLang = namedtuple('ProLong',['language','ext','annotation'])
ProgLangList = [
    ProgLang('cpp','cpp','//'),
    ProgLang('python3','py','#'),
    ProgLang('python','py','#')
]

class Config:
    # local_path = 'C:/Users/Administrator/Desktop/git-project/LeetCode'
    local_path = 'C:/Users/Administrator/Desktop/git-project/LeetCode2Github/src'
    github_leetcode_path = 'https://github.com/quinwu/LeetCode2Github'
    leetcode_url = 'https://leetcode.com/'
    leetcode_api = 'https://leetcode.com/api/problems/algorithms/'
    pattern_re = r"\|\d+\|"
    number_of_prefix = 5


def check_and_make_dir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def check_and_make_file(path):
    if not os.path.isfile(path):
        open(path,'w').close()


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


def get_config_from_file(CONFIG_FILE):
    cp = configparser.ConfigParser()
    cp.read(CONFIG_FILE)


    # print ('cp.sections() type:',type(cp.sections()))
    if 'leetcode' not in cp.sections():
        raise Exception('Please create config.cfg first.')

    username = cp.get('leetcode','username')
    # print (os.getenv('leetcode_username'))

    if os.getenv('leetcode_username'):
        username = os.getenv('leetcode_username')

    password = cp.get('leetcode', 'password')
    # print (os.getenv('leetcode_password'))

    if os.getenv('leetcode_password'):
        password = os.getenv('leetcode_password')

    if not username or not password:
        raise Exception(
            'Please input your username and password in config.cfg'
        )

    language = cp.get('leetcode','language')
    if not language:
        language = 'python' # default language python

    repo = cp.get('leetcode','repo')
    if not repo:
        raise Exception('Please input your Github repo address')

    driverpath = cp.get('leetcode','driverpath')

    config = dict(
        username=username,
        password=password,
        language=language.lower(),
        repo=repo,
        driverpath=driverpath,
    )
    return config

def rep_unicode_in_code(code):
    pattern = re.compile('(\\\\u[0-9a-zA-Z]{4})')
    m = pattern.findall(code)
    for item in set(m):
        code = code.replace(item, chr(int(item[2:], 16)))
    return code