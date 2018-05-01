import os
from src.generate import Readme
from src.question import Quiz
from src.utils import Config
from src.leetcode import Leetcode
from src.utils import get_config_from_file

from collections import namedtuple

HOME = os.getcwd()
CONFIG_FILE = os.path.join(HOME, 'config','config.cfg')
COOKIE_PATH = os.path.join(HOME,'config','cookies.json')


LOCAL_PATH = '/Users/aemonwk/git-project/LeetCodeTest'

def test_question():
    question = Question(12)
    print (question.info)
    print ('question:',question.num)
    readme = Readme(Config.local_path)
    readme.add_question(question)
    readme.write_readme()

def test_leetcode():
    CONFIG = get_config_from_file(CONFIG_FILE)
    leetcode = Leetcode(CONFIG)
    leetcode.load([1,13,7])
    leetcode.download()

def test_gen():
    CONFIG = get_config_from_file(CONFIG_FILE)
    leetcode = Leetcode(CONFIG)
    leetcode.load([1])
    leetcode.README.add_question(leetcode.items[0])


if __name__ == '__main__':
    test_gen()