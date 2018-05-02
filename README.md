# LeetCode2Github

LeetCode to Github

Automatically grab the LeetCode solutions uploaded to Github and generate `README.md` file.

This is my [LeetCode Solutions](https://github.com/quinwu/LeetCode) GitHub repo.

### Config Information

> config/config.cfg

Reference : [config/config.cfg.example](config/config.cfg.example)

- `username` 

    LeetCode username

- `password`

    LeetCode password

- `language`

    Problem solved programming language

- `driverpath`

    [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/) path address on your local machine

- `local_path`

    LeetCode repo path address on your local machine

### Requirements Information

requirements Python env : [requirements.txt](requirements.txt)

Use `selenium` and `ChromeDriver`

Install essential packages:`requestions`,`selenium`

> pip3 install -r requirements.txt

Recommend using package management tools:

- Anaconda

> conda install

- Pipenv

> pipenv install


### Run

#### Download by Problem ID

> python run.py 1
>
> python run.py 1 4 77

if you default python version not Python3.X

> python3 run.py 1
>
> python3 run.py 1 4 77

#### Download All Accepted Problems

> ToDo

### Attention

Python3 has tested 

Python2 not guaranteed

### Acknowledgement

This work builds on many excellent works, which include:

- [bonfy/leetcode](https://github.com/bonfy/leetcode)