import re
import os
import time
from utils import check_and_make_file

PREFIX_NUMBER = 9

class Readme:
    def __init__(self,LOCAL_PATH):
        self.file = os.path.join(LOCAL_PATH,'README.md')
        if not self.is_exit:
            self._init_readme_head()
        self.table_content = self._read_file()[PREFIX_NUMBER:]

    def _init_readme_head(self,num_solved=0,num_total=742):

        """

        :param num_solved:
        :param num_total:
        :return:
        """

        md = '''#  Leetcode solutions
Update time:  {tm} 

Auto Updated by [LeetCode2Github](https://github.com/quinwu/LeetCode2Github)

I have solved **{num_solved}   /   {num_total}** problems

|NO.|Title|Solutions|Note|Difficulty|
|:---:|:---:|:---:|:---:|:---:|
'''.format(
            tm=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            num_solved=num_solved,
            num_total=num_total,
        )
        check_and_make_file(self.file)
        self._write_file(md)

    def _del_row(self,row):
        self.table_content.pop(row)

    def _find_position(self,lists,num):
        re_id = re.compile(r"\|\d+\|")
        sort_nums = []
        for str in lists:
            id = re_id.match(str).group(0)[1:-1]
            sort_nums.append(int(id))
        if num not in sort_nums:
            sort_nums.append(num)
            sort_nums.sort()
            return sort_nums.index(num)
        else:
            print ('{num} problem is exit!'.format(num=num))
            index = sort_nums.index(num)
            self._del_row(index)
            return index

    def add_question(self,quiz,langs,prolangdict):

        solutions = ''
        dirname = '{id}.%20{title}'.format(
            id=str(quiz.id).zfill(3),
            title=quiz.title.replace(' ','%20')
        )

        lang_lst = [
            lang['lang']
            for lang in quiz.solutions
            if lang['lang'] in langs
        ]

        for lang in lang_lst:
            solutions += '[{language}]({url})'.format(
                language = lang.capitalize(),
                url = dirname + '/{title}.{ext}'.format(
                    title=quiz.title_slug,
                    ext=prolangdict[lang].ext
                )
            )
            solutions += ' '

        row = '|{id}|[{title}]({url})|{solutions}|{note}|{difficulty}|\n'.format(
                id= quiz.id,
                title= quiz.title,
                url = quiz.url,
                solutions = solutions,
                note='None',
                difficulty = quiz.difficulty,
            )

        pos = self._find_position(self.table_content,quiz.id)
        self.table_content.insert(pos,row)

    def update_readme(self,num_solved,num_total):
        self._init_readme_head(num_solved=num_solved,num_total=num_total)
        with open(self.file,'a') as fd:
            fd.writelines(self.table_content)
            fd.close()


    def _read_file(self):
        with open(self.file,'r') as fd:
            content = fd.readlines()
            fd.close()
        return content

    def _write_file(self,content):
        with open(self.file,'w') as fd:
            fd.writelines(content)
            fd.close()

    @property
    def is_exit(self):
        return os.path.isfile(self.file)