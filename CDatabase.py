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
                db='chatroom',
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


#测试数据库是否连接成功
if __name__ == '__main__':
    database = CDatabase()