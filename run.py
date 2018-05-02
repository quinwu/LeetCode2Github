from src.leetcode import Leetcode
from utils import get_config_from_file,CONFIG_FILE


def run(quizs):
    CONFIG = get_config_from_file(CONFIG_FILE)
    leetcode = Leetcode(CONFIG)
    leetcode.run(quizs)

if __name__ == '__main__':
    quizs = [771]
    run(quizs)