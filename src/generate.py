import re
from src.utils import check_and_make_file,check_and_make_dir
from src.utils import Config

class Readme:
    def __init__(self,dir):
        check_and_make_dir(dir)
        # self.path = dir + '/README.md'
        self.path = dir + '/READM1E.md'
        check_and_make_file(self.path)
        self.content = self._read_file()

    def _read_file(self):
        with open(self.path,'r') as fd:
            content = fd.readlines()
            fd.close()
        return content

    def _write_file(self):
        with open(self.path,'w') as fd:
            fd.writelines(self.content)
            fd.close()

    def _find_position(self,lists,num):
        re_id = re.compile(Config.pattern_re)
        sort_nums = []
        sort_nums.append(num)
        for str in lists:
            id = re_id.match(str).group(0)[1:-1]
            sort_nums.append(int(id))
        sort_nums.sort()
        return sort_nums.index(num) + Config.number_of_prefix

    def add_question(self,question):
        row = '|{id}|[{title}]({url})|{solutions}|{note}|{difficulty}|{tag}|\n'.format(
                id= question.num,
                title= question.info['title'],
                url = question.info['url'],
                solutions = question.info['solutions'],
                note='None',
                difficulty = question.info['difficult'],
                tag = ''
            )
        sort_content = self.content[Config.number_of_prefix:]
        pos = self._find_position(sort_content,question.num)
        self.content.insert(pos,row)

    def write_readme(self):
        self._write_file()
