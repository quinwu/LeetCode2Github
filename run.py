from src.generate import Readme
from src.question import Question
from src.utils import Config

def main():
    question = Question(12)
    print (question.info)
    print ('question:',question.num)
    readme = Readme(Config.local_path)
    readme.add_question(question)
    readme.write_readme()

if __name__ == '__main__':
    main()