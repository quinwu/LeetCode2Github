import json
import requests
from src.utils import Config

class Question:
    def __init__(self,num):
        self.num = num
        self.info = self._get_info(num)
        self.solutions = []

    def _get_info(self,num):
        # all question information
        content = requests.get(Config.leetcode_api).content
        questions = json.loads(content)['stat_status_pairs']

        difficultys = ['Easy','Medium','Hard']

        for i in range(len(questions) -1 ,-1, -1):
            question = questions[i]
            # soltions = {}
            if question['stat']['frontend_question_id'] == num:
                title = question['stat']['question__title']
                url = Config.leetcode_url + 'problems/' +question['stat']['question__title_slug']
                difficult = difficultys[question['difficulty']['level'] - 1]
                break

        return {
            'title':title,
            'url':url,
            'difficult':difficult,
        }