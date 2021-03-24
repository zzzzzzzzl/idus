# -*- coding: utf-8 -*-

import jaydebeapi
from datetime import *
import threading
import multiprocessing
import time
now_date = datetime.now()

url = r'jdbc:kunlun://192.168.3.136:9258/system'
driver = r'com.kunlun.jdbc.Driver'
jar_file = r'/home/gao/kunlun_r3.jar'

user = 'SYSDBA'
passwd = 'SYSDBA'



class ThreadPool():  # 创建线程池类
    def __init__(self, max_thread):
        self.queue = multiprocessing.Queue(max_thread)  # 创建一个队列(使用multiprocessing多线程队列)
        for i in range(max_thread):  # 循环把线程对象加入到队列中
            self.queue.put(threading.Thread)
            # 把线程的类名放进去，执行完这个Queue

    def get_thread(self):  # 定义方法从队列里获取线程
        return self.queue.get()

    def add_thread(self):  # 定义方法在队列里添加线程
        self.queue.put(threading.Thread)


class conn_db():

    # 连接和执行语句一起
    def executesql(slef, exec_sql, a, p):

        # 表示有结果输出的sql
        if a == 0:
            conn = jaydebeapi.connect(driver, url, [user, passwd], jar_file)
            curs = conn.cursor()
            curs.execute(exec_sql)
            res = curs.fetchall()
            curs.close()
            conn.close()
            print(res)
            p.add_thread()
            return res
        # 表示有结果输出的sql
        elif a == 1:
            conn = jaydebeapi.connect(driver, url, [user, passwd], jar_file)
            curs = conn.cursor()
            curs.execute(exec_sql)
            curs.close()
            conn.close()
            p.add_thread()
        else:
            print('please input 0/1 !')
            raise ValueError

    # KL数据库额外新建连接
    def conn(self):
        con = jaydebeapi.connect(driver, url, [user, passwd], jar_file)
        return con

    # 新建连接后执行语句
    def executesql_js(slef, conn, exec_sql, a, p):

        # 表示有结果输出的sql
        if a == 0:
            curs = conn.cursor()
            curs.execute(exec_sql)
            res = curs.fetchall()
            print(res)
            time.sleep(5)
            p.add_thread()
            return res
        # 表示无结果输出的sql
        elif a == 1:
            curs = conn.cursor()
            curs.execute(exec_sql)
            p.add_thread()
        else:
            print('please input 0/1 !')
            raise ValueError
    #close curs and connect
    def close_con(self, conn):
        curs = conn.cursor()
        curs.close()
        conn.close()


# 该方法将一个函数列为单独进程并置于后台的程序
def mul_pro(func,*args):
    try:
        p = multiprocessing.Process(target=func,args=args)
        p.daemon = True
        p.start()
    except TypeError as e:
        print(*args)
        raise e

if __name__ == '__main__':
    exec_sql = 'call clb_proc2()'
    pool = ThreadPool(50)
    conn_list = []
    for i in range(100):
        conn = conn_db().conn()
        conn_list.append(conn)
    c = conn_db()
    while True:
        j = 0
        thread = pool.get_thread()
        t = thread(target=mul_pro, args=(c.executesql, exec_sql, 1, pool))
        t.daemon = True
        j += 1
        t.start()
