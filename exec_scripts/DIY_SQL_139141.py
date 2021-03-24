# -*- coding: utf-8 -*-

from EXECUTE_CLS import *
from EXECUTING_SQL import *
from SOCKET_SERVER_FOR_STATISTICS import *
from exec_scripts.OV_SQL_CLOB139141 import main as clob_run
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
port = ['25690', '26690', '27690', '28690']


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


def do_insert_cmcc_user_info(thread_id, my_port):
    i = 0
    j = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:
        try:
            sql = DiyBusiness().insert_sql_cmcc_user_info(i, str(thread_id).zfill(3), str(my_port))
            con.short_execute_sql(sql)
            i = i + 1
            j = j + 1
            if j == 1000:
                socket_client_for_statistics('192.168.3.118', 'do_insert_cmcc_user_info--' + str(j), 56789)
                j = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'do_insert_cmcc_user_info--' + str(j), 56789)
                break


def do_update_diy():
    i = 0
    j = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:
        try:
            time.sleep(3)
            sql = DiyBusiness().update_sql_user_account(i)
            con.short_execute_sql(sql)
            i = i + 1
            j = j + 1
            if j == 1000:
                socket_client_for_statistics('192.168.3.118', 'do_update_diy--' + str(j), 56789)
                j = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'do_update_diy--' + str(j), 56789)
                break


def transfer_pro():
    i = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:
        try:
            sql = DiyBusiness().transfer_pro()
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'transfer_pro--' + str(i), 56789)
                i = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'transfer_pro--' + str(i), 56789)
                break


def delete_sql():
    table_list = ['ERR_TRANSFER_LOG', 'SUCC_TRANSFER_LOG']
    i = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:
        try:
            sql = DiyBusiness().del_data_with_date(table_list[random.randint(0, len(table_list) - 1)])
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'delete_sql--' + str(i), 56789)
                i = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'delete_sql--' + str(i), 56789)
                break


def exec_sql_from_file(con):
    for sql in read_sqlfile('sql_mk/DIY_SQL1'):
        con.short_execute_sql(sql)
        print(sql + ' do ok!')


def call_order_product():
    i = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:
        try:
            sql = 'call ORDER_PRODUCT'
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'call_order_product--' + str(i), 56789)
                i = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'call_order_product--' + str(i), 56789)
                break


def call_order_product_clob():
    i = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:
        try:
            sql = 'call ORDER_PRODUCT_CLOB'
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'call_order_product_clob--' + str(i), 56789)
                i = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'call_order_product_clob--' + str(i), 56789)
                break


def call_cancel_account():
    i = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:
        try:
            sql = 'call cancel_account'
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'CALL_cancel_account--' + str(i), 56789)
                i = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'CALL_cancel_account--' + str(i), 56789)
                break


def call_cancel_account_clob():
    i = 0
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    while True:
        try:
            sql = 'call cancel_account_clob'
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'CALL_cancel_account_clob--' + str(i), 56789)
                i = 0
        except Exception:
            con_list = sel_con()
            if len(con_list) != 0:
                con = con_list[random.randint(0, len(con_list) - 1)]
            else:
                print('No Useable IpAddress!')
                socket_client_for_statistics('192.168.3.118', 'CALL_cancel_account_clob--' + str(i), 56789)
                break


def clear_sql():
    con_list = sel_con()
    if len(con_list) != 0:
        con = con_list[random.randint(0, len(con_list) - 1)]
    else:
        print('No Useable IpAddress!')
        return
    sql = """
            declare
            begin
            while 2 > 1 loop
                alter table PRODUCT_INFO_TAB clear cascade;
                alter table PRODUCT_INFO_TAB_CLOB clear cascade;
                alter table ERR_TRANSFER_LOG clear cascade;
                alter table SUCC_TRANSFER_LOG clear cascade;
                alter table USER_ACCOUNT clear cascade;
                alter table CMCC_USER_INFO clear cascade;
                alter table USER_ORDER_INFO clear cascade;
                alter table USER_ORDER_INFO_CLOB clear cascade;
                send_msg('clear done!');
                sleep(30000);
            end loop;
            end;
    """
    try:
        con.short_execute_sql(sql)
    except Exception:
        clear_sql()


