import json
import requests
from src.utils import Config
BASE_URL = 'https://leetcode.com'

class Quiz:
    base_url = BASE_URL

    def __init__(self,**data):
        self.__dict__.update(data)
        self.solutions = []

    def __str__(self):
        return '<Quiz: {question_id}-{question__title_slug}({difficulty})-{is_pass}>'.format(
            question_id=self.question_id,
            question__title_slug=self.question_title_slug,
            difficulty=self.difficulty,
            is_pass=self.is_pass,
        )

    def __repr__(self):
        return self.__str__()

    @property
    def json_object(self):
        addition_proporties = [
            'is_pass',
            'id',
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
    def id(self):
        return self.question_id

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