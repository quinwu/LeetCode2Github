import re
import os
import time
from src.utils import check_and_make_file,check_and_make_dir
from src.utils import Config

PREFIX_NUMBER = 9
BASE_URL = 'https://leetcode.com'


class Readme:
    def __init__(self,LOCAL_PATH):
        self.file = os.path.join(LOCAL_PATH,'README.md')
        if not self.is_exit:
            self._init_readme_head()
        self.content = self._read_file()

    def _init_readme_head(self,num_solved=0,num_total=742):

        md = '''#  Leetcode solutions
Update time:  {tm} 

Auto Updated by [LeetCode2Github](https://github.com/quinwu/LeetCode2Github)

I have solved **{num_solved}   /   {num_total}** problems

|NO.|Title|Solutions|Note|Difficulty|
|:---:|:---:|:---:|:---:|:---:|'''.format(
            tm=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            num_solved=num_solved,
            num_total=num_total,
        )
        check_and_make_file(self.file)
        self._write_file(md)

    @property
    def is_exit(self):
        return os.path.isfile(self.file)

    def _read_file(self):
        with open(self.file,'r') as fd:
            content = fd.readlines()
            fd.close()
        return content

    def _write_file(self,content):
        with open(self.file,'w') as fd:
            fd.writelines(content)
            fd.close()


    def _find_position(self,lists,num):
        re_id = re.compile(r"\|\d+\|")
        sort_nums = []
        sort_nums.append(num)
        for str in lists:
            id = re_id.match(str).group(0)[1:-1]
            sort_nums.append(int(id))
        sort_nums.sort()
        return sort_nums.index(num) + PREFIX_NUMBER

    def add_question(self,quiz):

        solutions = ''
        dirname = '{id}.%20{title}'.format(
            id=quiz.id,
            title=quiz.title.replace(' ','%20')
        )
        print (dirname)

        print (quiz.solutions)

        # row = '|{id}|[{title}]({url})|{solutions}|{note}|{difficulty}|\n'.format(
        #         id= quiz.id,
        #         title= quiz.title,
        #         url = quiz.url,
        #         solutions = solutions,
        #         note='None',
        #         difficulty = quiz.difficulty,
        #     )
        # sort_content = self.content[PREFIX_NUMBER:]
        # pos = self._find_position(sort_content,quiz)
        # self.content.insert(pos,row)

    def write_readme(self,content):
        self._write_file(content)
