# -*- coding: utf-8 -*-

from EXECUTE_CLS import *
from EXECUTING_SQL import *
from SOCKET_SERVER_FOR_STATISTICS import *
from exec_scripts.OV_SQL_CLOB import main as clob_run
import multiprocessing as mp

url0 = r'jdbc:kunlun://127.0.0.1:2001/UPBMS'
url1 = r'jdbc:kunlun://127.0.0.1:2001/UPBMS'
url2 = r'jdbc:kunlun://127.0.0.1:2001/UPBMS'
url3 = r'jdbc:kunlun://127.0.0.1:2001/UPBMS'
driver = r'com.kunlun.jdbc.Driver'
jar_file = r'kunlun_r9.jar'
user = 'UPBMS'
passwd = 'UPBMS'

con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
con_class1 = my_execsql(url1, driver, jar_file, user, passwd)
con_class2 = my_execsql(url2, driver, jar_file, user, passwd)
con_class3 = my_execsql(url3, driver, jar_file, user, passwd)
con_list = [con_class0, con_class1, con_class2, con_class3]
port = ['25690', '26690', '27690', '28690']


def sel_con():
    new_con_list = []
    v_sql = 'select 1 from dual'
    for con in con_list:
        try:
            con.short_execute_sql(v_sql, a_out=1)
            new_con_list.append(con)
        except Exception:
            pass
    return new_con_list


def do_insert_cmcc_user_info(con, thread_id, my_port):
    i = 0
    while True:
        try:
            sql = DiyBusiness().insert_sql_cmcc_user_info(i, str(thread_id).zfill(3), str(my_port))
            con.short_execute_sql(sql)
            i = i + 1

        except Exception:
            break


def do_update_diy(con):
    i = 0
    j = 0
    while True:
        try:
            time.sleep(3)
            sql = DiyBusiness().update_sql_user_account(i)
            con.short_execute_sql(sql)
            i = i + 1
            j = j + 1
            if j == 1000:
                socket_client_for_statistics('192.168.3.118', 'do_update_diy--' + str(j), 12345)
                j = 0
        except Exception:
            socket_client_for_statistics('192.168.3.118', 'do_update_diy--' + str(j), 12345)
            break


def transfer_pro(con):
    i = 0
    while True:
        try:
            sql = DiyBusiness().transfer_pro()
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'transfer_pro--' + str(i), 12345)
                i = 0
        except Exception:
            socket_client_for_statistics('192.168.3.118', 'transfer_pro--' + str(i), 12345)
            break


def delete_sql(con):
    table_list = ['ERR_TRANSFER_LOG', 'SUCC_TRANSFER_LOG']
    i = 0
    while True:
        try:
            sql = DiyBusiness().del_data_with_date(table_list[random.randint(0, len(table_list) - 1)])
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'delete_sql--' + str(i), 12345)
                i = 0
        except Exception:
            socket_client_for_statistics('192.168.3.118', 'delete_sql--' + str(i), 12345)
            break


def exec_sql_from_file(con):
    for sql in read_sqlfile('sql_mk/DIY_SQL1'):
        con.short_execute_sql(sql)
        print(sql + ' do ok!')


def call_order_product(con):
    i = 0
    while True:
        try:
            sql = 'call ORDER_PRODUCT'
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'call_ORDER_PRODUCT--' + str(i), 12345)
                i = 0
        except Exception:
            socket_client_for_statistics('192.168.3.118', 'call_ORDER_PRODUCT--' + str(i), 12345)
            break


def call_cancel_account(con):
    i = 0
    while True:
        try:
            sql = 'call cancel_account'
            con.short_execute_sql(sql)
            i = i + 1
            if i == 1000:
                socket_client_for_statistics('192.168.3.118', 'call_cancel_account--' + str(i), 12345)
                i = 0
        except Exception:
            socket_client_for_statistics('192.168.3.118', 'call_cancel_account--' + str(i), 12345)
            break


