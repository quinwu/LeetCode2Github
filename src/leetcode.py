import requests
import os
import time
import datetime
import re
import json
from collections import OrderedDict
from selenium import webdriver
from src.question import Quiz
from src.generate import Readme
from utils import check_and_make_dir,ProgLangDict,rep_unicode_in_code,HEADERS,PROXIES,BASE_URL,COOKIE_PATH

class Leetcode:

    def __init__(self,config):
        self.base_url = BASE_URL
        self.config = config

        self.languages = [x.strip() for x in self.config['language'].split(',')]
        proglangs = [
            ProgLangDict[x.strip()] for x in self.config['language'].split(',')
        ]
        self.prolangdict = dict(zip(self.languages,proglangs))

        self.num_solved = 0
        self.num_total = 0

        self.items = []
        self.submissions = []
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.proxies = PROXIES
        self.cookies = None

        self.README = Readme(self.config['local_path'])

    def login(self):
        LOGIN_URL = self.base_url + '/accounts/login/'
        if not self.config['username'] or not self.config['password']:
            raise Exception(
                'Leetcode - Please input your username and password in config.cfg.'
            )

        usr = self.config['username']
        passwd = self.config['password']

        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--disable-gpu')
        executable_path = self.config.get('driverpath')
        driver = webdriver.Chrome(
            chrome_options=options,executable_path=executable_path
        )
        driver.get(LOGIN_URL)
        time.sleep(10)

        driver.find_element_by_name('login').send_keys(usr)
        driver.find_element_by_name('password').send_keys(passwd)
        # driver.find_element_by_xpath('//button[@type="submit"]').click()
        btns = driver.find_elements_by_tag_name('button')
        submit_btn = btns[1]
        submit_btn.click()

        time.sleep(5)
        webdriver_cookies = driver.get_cookies()
        driver.close()

        if 'LEETCODE_SESSION' not in [
            cookie['name'] for cookie in webdriver_cookies
        ]:
            raise Exception('Please check your config or network')

        with open(COOKIE_PATH,'w') as f:
            json.dump(webdriver_cookies,f,indent=2)
        self.cookies = {
            str(cookie['name']): str(cookie['value'])
            for cookie in webdriver_cookies
        }
        self.session.cookies.update(self.cookies)

    @property
    def is_login(self):
        api_url = self.base_url + '/api/problems/algorithms/'
        if not os.path.exists(COOKIE_PATH):
            return False

        with open(COOKIE_PATH,'r') as f:
            webdriver_cookies = json.load(f)
        self.cookies = {
            str(cookie['name']) : str(cookie['value'])
            for cookie in webdriver_cookies
        }

        self.session.cookies.update(self.cookies)
        r = self.session.get(api_url,proxies = PROXIES)
        if r.status_code != 200:
            return False

        data = json.loads(r.text)
        return 'user_name' in data and data['user_name'] != ''

    def load_items_from_api(self,quizs):

        """

        :param quizs: int list, each of list element mean each title frontend-question-id
        :return:
        """
        api_url = self.base_url + '/api/problems/algorithms/'
        r = self.session.get(api_url,proxies=PROXIES)

        assert r.status_code == 200

        rst = json.loads(r.text)

        if not rst['user_name']:
            raise Exception("Something wrong with your personal info.\n")

        self.num_solved = rst['num_solved']
        self.num_total = rst['num_total']
        self.items = list(self._generate_items_from_api(rst,quizs))
        self.items.reverse()

    def _generate_items_from_api(self,json_data,quizs):
        """

        :param json_data: all problem status json data
        :param quizs: int list, each of list element mean each title frontend-question-id
                        if quizs is empty , we want to download all Accepted problems
        :return:
        """
        if quizs:
            stat_staus_pairs = json_data['stat_status_pairs']
            # print (stat_staus_pairs)
            for quiz in stat_staus_pairs:
                if quiz['stat']['frontend_question_id'] in quizs:
                    data = {}
                    data['question_id'] = quiz['stat']['frontend_question_id'] #id
                    data['question_title_slug'] = quiz['stat']['question__title_slug']   #title-slug
                    data['question_title'] = quiz['stat']['question__title'] #title
                    data['level'] = quiz['difficulty']['level']             #difficulty
                    data['status'] = quiz['status']
                    item = Quiz(**data)
                    yield item
        else:
            stat_staus_pairs = json_data['stat_status_pairs']
            for quiz in stat_staus_pairs:
                if quiz['status'] == 'ac':
                    data = {}
                    data['question_id'] = quiz['stat']['frontend_question_id']
                    data['question_title_slug'] = quiz['stat']['question__title_slug']
                    data['question_title'] = quiz['stat']['question__title']
                    data['level'] = quiz['difficulty']['level']
                    data['status'] = quiz['status']
                    item = Quiz(**data) 
                    yield item

    def load_submission(self):
        """
        load all submissions
        :return: all submissions
        """
        print('API load submissions request 2 seconds per request')
        print('Please wait ...')
        limit = 20
        offset = 0
        last_key = ''
        while True:
            # submissions_url = '{}/api/submissions/?format=json&limit={}&offset={}'.format(
            #     self.base_url, limit, offset
            # )
            print('try to load submissions from ', offset, ' to ', offset+limit)
            submissions_url = '{}/api/submissions/?format=json&limit={}&offset={}&last_key={}'.format(
                self.base_url, limit, offset, last_key
            )

            resp = self.session.get(submissions_url,proxies=PROXIES)
            print (submissions_url,':', resp.status_code)

            assert resp.status_code == 200
            data = resp.json()

            if 'has_next' not in data.keys():
                raise  Exception ('Get submissions wrong ,Check network \n')

            self.submissions += data['submissions_dump']
            if data['has_next']:
                offset += limit
                last_key = data['last_key']
                time.sleep(2.5)
            else:
                break

    def load_submission_to_items(self):

        titles = [i.title for i in self.items]
        itemdict = OrderedDict(zip(titles,self.items))

        def make_sub(sub):
            return dict(
                runtime=int(sub['runtime'][:-3]),
                title=sub['title'],
                lang=sub['lang'],
                submission_url = self.base_url + sub['url']
            )

        ac_subs = [
            make_sub(sub)
            for sub in self.submissions
            if sub['status_display'] == 'Accepted'
        ]

        def remain_shortesttime_submissions(submissions):
            submissions_dict = {}

            for item in submissions:
                k = '{}-{}'.format(item['lang'],item['title'])
                if k not in submissions_dict.keys():
                    submissions_dict[k] = item
                else:
                    old = submissions_dict[k]
                    if item['runtime'] < old['runtime']:
                        submissions_dict[k] = item
            return list(submissions_dict.values())

        shortest_sub = remain_shortesttime_submissions(ac_subs)

        for solution in shortest_sub:
            title = solution['title']
            if title in itemdict.keys():
                itemdict[title].solutions.append(solution)

        for item in itemdict.values():
            py_solution = 0
            sol = None
            for solution in item.solutions:
                if solution['lang'] == 'python' :
                    py_solution += 1
                    sol = solution
                elif solution['lang'] == 'python3':
                    py_solution += 1
            if py_solution == 2:
                item.solutions.remove(sol)

    def _get_code_by_solution(self,solution):
        """

        :param solution:
        :return: code by solution submission_url
        """
        solution_url = solution['submission_url']
        print (solution_url)
        r = self.session.get(solution_url,proxies=PROXIES)

        assert r.status_code == 200

        pattern = re.compile(
            r'submissionCode: \'(?P<code>.*)\',\n  editCodeUrl', re.S
        )

        m1 = pattern.search(r.text)
        code = m1.groupdict()['code'] if m1 else None

        if not code:
            raise Exception(
                'can not find solution code in question:{title}'.format(
                    title = solution['title']
                )
            )

        code = rep_unicode_in_code(code)
        return code

    def _download_code_by_quiz(self,quiz):
        id = quiz.question_id
        title = quiz.question_title
        title_slug = quiz.question_title_slug
        solutions = list(
            filter(lambda i:i['lang'] in self.languages ,quiz.solutions)
        )

        if not solutions:
            print(
                'No solution with the set languages in question:{}-{}'.format(
                    id, title
                )
            )
            return

        dirname = '{id}. {title}'.format(id=str(id).zfill(3),title=title)
        print ('begin download'+ dirname)
        path = os.path.join(self.config['local_path'],dirname)
        print ('path is',path)
        check_and_make_dir(path)

        for solution in solutions:
            fname = '{title_slug}.{ext}'.format(
                title_slug = title_slug,
                ext = self.prolangdict[solution['lang']].ext
            )
            filename = os.path.join(path,fname)
            code = self._get_code_by_solution(solution)

            #todo what is codecs
            import codecs
            with codecs.open(filename,'w','utf-8') as f:
                print ('write to file -> ',fname)
                f.write(code)

    def load(self,quizs):
        if not self.is_login:
            print ('not login')
            self.login()
        print ('has login')
        self.load_items_from_api(quizs)
        self.load_submission()
        self.load_submission_to_items()

    def download(self):
        for quiz in self.items:
            time.sleep(1)
            self._download_code_by_quiz(quiz)

    def write_README(self):
        print ('start to write README')
        for quiz in self.items:
            self.README.add_question(quiz, self.languages, self.prolangdict)
        self.README.update_readme(self.num_solved,self.num_total)
        print ('write README done!')

    def push_to_github(self):
        print ('start push to GitHub')
        strdate = datetime.datetime.now().strftime('%Y-%m-%d')
        cmd_git_add = 'git add .'
        cmd_git_commit = 'git commit -m "update at {date}"'.format(
            date=strdate
        )
        cmd_git_push = 'git push -u origin master'
        
        print (os.getcwd())
        os.chdir(self.config['local_path'])
        print (os.getcwd())
        os.system(cmd_git_add)
        os.system(cmd_git_commit)
        os.system(cmd_git_push)
        print ('push to GitHub done!')


    def run(self,quizs):
        self.load(quizs)
        self.download()
        self.write_README()
        self.push_to_github()