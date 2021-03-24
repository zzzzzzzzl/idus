# -*- coding: utf-8 -*-

from EXECUTE_CLS import *
from EXECUTING_SQL import *
from SOCKET_SERVER_FOR_STATISTICS import *
import multiprocessing as mp

url0 = r'jdbc:kunlun://192.168.3.139:35690/UPBMS'
url1 = r'jdbc:kunlun://192.168.3.140:35690/UPBMS'
url2 = r'jdbc:kunlun://192.168.3.141:35690/UPBMS'
# url0 = r'jdbc:kunlun://192.168.3.138:25690/UPBMS'
# url1 = r'jdbc:kunlun://192.168.3.138:26690/UPBMS'
# url2 = r'jdbc:kunlun://192.168.3.138:27690/UPBMS'
# url3 = r'jdbc:kunlun://192.168.3.138:28690/UPBMS'
driver = r'com.kunlun.jdbc.Driver'
jar_file = r'kunlun_r9.jar'
user = 'UPBMS'
passwd = 'UPBMS'

con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
con_class1 = my_execsql(url1, driver, jar_file, user, passwd)
con_class2 = my_execsql(url2, driver, jar_file, user, passwd)
con_all_list = [con_class0, con_class1, con_class2]


def sel_con():
    new_con_list = []
    v_sql = 'select * from dual'
    for con in con_all_list:
        try:
            con.short_execute_sql(v_sql, a_out=1)
            new_con_list.append(con)
        except Exception as e:
            if '无法与服务器通信' in str(e):
                continue
    return new_con_list


def do_insert_product_info_tab():
    i = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:

        try:
            sql1 = DiyBusiness().product_info_tab_clob()
            sql2 = DiyBusiness().product_info_tab()
            con.short_execute_sql(sql2)
            con.short_execute_sql(sql1)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'do_insert_product_info_tab--' + str(i), 56789)
                i = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'do_insert_cmcc_user_info--' + str(i), 56789)
                break


def main():
    for a in range(50):
        '''表的insert'''
        p_in_1 = mp.Process(target=do_insert_product_info_tab)
        p_in_2 = mp.Process(target=do_insert_product_info_tab)
        p_in_3 = mp.Process(target=do_insert_product_info_tab)
        p_in_1.start()
        p_in_2.start()
        p_in_3.start()


if __name__ == '__main__':
    opt = int(input('please input your option with 1:建库建表/2:执行业务程序:'))
    if opt == 1:
        do_create_upbms('jdbc:kunlun://192.168.3.121:6632/sysdb')
    elif opt == 2:
        main()
    else:
        print('please input your option with 1:建库建表/2:执行业务程序!')
