import os
import configparser
import re
from collections import namedtuple

HOME = os.getcwd()
CONFIG_FILE = os.path.join(HOME, 'config','config.cfg')
COOKIE_PATH = os.path.join(HOME,'config','cookies.json')

BASE_URL = 'https://leetcode.com'
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

ProgLang = namedtuple('ProgLang', ['language', 'ext', 'annotation'])
ProgLangList = [
    ProgLang('cpp', 'cpp', '//'),
    ProgLang('java', 'java', '//'),
    ProgLang('python', 'py', '#'),
    ProgLang('python3', 'py', '#'),
    ProgLang('c', 'c', '//'),
    ProgLang('csharp', 'cs', '//'),
    ProgLang('javascript', 'js', '//'),
    ProgLang('ruby', 'rb', '#'),
    ProgLang('kotlin', 'kt', '//'),
    ProgLang('swift', 'swift', '//'),
    ProgLang('golang', 'go', '//'),
]
ProgLangDict = dict((item.language, item) for item in ProgLangList)

def check_and_make_dir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def check_and_make_file(path):
    if not os.path.isfile(path):
        open(path,'w').close()

def get_config_from_file(CONFIG_FILE):
    cp = configparser.ConfigParser()
    cp.read(CONFIG_FILE)

    if 'leetcode' not in cp.sections():
        raise Exception('Please create config.cfg first.')

    username = cp.get('leetcode','username')

    if os.getenv('leetcode_username'):
        username = os.getenv('leetcode_username')

    password = cp.get('leetcode', 'password')

    if os.getenv('leetcode_password'):
        password = os.getenv('leetcode_password')

    if not username or not password:
        raise Exception(
            'Please input your username and password in config.cfg'
        )

    language = cp.get('leetcode','language')
    if not language:
        language = 'python3' # default language python

    driverpath = cp.get('leetcode','driverpath')

    local_path = cp.get('leetcode', 'local_path')
    if not local_path:
        raise Exception('Please input your local path')

    config = dict(
        username=username,
        password=password,
        language=language.lower(),
        driverpath=driverpath,
        local_path=local_path,
    )
    return config

def rep_unicode_in_code(code):
    pattern = re.compile('(\\\\u[0-9a-zA-Z]{4})')
    m = pattern.findall(code)
    for item in set(m):
        code = code.replace(item, chr(int(item[2:], 16)))
    return code