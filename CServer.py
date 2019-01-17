#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from socket import *
import threading
import struct
from CDatabase import *
from enum import Enum

#回复消息枚举
class EnumMessageType(Enum):
    GetVirusMD5 = 1
    UploadVirus = 2





class CServerSocket():
    #数据包放数据的总大小 = 2048
    #真正有效的数据大小 = 4
    #请求的类型 = 4
    BUFSIZE = 2048 + 4 + 4
    #连接数据库的对象
    db = CDatabase()

    def __init__(self , ip , port):
        #ip = 服务器IP
        #port = 监听的端口
        ADDR = (ip , port);
        print("正在启动服务器启动...")
        self.socketServer=socket(AF_INET,SOCK_STREAM)
        #绑定
        self.socketServer.bind(ADDR)
        #监听
        self.socketServer.listen(5)

    #接收客户端 , 只用来接收客户端线程
    def acceptClient(self):
        #创建线程 , 用来接收多个客户端(socket)
        #__accpetProc__这个线程执行代码的地方
        t = threading.Thread(target=self.__acceptProc__)
        t.start()

    #接收客户端线程
    def __acceptProc__(self):
        #使用while死循环 , 让此线程不停的接受客户端
        while True:
            # accept返回的是个元组（套接字对象，客户端地址）
            socketClient, addrClient = self.socketServer.accept()
            print("客户端连接了!!!");
            # 向客户端发送连接成功消息
            #socketClient.send("连接成功!".encode('gb2312'))

            #每成功接收一个客户端 , 就创建一个线程为其服务
            t = threading.Thread(target=self.__recvProc__ ,
                                 args=(socketClient , ))
            t.start()

    #为每个客户端服务的线程
    def __recvProc__(self, socket):
        #使用while循环 , 不停的获取从客户端传输过来的消息
        while True:
            try:
                # 接收客户端发送过来的消息
                message = socket.recv(CServerSocket.BUFSIZE)
                # 解码消息
                MsgSize, MsgType = struct.unpack('ii', message[0:8])
                # 根据消息的类型调用不同的处理函数
                CServerSocket.dictFun[MsgType](socket, message, MsgSize)

            except Exception as info:
                print(info)
                socket.close()
                return


    #从数据库中获取病毒的MD5值
    def __GetVirusMD5__(socket,  message, MsgSize):
        #从数据库中查询出病毒的MD5值
        sql_select = "select virus_name , md5 from virus_list"
        result = CServerSocket.db.query(sql_select)

        #设置发送给客户端的消息
        message_type = EnumMessageType.GetVirusMD5

        #构造发送给客户端的数据包
        send_msg = ""
        for row in result:
            #send_msg += row[0] + ":";
            send_msg += row[1] + "|";
        #除去最后的|
        send_msg = send_msg[:-1].encode('gbk')

        #发送消息给客户端
        return_msg = struct.pack("ii2048s" , len(send_msg) , message_type.value , send_msg)
        socket.send(return_msg)

    #上次病毒到数据库
    def __UploadVirus__(socket,  message, MsgSize):
        #解析出用户上传上来的md5值
        msgbuff, = struct.unpack('%ds' % MsgSize, message[8:8 + MsgSize])
        virus_md5 = msgbuff.decode("gbk")

        #从数据库中查询出病毒的MD5值
        sql_select = "select md5 from virus_list"
        result = CServerSocket.db.query(sql_select)

        message_type = EnumMessageType.UploadVirus

        sql_select = "INSERT INTO virus_list(md5) VALUES(%s)"


        flag = 1
        #判断数据库是否存在病毒
        for row in result:
            if virus_md5 == row[0]:
                flag = 0
                break;

        if flag:
            result = CServerSocket.db.insert(sql_select, virus_md5)



        send_msg = "上传成功".encode('gbk')
        return_msg = struct.pack("ii2048s", len(send_msg), message_type.value, send_msg)
        socket.send(return_msg)





    # 类变量
    # 处理各种消息的函数
    dictFun = {
        1: __GetVirusMD5__,
        2:__UploadVirus__
    }