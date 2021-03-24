# -*- coding: utf-8 -*-

from EXECUTE_CLS import *


def do_insert_CMCC_USER_INFO(con, thread_id):
    i = 0
    while True:
        i = i + 1
        sql = con.insert_sql_cmcc_user_info(i, str(thread_id).zfill(3))
        con.short_execute_sql(sql, record=1)
        print('insert_sql-' + str(i) + '-' + str(thread_id).zfill(3) + ' ok!')
        if i == 100000:
            break


def transfer_pro(con, thread_id):
    i = 0
    while True:
        i = i + 1
        sql = con.transfer_pro()
        con.short_execute_sql(sql, record=1)
        print('trans_sql-' + str(i) + '-' + str(thread_id).zfill(3) + ' ok!')
        if i == 100000:
            break


if __name__ == '__main__':
    import multiprocessing as mp

    url0 = r'jdbc:kunlun://192.168.3.130:12600/UPBMS'
    url1 = r'jdbc:kunlun://192.168.3.131:12600/UPBMS'
    url2 = r'jdbc:kunlun://192.168.3.132:12600/UPBMS'
    driver = r'com.kunlun.jdbc.Driver'
    jar_file = r'/home/zl/jm/kunlun_r9.jar'
    user = 'UPBMS'
    passwd = 'UPBMS123'

    con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
    con_class1 = my_execsql(url1, driver, jar_file, user, passwd)
    con_class2 = my_execsql(url2, driver, jar_file, user, passwd)
    for a in range(1):
        '''每个节点做不同表的insert'''
        p_in_5690 = mp.Process(target=do_insert_CMCC_USER_INFO, args=(con_class0, a,))
        '''每个节点做不同表的update'''
        p_up_5690 = mp.Process(target=transfer_pro, args=(con_class0, a))
        '''启动进程'''
        p_in_5690.start()
        p_up_5690.start()