def main_insert(n):
    for a in range(n):
        '''每个节点做不同表的insert'''
        p_in_1 = mp.Process(target=do_insert_cmcc_user_info, args=(a, port[0]))
        p_in_2 = mp.Process(target=do_insert_cmcc_user_info, args=(a, port[1]))
        p_in_3 = mp.Process(target=do_insert_cmcc_user_info, args=(a, port[2]))
        p_in_4 = mp.Process(target=do_insert_cmcc_user_info, args=(a, port[3]))
        p_in_1.start()
        p_in_2.start()
        p_in_3.start()
        p_in_4.start()


def main_update(n):
    for a in range(n):
        '''每个节点做不同表的update'''
        p_up_1 = mp.Process(target=do_update_diy)
        p_up_2 = mp.Process(target=do_update_diy)
        p_up_3 = mp.Process(target=do_update_diy)
        p_up_4 = mp.Process(target=do_update_diy)

        p_up_1.start()
        p_up_2.start()
        p_up_3.start()
        p_up_4.start()


def main_trans(n):
    for a in range(n):
        p_trans_1 = mp.Process(target=transfer_pro)
        p_trans_2 = mp.Process(target=transfer_pro)
        p_trans_3 = mp.Process(target=transfer_pro)
        p_trans_4 = mp.Process(target=transfer_pro)

        p_trans_1.start()
        p_trans_2.start()
        p_trans_3.start()
        p_trans_4.start()


def main_order_product(n):
    for a in range(n):
        p_order_product_1 = mp.Process(target=call_order_product)
        p_order_product_2 = mp.Process(target=call_order_product)
        p_order_product_3 = mp.Process(target=call_order_product)
        p_order_product_4 = mp.Process(target=call_order_product)
        p_order_product_1.start()
        p_order_product_2.start()
        p_order_product_3.start()
        p_order_product_4.start()


def main_call_cancel_account(n):
    for a in range(n):
        p_order_product_1 = mp.Process(target=call_cancel_account)
        p_order_product_2 = mp.Process(target=call_cancel_account)
        p_order_product_3 = mp.Process(target=call_cancel_account)
        p_order_product_4 = mp.Process(target=call_cancel_account)
        p_order_product_1.start()
        p_order_product_2.start()
        p_order_product_3.start()
        p_order_product_4.start()


def main_order_product_clob(n):
    for a in range(n):
        p_order_product_1 = mp.Process(target=call_order_product_clob)
        p_order_product_2 = mp.Process(target=call_order_product_clob)
        p_order_product_3 = mp.Process(target=call_order_product_clob)
        p_order_product_4 = mp.Process(target=call_order_product_clob)
        p_order_product_1.start()
        p_order_product_2.start()
        p_order_product_3.start()
        p_order_product_4.start()


def main_call_cancel_account_clob(n):
    for a in range(n):
        p_order_product_1 = mp.Process(target=call_cancel_account_clob)
        p_order_product_2 = mp.Process(target=call_cancel_account_clob)
        p_order_product_3 = mp.Process(target=call_cancel_account_clob)
        p_order_product_4 = mp.Process(target=call_cancel_account_clob)
        p_order_product_1.start()
        p_order_product_2.start()
        p_order_product_3.start()
        p_order_product_4.start()


def main_delete(n):
    for a in range(n):
        p_d_1 = mp.Process(target=delete_sql)

        p_d_1.start()


def main_clear_sql(n):
    for a in range(n):
        p_d_1 = mp.Process(target=clear_sql)

        p_d_1.start()


def main():
    print('begin run...')
    time.sleep(1)
#    clob_run()
    main_insert(20)
    main_trans(20)
    main_update(20)
    main_order_product(20)
    main_order_product_clob(20)
    main_delete(20)
    main_call_cancel_account(20)
    main_call_cancel_account_clob(20)
    # main_clear_sql(20)


if __name__ == '__main__':
    opt = int(input('please input your option with 1:建库建表/2:执行业务程序:'))
    if opt == 1:
        do_create_upbms('jdbc:kunlun://192.168.3.139:35690/sysdb')
        exec_sql_from_file(con_class0)
    elif opt == 2:
        server_p = mp.Process(target=socket_server_for_statistics, args=('192.168.3.118', 2000, 56789,))
        server_p.start()
        main_p = mp.Process(target=main)
        main_p.start()
        main_p.join()
        socket_client_for_statistics('192.168.3.118', 'over', 56789)
    else:
        print('please input your option with 1:建库建表/2:执行业务程序:!')
