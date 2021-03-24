# -*- coding: utf-8 -*-

from EXECUTE_CLS import *
from EXECUTING_SQL import *
from SOCKET_SERVER_FOR_STATISTICS import *
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
con_list = [con_class0]


def do_insert_PRODUCT_INFO_TAB(con):
    i = 0
    while True:
        try:
            sql = DiyBusiness().product_info_tab()
            con.short_execute_sql(sql)
            i = i + 1
            if i % 1000 == 0:
                socket_client_for_statistics('192.168.3.118', 'do_insert_PRODUCT_INFO_TAB--' + str(i))
        except Exception:
            socket_client_for_statistics('192.168.3.118', 'do_insert_PRODUCT_INFO_TAB--' + str(i))
            break


def main():
    for a in range(200):
        '''表的insert'''
        p_in_1 = mp.Process(target=do_insert_PRODUCT_INFO_TAB, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_in_2 = mp.Process(target=do_insert_PRODUCT_INFO_TAB, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_in_1.start()
        p_in_2.start()


if __name__ == '__main__':
    opt = int(input('please input your option with 1/2:'))
    if opt == 1:
        do_create_upbms('jdbc:kunlun://192.168.3.138:25690/sysdb')
    elif opt == 2:
        p = mp.Process(target=main)
        p.start()
        p.join()
        socket_client_for_statistics('192.168.3.118', 'over')
    else:
        print('please input your option with 1/2!')
