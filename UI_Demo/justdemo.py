# -*- coding: UTF-8 -*-
"""
@author:ZHOU LEI
@file:justdemo.py
@time:2021/02/24
"""
import os
import threading as thr
import multiprocessing as mlp

loc = 'D:\测试备份\python_scripts\idus\exec_scripts\connect_demo.py'


def do_java_re():
    p = thr.Thread(target=os.system, args=('{} {}'.format('python', loc),))
    p.start()
    p.join()
    print('do it over!')


if __name__ == '__main__':
    do_java_re()
