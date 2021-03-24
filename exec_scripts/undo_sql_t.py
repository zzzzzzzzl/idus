# -*- coding: utf-8 -*-

from EXECUTE_CLS import *
from EXECUTING_SQL import *
import multiprocessing as mp

url0 = r'jdbc:kunlun://192.168.3.138:25690/UPBMS'
url1 = r'jdbc:kunlun://192.168.3.138:26690/UPBMS'
url2 = r'jdbc:kunlun://192.168.3.138:27690/UPBMS'
driver = r'com.kunlun.jdbc.Driver'
jar_file = r'/home/zl/jm/kunlun_r9.jar'
user = 'UPBMS'
passwd = 'UPBMS'

con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
con_class1 = my_execsql(url1, driver, jar_file, user, passwd)
con_class2 = my_execsql(url2, driver, jar_file, user, passwd)
con_list = [con_class0, con_class1, con_class2]
undo = UndoTest()


def create_table(i):
    for a in range(i):
        con = con_list[random.randint(0, len(con_list) - 1)]
        sql_v = undo.create_undo_table(a)
        p = mp.Process(target=con.short_execute_sql, args=(sql_v,))
        p.start()
        print(sql_v + ' do ok !')


def do_loop(i):
    for a in range(i):
        con = con_list[random.randint(0, len(con_list) - 1)]
        sql_v = undo.insert_loop(a)
        p = mp.Process(target=con.short_execute_sql, args=(sql_v,))
        p.start()
        print(sql_v + ' do ok !')


def exec_sql_from_file(con):
    for sql in read_sqlfile('sql_mk/DIY_SQL'):
        con.short_execute_sql(sql)
        print(sql + ' do ok!')


if __name__ == '__main__':
    opt = int(input('please input your option with 1/2/3:'))
    if opt == 1:
        do_create_upbms('jdbc:kunlun://192.168.3.138:25690/sysdb')
        exec_sql_from_file(con_class0)
    elif opt == 2:
        create_table(100)
    elif opt == 3:
        do_loop(100)
    else:
        print('please input your option with 1/2/3!')
