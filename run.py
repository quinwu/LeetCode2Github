import os
from src.generate import Readme
from src.question import Question
from src.utils import Config
from src.leetcode import Leetcode
from src.utils import get_config_from_file

from collections import namedtuple

HOME = os.getcwd()
CONFIG_FILE = os.path.join(HOME, 'config','config.cfg')
COOKIE_PATH = os.path.join(HOME,'config','cookies.json')


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


def test_question():
    question = Question(12)
    print (question.info)
    print ('question:',question.num)
    readme = Readme(Config.local_path)
    readme.add_question(question)
    readme.write_readme()

def test_leetcode():
    CONFIG = get_config_from_file(CONFIG_FILE)
    # print (CONFIG)
    leetcode = Leetcode(CONFIG)
    # if not leetcode.is_login():
    #     leetcode.login()
    # leetcode.load_submissison()

if __name__ == '__main__':
    # CONFIG = get_config_from_file(CONFIG_FILE)
    # print (CONFIG)
    # print (ProgLangDict)
    test_leetcode()