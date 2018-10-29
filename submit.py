# -*- coding: utf-8 -*-
# @Time    : 2018/10/29 13:55
# @Author  : Jeffrey
import json

import re
import requests
from bs4 import BeautifulSoup

COOKIE = '' # 填写你的COOKIE
AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'


class Submit:
    # 根据自己的考试链接填写
    CURL = ''
    s = requests.session()

    def __init__(self, cookie):
        self.question_items = []
        self.headers = {
            'cookie': cookie,
            'user-agent': AGENT,
        }

    def _get_item(self):
        html = self.s.get(url=self.CURL, headers=self.headers, timeout=20)
        soup = BeautifulSoup(html.text, 'html.parser')
        btn_list = soup.select('.btn-toolbar')[0].findAll('button')
        for item in btn_list:
            item_info = dict()
            item_info['itemId'] = item['rel']
            item_info['itemType'] = item['itemtype']
            item_info['state'] = 0
            item_info['answer'] = ''
            self.question_items.append(item_info)

    def _get_answer(self):
        url = 'http://aqkslab.nbut.edu.cn/ept/manage/examcenter/showItem'
        question_items = self.question_items
        for item in question_items:
            data = {
                'id': item['itemId']
            }
            html = self.s.post(url=url, headers=self.headers, data=data, timeout=20)
            soup = BeautifulSoup(html.text, 'html.parser')
            praxis_id = soup.select('.praxis-id')[0]['value']
            answer = self._search(praxis_id)
            item['answer'] = answer

    def _submut_items(self):
        url = 'http://aqkslab.nbut.edu.cn/ept/manage/examcenter/submitAnswer'
        exa_id = re.search(r'examineeDetailId=(.*?)&', self.CURL).group(1)
        for item in self.question_items:
            data = {
                'answer': str([item]),
                'examineeDetailId': exa_id,
                'tag': False
            }
            print(data)
            html = self.s.post(url=url, headers=self.headers, data=data, timeout=20)
            print(html.text)

    def _submit_answers(self):
        exa_id = re.search(r'examineeDetailId=(.*?)&', self.CURL).group(1)
        url = 'http://aqkslab.nbut.edu.cn/ept/manage/examcenter/submitAnswer'
        for item in self.question_items:
            item['state'] = 1
        data = {
            'answer': str(self.question_items),
            'examineeDetailId': exa_id,
            'tag': True,
            'noAnswer': ''
        }
        html = self.s.post(url=url, headers=self.headers, data=data, timeout=20)
        print(html.text)

    @staticmethod
    def _search(praxis_id):
        with open('questions.json', 'r') as f:
            json_data = json.load(f)
            for data in json_data:
                if data['praxis_id'] == praxis_id:
                    if (len(data['answer']) > 1) and (len(data['answer']) <= 10):
                        return data['answer'].replace('', ',')[1:-1]
                    return data['answer']

    def get(self):
        self._get_item()
        self._get_answer()
        self._submut_items()
        self._submit_answers()


submit = Submit(COOKIE)
submit.get()
# 完成后查看成绩
# url = 'http://aqkslab.nbut.edu.cn/ept/manage/examcenter/result?examineeId=8296&examineeDetailId=' + exa_id
