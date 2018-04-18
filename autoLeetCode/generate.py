import os
import json
import requests
import time
import datetime
import html
import sys
from collections import namedtuple

def check_and_make_dir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

ProgLang = namedtuple('ProLong',['language','ext','annotation'])
ProgLangList = [
    ProgLang('cpp','cpp','//'),
    ProgLang('python3','py','#'),
    ProgLang('python','py','#')
]

class Config:
    local_path = ''
    github_leetcode_path = ''
    leetcode_url = 'https://leetcode.com/problemset/all/'
    leetcode_api = 'https://leetcode.com/api/problems/algorithms/'


class Question:
    def __init__(self,num):
        self.num = num
        self.info = self._get_info(num)

    def _get_info(self,num):

        # all question information
        content = requests.get(Config.leetcode_api).content
        questions = json.loads(content)['stat_status_pairs']

        difficultys = ['Easy','Medium','Hard']

        for i in range(len(questions) -1 ,-1, -1):
            question = questions[i]
            if question['stat']['frontend_question_id'] == num:
                title = question['stat']['question__title']
                url = question['stat']['question__title_slug']
                difficult = difficultys[question['difficulty']['level'] - 1]
                break

        return {
            'title':title,
            'url':url,
            'difficult':difficult,
        }


class TableInform:
    def __init__(self):
        pass

class Readme:
    def __init__(self):
        pass


def main():
    question = Question(1)
    print (question.info)
    print (question.num)

if __name__ == '__main__':
    main()