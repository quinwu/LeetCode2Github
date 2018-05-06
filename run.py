import sys
from src.leetcode import Leetcode
from utils import get_config_from_file,CONFIG_FILE

def run(leetcode):
    quizs = [int(i) for i in sys.argv[1:]]
    print (quizs)
    print ('download problems id is: {list}'.format(list=quizs))
    leetcode.run(quizs)

if __name__ == '__main__':
    CONFIG = get_config_from_file(CONFIG_FILE)
    leetcode = Leetcode(CONFIG)
    run(leetcode)