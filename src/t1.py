# -*- coding: utf-8 -*-
"""
@Author: ipokemon
@Time: 2020/12/11 1:26
@Software: PyCharm 
"""
# -*- coding: utf-8 -*-
"""
@作者: ipokemon
@时间: 2020/11/12 19:36
@文件: translate.py
"""

import time
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from src.kengeemysql import SqlDao
from browsermobproxy import Server
from selenium.webdriver.chrome.options import Options
from itertools import permutations
import subprocess  # vbs






class Kengee(object):
    def __init__(self):
        self.dr = webdriver.Chrome()

        time.sleep(1)
        self.dr.get('https://www.wenjuan.top/s/3ARbiy1#')
        self.dr.implicitly_wait(10)

    def saveall(self):
        """存储题目和答案列表"""
        time.sleep(0.39)
        self.dr.find_element_by_id('5ebe11f93631f27cbbb79679').send_keys('text_name')
        self.dr.find_element_by_id('5ebe12173631f27bad72c2f1').send_keys('text_number')
        self.dr.find_element_by_id('5ebe121b92beb5614a270460').send_keys('text_name')
        self.dr.find_element_by_id('5ebe121f92beb56237aaaf37').send_keys('text_store')
        self.dr.find_element_by_xpath('//*[@id="question_5ebe133e3631f27930b6eea2"]/div[2]/div[3]/div/div[1]').click()
        doc = self.dr.page_source
        soup = BeautifulSoup(doc, "html.parser")
        aq = soup.find_all("div", class_="wjques maxtop question")
        an = 0
        sx = SqlDao()
        sx.opensql()
        self.all_question_id = []
        for i in aq[5:]:
            an += 1
            qid = i.get('question-id')
            self.all_question_id.append(qid)
            typ = i.get("questiontype")
            ali, aali = [], []
            for j in i.find_all("input"):
                aid = j.get('value')
                ali.append(aid)
            if str(typ) == '3':
                for ai in permutations(ali, 2):
                    st = ','.join(ai)
                    aali.append(st)
                for ai in permutations(ali, 3):
                    st = ','.join(ai)
                    aali.append(st)
                aali.append(','.join(ali))
                ali = aali
            sx.writenotexist(qid, ali, str(typ))
        sx.killsql()
        return

    def dokengee(self):
        """做题"""
        sx = SqlDao()
        sx.opensql()
        all_aid = []
        for qid in self.all_question_id:
            aid = sx.getanswer(qid)
            all_aid.append(aid)
            if len(aid) > 24:
                for ai in aid.split(','):
                    ele = self.dr.find_element_by_css_selector(f'input[value="{ai}"]')
                    self.dr.execute_script("arguments[0].scrollIntoView();", ele)
                    self.dr.execute_script("arguments[0].click();", ele)
            else:
                ele = self.dr.find_element_by_css_selector(f'input[value="{aid}"]')
                self.dr.execute_script("arguments[0].scrollIntoView();", ele)
                self.dr.execute_script("arguments[0].click();", ele)
        self.qa_di = dict(zip(self.all_question_id, all_aid))
        if sx.ifstop() == 20:
            # pass
            self.dr.maximize_window()
            subprocess.call('cscript ../files/msg.vbs')
            print('============================================================')
            print('                    本次为满分答案!!!')
            input('============================================================')
        return

    def submitkengee(self):
        """提交后获取代理数据"""
        sx = SqlDao()
        sx.opensql()
        self.dr.find_element_by_id('next_button').click()
        time.sleep(2.11)
        result = self.proxy.har
        for i in result['log']['entries']:
            request = i['request']
            response = i['response']
            # 判断数据所在url并解析数据
            if 'save_page_answers' in request['url']:
                text = response['content']['text']
                text = json.loads(text)
                textlist = text['question_score_map']
                for te, xt in textlist.items():
                    if int(xt) > 0:
                        for q, a in self.qa_di.items():
                            if q == te:
                                sx.setanswer(q, a)
                    else:
                        for q, a in self.qa_di.items():
                            if q == te:
                                sx.setunanswer(q, a)
        sx.killsql()
        return

if __name__ == '__main__':
    k = Kengee()
    k.dokengee()