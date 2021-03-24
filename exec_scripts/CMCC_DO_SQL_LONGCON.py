# -*- coding: utf-8 -*-

from EXECUTE_CLS import *


def do_long_cmcc(con, t):
    sql = con.transfer_pro()
    con.long_execute_sql(sql, t)


if __name__ == '__main__':
    import multiprocessing as mp

    url0 = r'jdbc:kunlun://192.168.3.138:5690/UPBMS'
    url1 = r'jdbc:kunlun://192.168.3.138:6690/UPBMS'
    url2 = r'jdbc:kunlun://192.168.3.138:7690/UPBMS'
    driver = r'com.kunlun.jdbc.Driver'
    jar_file = r'/home/zl/jm/kunlun_r9.jar'
    user = 'UPBMS'
    passwd = 'UPBMS'

    con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
    con_class1 = my_execsql(url1, driver, jar_file, user, passwd)
    con_class2 = my_execsql(url2, driver, jar_file, user, passwd)
    for a in range(150):
        '''每个节点做不同表的insert'''
        p_in_5690 = mp.Process(target=do_long_cmcc, args=(con_class0, a,))
        '''启动进程'''
        p_in_5690.start()
