#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
print(sys.version)

from CServer import *

HOST = '127.0.0.1'#服务器ip
PORT = 1234

def main():
    #创建服务器对象
    server = CServerSocket(HOST , PORT)
    #开启接受客户端的线程
    server.acceptClient();


if __name__ == '__main__':
    main();