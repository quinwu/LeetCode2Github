import json
import requests
from src.utils import Config
BASE_URL = 'https://leetcode.com'

# class Question:
#     def __init__(self,num):
#         self.num = num
#         self.info = self._get_info(num)
#         self.solutions = []
#
#     def _get_info(self,num):
#         # all question information
#         content = requests.get(Config.leetcode_api).content
#         questions = json.loads(content)['stat_status_pairs']
#
#         difficultys = ['Easy','Medium','Hard']
#
#         for i in range(len(questions) -1 ,-1, -1):
#             question = questions[i]
#             # soltions = {}
#             if question['stat']['frontend_question_id'] == num:
#                 title = question['stat']['question__title']
#                 url = Config.leetcode_url + 'problems/' +question['stat']['question__title_slug']
#                 difficult = difficultys[question['difficulty']['level'] - 1]
#                 break
#
#         return {
#             'title':title,
#             'url':url,
#             'difficult':difficult,
#         }

class Quiz:
    base_url = BASE_URL

    def __init__(self,**data):
        self.__dict__.update(data)
        self.solutionis = []

    def __str__(self):
        return '<Quiz: {question_id}-{question__title_slug}({difficulty})-{is_pass}>'.format(
            question_id=self.question_id,
            question__title_slug=self.question__title_slug,
            difficulty=self.difficulty,
            is_pass=self.is_pass,
        )

    def __repr__(self):
        return self.__str__()

    @property
    def json_object(self):
        addition_proporties = [
            'is_pass',
            'difficulty',
            'url',
            'title'
        ]
        dct = self.__dict__
        for prop in addition_proporties:
            dct[prop] = getattr(self,prop)
        return dct

    @property
    def is_pass(self):
        return True if self.status == 'ac' else False

    @property
    def difficulty(self):
        difficulty = {1:"Easy",2:"Medium",3:"Hard"}
        return difficulty[self.level]

    @property
    def url(self):
        return '{base_url}/problems/{question_title_slug}'.format(
            base_url = self.base_url,
            question_title_slug = self.question_title_slug,
        )

    @property
    def title(self):
        return self.question_title