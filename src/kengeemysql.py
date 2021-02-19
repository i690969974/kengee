# -*- coding: utf-8 -*-
"""
@作者: ipokemon
@时间: 2020/11/12 19:35
@文件: kengeemysql.py
"""


import pymysql


class SqlDao(object):
    def opensql(self):
        """连接数据库建表"""
        self.number = 0
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='12345678', db='mysql')
        self.cur = self.conn.cursor()  # 获取一个游标对象
        self.cur.execute("CREATE DATABASE IF NOT EXISTS `kengee`;")
        self.cur.execute("USE `kengee`;")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS `questionku`(
        `id` INT PRIMARY KEY AUTO_INCREMENT,
        `question_id` VARCHAR(24),
        `answer_id_list` TEXT,
        `unanswer_id_list` TEXT,
        `question_type` VARCHAR(1),
        `answer_id` VARCHAR(255));""")

    def writenotexist(self, qid, aidlist, qtype):
        """检测问题id是否重复,否则添加该问题"""
        self.cur.execute(f"SELECT COUNT(question_id) FROM questionku WHERE question_id='{qid}'")
        if not self.cur.fetchone()[0]:
            self.cur.execute(
                f"INSERT INTO questionku(question_id,answer_id_list,question_type) VALUES('{qid}','{';'.join(aidlist)}','{qtype}');")

    def setanswer(self, question_id, answer_id):
        self.cur.execute(f"SELECT answer_id FROM questionku WHERE question_id = '{question_id}'")
        a = self.cur.fetchone()
        if a[0] is None:
            self.cur.execute(f"UPDATE questionku SET answer_id='{answer_id}' WHERE question_id = '{question_id}'")

    def setunanswer(self, question_id, answer_id):
        self.cur.execute(f"SELECT unanswer_id_list FROM questionku WHERE question_id = '{question_id}'")
        a = self.cur.fetchone()
        if a[0] is None:
            self.cur.execute(
                f"UPDATE questionku SET unanswer_id_list='{answer_id}' WHERE question_id = '{question_id}'")
        else:
            unali = a[0] + ';' + answer_id
            self.cur.execute(f"UPDATE questionku SET unanswer_id_list='{unali}' WHERE question_id = '{question_id}'")

    def getanswer(self, question_id):
        self.cur.execute(f"SELECT answer_id FROM questionku WHERE question_id = '{question_id}'")
        answer = self.cur.fetchone()
        if answer[0] is None:
            self.cur.execute(
                f"SELECT answer_id_list, unanswer_id_list FROM questionku WHERE question_id = '{question_id}'")
            yu = self.cur.fetchone()
            ali, unali = yu[0], yu[1]
            if unali is None:
                li = ali.split(';')
                return li[0]
            else:
                li = ali.split(';')
                if ';' in unali:
                    l0 = unali.split(';')
                else:
                    l0 = [unali]
                return list(set(li) - set(l0))[0]
        else:
            self.number += 1
            return answer[0]

    def ifstop(self):
        return self.number

    def killsql(self):
        """提交数据并关闭数据库连接"""
        self.conn.commit()
        self.cur.close()
        self.conn.close()

