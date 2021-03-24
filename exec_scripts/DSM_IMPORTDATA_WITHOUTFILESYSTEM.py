# -*- coding: utf-8 -*-

from EXECUTE_CLS import *

url0 = r'jdbc:kunlun://192.168.3.131:5690/UPBMS'
url1 = r'jdbc:kunlun://192.168.3.139:6690/UPBMS'
driver = r'com.kunlun.jdbc.Driver'
jar_file = r'/home/zl/jm/kunlun_r9.jar'
user = 'UPBMS'
passwd = 'UPBMS'

con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
con_class1 = my_execsql(url1, driver, jar_file, user, passwd)
url_list = [con_class0, con_class1]


def dsm_importdata_withwritebuffer(con, thread_id):
    sql = """
                declare 
                sto varchar;
                iops int;
                begin
                    SYS.DBMS_IOPS.TEST_DSM_WRITE_BUFF(5000000, iops, sto);
                    insert into write_store values(sto,iops);
                end;
            """
    con.short_execute_sql(sql)
    print('write_buffer' + '-' + str(thread_id).zfill(3) + ' ok!')


def dsm_importdata_withreadbuffer(con, thread_id):
    sql = """
                declare 
                sto varchar;
                iops int;
                is_err int;
                begin
                    select sto_id into sto from write_store;
                    SYS.DBMS_IOPS.TEST_DSM_READ_BUFF(sto, iops, is_err);
                    insert into read_store values(sto,iops,is_err);
                end;
            """
    con.short_execute_sql(sql)
    print('read_buffer' + '-' + str(thread_id).zfill(3) + ' ok!')


def create_tab(con):
    sql = ['create table write_store(sto_id varchar(64), iops int)',
           'create table read_store(sto_id varchar(64), iops int, is_err int)']
    for i, elem in enumerate(sql):
        con.short_execute_sql(elem)
        print(elem + ' do ok !')


def main():
    import multiprocessing as mp

    for a in range(324):
        '''每个节点做不同表的insert'''
        pwrite = mp.Process(target=dsm_importdata_withwritebuffer,
                            args=(url_list[random.randint(0, len(url_list) - 1)], a,))
        pwrite.start()


if __name__ == '__main__':
    opt = int(input('please input your option with 1/2:'))
    if opt == 1:
        do_create_upbms('jdbc:kunlun://192.168.3.131:5690/sysdb')
        create_tab(con_class0)
    elif opt == 2:
        main()
    else:
        print('please input your option with 1/2!')
