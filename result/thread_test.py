# -*- coding: utf-8 -*-

import threading
from time import sleep,ctime

loops = [4,2]

def loop(nloop,nsec):
    print('开始循环',nloop,'at:',ctime())
    sleep(nsec)
    print('结束循环', nloop, 'at:', ctime())


def main():
    print('程序开始于：',ctime)
    threads = []
    nloops = range(len(loops))

    for i in nloops:
        t = threading.Thread(target=loop,args=(i,loops[i]))
        threads.append(t)

    for i in nloops:
        threads[i].start()

    for i in nloops:
        threads[i].join()

    print('任务完成：',ctime())

if __name__ == "__main__":
    main()
