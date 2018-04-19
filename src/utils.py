import os
from collections import namedtuple

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


# if __name__ == '__main__':
#     for prolang in ProgLangList:
#         print (prolang.language,prolang.ext,prolang.annotation)