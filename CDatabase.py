#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
print(sys.version)

import pymysql

class CDatabase():
    def __init__(self):
        #1.连接数据库
        print("正在链接数据库...")
        try:
            connecter = pymysql.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='root',
                db='virus',
                charset='utf8'
            )

            self.connecter = connecter
            # 获取游标对象
            cursor = connecter.cursor()
            # 添加变量
            self.cursor = cursor
            print("数据库链接成功！")
        except Exception as ex:
            print(ex)



    #查询操作
    def query(self , sql_select , param=None):
        try:
            #self.cursor.execute("reset query cahce")
            self.cursor.execute(sql_select , param)

            #获取符合要求的数据列表
            result = self.cursor.fetchall()

            return result
        except:
            print("Error: unable to fecth data")
            return None

    #插入操作
    def insert(self, sql_select, param=None):
        try:
            self.cursor.execute(sql_select, param)
            self.connecter.commit()               # 提交数据
            return True
        except:
            print("Error: insert failed")
            # 发生错误时回滚
            # self.cursor.rollback()
            return None

#测试数据库是否连接成功
if __name__ == '__main__':
    database = CDatabase()