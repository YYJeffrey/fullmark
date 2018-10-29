# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 13:32
# @Author  : Jeffrey
import time
import random
import re
import json
import requests
from bs4 import BeautifulSoup

# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=2&type=0&_=1540791243903'   # 化学类
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=3&type=0&_=1540791265494'   # 生物类
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=5&type=0&_=1540791382584'   # 机械类
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=6&type=0&_=1540791410486'   # 辐射类
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=7&type=0&_=1540791441877'   # 电气类
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=8&type=0&_=1540791482212'   # 通识类
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=10&type=0&_=1540791482215'  # 消防安全类
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=11&type=0&_=1540791608166'  # 特种设备
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=12&type=0&_=1540791608169'  # 信息安全类
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId=13&type=0&_=1540791737363'  # 网络安全类


COOKIE = '' # 填写你的COOKIE
AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'


class Questions:
    def __init__(self, cookie):
        self.questions = []
        self.subject_list = ['2', '3', '5', '6', '7', '8', '10', '11', '12', '13']
        self.headers = {
            'cookie': cookie,
            'user-agent': AGENT
        }

    def _get_praxis_id(self, subject_id):
        url_base = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/content?subjectId={subjectId}&type=0&_=1540791243903'
        url = url_base.format(subjectId=subject_id)

        html = requests.get(url=url, headers=self.headers, timeout=20)
        praxis_id_list = re.search(r'\[(.*?)\]', html.text).group(0)
        praxis_id = praxis_id_list[1:-1].split(',')
        return praxis_id

    def _get_question(self, praxis_id):
        url = 'http://aqkslab.nbut.edu.cn/ept/manage/practice/praxis'
        data = {
            'praxisId': praxis_id
        }
        html = requests.post(url=url, headers=self.headers, data=data, timeout=20)
        soup = BeautifulSoup(html.text, 'html.parser')
        question = dict()
        # noinspection PyBroadException
        try:
            question['praxis_id'] = praxis_id
            question['title'] = soup.select('.item-title p')[0].text
            question['answer'] = soup.find('div', class_='div-item-answer').text.strip().replace('<p>', '').replace(
                '</p>', '').replace('\n', '')
        except Exception:
            question = {}
        print(question)
        return question

    def get(self):
        for subject in self.subject_list:
            praxis_id = self._get_praxis_id(subject)
            for pid in praxis_id:
                self.questions.append(self._get_question(pid))
                time.sleep(random.random())   # 随机延迟减小服务器压力(注释此行代码后会很刺激)

    def save(self):
        json_data = json.dumps(self.questions)
        with open('questions.json', 'w') as f:
            f.write(json_data)


questions = Questions(COOKIE)
questions.get()
questions.save()
