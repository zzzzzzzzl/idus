# -*- coding: utf-8 -*-

from EXECUTE_CLS import *
from EXECUTING_SQL import *

DIY = DiyBusiness()


def BJ_insert_cmcc(table_name, con, thread_id):
    BJ = BJCMCC(table_name)
    i = 0
    while True:
        i = i + 1
        sql = BJ.insert_sql_cmcc(i, str(thread_id).zfill(3))
        con.short_execute_sql(sql)
        print('insert executed ok!')
        if i == 100000:
            break


def BJ_update_cmcc(table_name, con):
    BJ = BJCMCC(table_name)
    i = 0
    while True:
        i = i + 1
        sql = BJ.update_sql_cmcc(i)
        con.short_execute_sql(sql)
        print('update executed ok!')
        if i == 100000:
            break


def do_insert_CMCC_USER_INFO(con, thread_id):
    i = 0
    while True:
        i = i + 1
        sql = DIY.insert_sql_cmcc_user_info(i, str(thread_id).zfill(3))
        con.short_execute_sql(sql, record=1)
        print('insert_sql-' + str(i) + '-' + str(thread_id).zfill(3) + ' ok!')
        if i == 100000:
            break


def transfer_pro(con, thread_id):
    i = 0
    while True:
        i = i + 1
        sql = DIY.transfer_pro()
        con.short_execute_sql(sql, record=1)
        print('trans_sql-' + str(i) + '-' + str(thread_id).zfill(3) + ' ok!')
        if i == 100000:
            break


def do_update(con, thread_id):
    i = 0
    while True:
        i = i + 1
        sql = DIY.update_sql_user_account(i)
        con.short_execute_sql(sql, record=1)
        print('update_sql-' + str(i) + '-' + str(thread_id).zfill(3) + ' ok!')
        if i == 100000:
            break


def main():
    import multiprocessing as mp

    url0 = r'jdbc:kunlun://192.168.3.119:11659/system'
    driver = r'com.kunlun.jdbc.Driver'
    jar_file = r'/home/zl/jm/kunlun_r9.jar'
    user = 'SYSDBA'
    passwd = 'SYSDBA'

    con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
    for a in range(100):
        '''每个节点做不同表的insert'''
        p_in_1 = mp.Process(target=BJ_insert_cmcc, args=('SMS_PUSHSYS', con_class0, a,))
        '''每个节点做不同表的update'''
        p_up_1 = mp.Process(target=BJ_update_cmcc, args=('SMS_PUSHSYS', con_class0,))
        """start"""
        p_in_1.start()
        p_up_1.start()


if __name__ == '__main__':
    main()