def clear_sql(con):
    sql = """
            declare
            i int;
            begin
            i := 2;
            while i > 1 loop
                    alter table PRODUCT_INFO_TAB clear cascade;
                            alter table ERR_TRANSFER_LOG clear cascade;
                            alter table SUCC_TRANSFER_LOG clear cascade;
                            alter table USER_ACCOUNT clear cascade;
                            alter table CMCC_USER_INFO clear cascade;
                            alter table USER_ORDER_INFO clear cascade;
                            send_msg('clear done!');
                            sleep(3000);
            end loop;
            end;
    """
    try:
        con.short_execute_sql(sql)
    except Exception:
        return


def main_insert(n):
    print('do_insert_cmcc_user_info start!')
    for a in range(n):
        '''每个节点做不同表的insert'''
        p_in_1 = mp.Process(target=do_insert_cmcc_user_info,
                            args=(con_list[random.randint(0, len(con_list) - 1)], a, port[0]))
        p_in_1.start()


def main_update(n):
    print('do_update_diy start!')
    for a in range(n):
        '''每个节点做不同表的update'''
        p_up_1 = mp.Process(target=do_update_diy, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_up_2 = mp.Process(target=do_update_diy, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_up_3 = mp.Process(target=do_update_diy, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_up_4 = mp.Process(target=do_update_diy, args=(con_list[random.randint(0, len(con_list) - 1)],))

        p_up_1.start()
        p_up_2.start()
        p_up_3.start()
        p_up_4.start()


def main_trans(n):
    print('transfer_pro start!')
    for a in range(n):
        p_trans_1 = mp.Process(target=transfer_pro, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_trans_2 = mp.Process(target=transfer_pro, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_trans_3 = mp.Process(target=transfer_pro, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_trans_4 = mp.Process(target=transfer_pro, args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_trans_1.start()
        p_trans_2.start()
        p_trans_3.start()
        p_trans_4.start()


def main_order_product(n):
    print('call_order_product start!')
    for a in range(n):
        p_order_product_1 = mp.Process(target=call_order_product,
                                       args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_order_product_2 = mp.Process(target=call_order_product,
                                       args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_order_product_3 = mp.Process(target=call_order_product,
                                       args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_order_product_4 = mp.Process(target=call_order_product,
                                       args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_order_product_1.start()
        p_order_product_2.start()
        p_order_product_3.start()
        p_order_product_4.start()


def main_delete(n):
    print('delete_sql start!')
    for a in range(n):
        p_d_1 = mp.Process(target=delete_sql, args=(con_list[random.randint(0, len(con_list) - 1)],))

        p_d_1.start()


def main_call_cancel_account(n):
    print('call_cancel_account start!')
    for a in range(n):
        p_order_product_1 = mp.Process(target=call_cancel_account,
                                       args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_order_product_2 = mp.Process(target=call_cancel_account,
                                       args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_order_product_3 = mp.Process(target=call_cancel_account,
                                       args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_order_product_4 = mp.Process(target=call_cancel_account,
                                       args=(con_list[random.randint(0, len(con_list) - 1)],))
        p_order_product_1.start()
        p_order_product_2.start()
        p_order_product_3.start()
        p_order_product_4.start()


def main_clear_sql(n):
    print('clear_sql start!')
    for a in range(n):
        p_d_1 = mp.Process(target=clear_sql, args=(con_list[random.randint(0, len(con_list) - 1)],))

        p_d_1.start()


def main():
    print('begin run...')
    time.sleep(1)
    # clob_run()
    main_insert(5)
    # main_trans(50)
    # main_update(50)
    # main_order_product(50)
    # main_delete(50)
    # main_call_cancel_account(50)
    # main_clear_sql(10)


if __name__ == '__main__':
    # opt = int(input('please input your option with 1:建库建表/2:执行业务程序:'))
    # if opt == 1:
    #     do_create_upbms('jdbc:kunlun://127.0.0.1:2001/system')
    #     exec_sql_from_file(con_class0)
    # elif opt == 2:
    #     main_p = mp.Process(target=main)
    #     main_p.start()
    #     main_p.join()
    # else:
    #     print('please input your option with 1:建库建表/2:执行业务程序:!')
    main_p = mp.Process(target=main)
    main_p.start()
    main_p.join()
