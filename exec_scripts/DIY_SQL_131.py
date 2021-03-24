# -*- coding: utf-8 -*-
import time
from EXECUTE_CLS import *
from EXECUTING_SQL import *

import multiprocessing as mp

url0 = r'jdbc:kunlun://192.168.3.121:6611/UPBMS'
url1 = r'jdbc:kunlun://192.168.3.138:26690/UPBMS'
url2 = r'jdbc:kunlun://192.168.3.138:27690/UPBMS'
driver = r'com.kunlun.jdbc.Driver'
jar_file = r'/home/zl/jm/kunlun_r9.jar'
user = 'UPBMS'
passwd = 'UPBMS'

con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
con_class1 = my_execsql(url1, driver, jar_file, user, passwd)
con_class2 = my_execsql(url2, driver, jar_file, user, passwd)
con_list = [con_class0, con_class0, con_class0]


def do_insert_CMCC_USER_INFO(con, thread_id):
    i = 0
    while True:
        i = i + 1
        sql = DiyBusiness().insert_sql_cmcc_user_info(i, str(thread_id).zfill(3))
        con.short_execute_sql(sql)
        print('insert_sql-' + str(i) + '-' + str(thread_id).zfill(3) + ' ok!')
        if i == 10000000000:
            break


def do_update_DIY(con):
    i = 0
    while True:
        i = i + 1
        time.sleep(3)
        sql = DiyBusiness().update_sql_user_account(i)
        con.short_execute_sql(sql)
        print('update ok!')
        if i == 10000000000:
            break


def transfer_pro(con, thread_id):
    i = 0
    while True:
        i = i + 1
        sql = DiyBusiness().transfer_pro()
        con.short_execute_sql(sql)
        print('trans_sql-' + str(i) + '-' + str(thread_id).zfill(3) + ' ok!')
        if i == 10000000000:
            break


def delete_sql(con, thread_id):
    tablelist = ['ERR_TRANSFER_LOG', 'SUCC_TRANSFER_LOG']
    i = 0
    while True:
        i = i + 1
        sql = DiyBusiness().del_data_with_date(tablelist[random.randint(0, len(tablelist) - 1)])
        con.short_execute_sql(sql)
        print('trans_sql-' + str(i) + '-' + str(thread_id).zfill(3) + ' ok!')
        if i == 10000000000:
            break


def exec_sql_from_file(con):
    for sql in read_sqlfile('sql_mk/DIY_SQL'):
        con.short_execute_sql(sql)
        print(sql + ' do ok!')


def main():
    for a in range(100):
        '''每个节点做不同表的insert'''
        p_in_1 = mp.Process(target=do_insert_CMCC_USER_INFO, args=(con_list[random.randint(0, len(con_list) - 1)], a,))
        '''每个节点做不同表的update'''
        p_up_1 = mp.Process(target=do_update_DIY, args=(con_list[random.randint(0, len(con_list) - 1)],))
        # p_up_2 = mp.Process(target=do_update_DIY, args=(con_list[random.randint(0, len(con_list) - 1)],))
        # p_up_3 = mp.Process(target=do_update_DIY, args=(con_list[random.randint(0, len(con_list) - 1)],))
        '''每个不同的节点做转账'''
        p_trans_1 = mp.Process(target=transfer_pro, args=(con_list[random.randint(0, len(con_list) - 1)], a,))
        p_trans_2 = mp.Process(target=transfer_pro, args=(con_list[random.randint(0, len(con_list) - 1)], a,))
        p_trans_3 = mp.Process(target=transfer_pro, args=(con_list[random.randint(0, len(con_list) - 1)], a,))
        p_d_1 = mp.Process(target=delete_sql, args=(con_list[random.randint(0, len(con_list) - 1)], a,))

        p_in_1.start()
        p_up_1.start()
        # p_up_2.start()
        # p_up_3.start()
        p_trans_1.start()
        p_trans_2.start()
        p_trans_3.start()
        p_d_1.start()


if __name__ == '__main__':
    opt = int(input('please input your option with 1/2:'))
    if opt == 1:
        do_create_upbms('jdbc:kunlun://192.168.3.121:6611/sysdb')
        exec_sql_from_file(con_class0)
    elif opt == 2:
        main()
    else:
        print('please input your option with 1/2!')
