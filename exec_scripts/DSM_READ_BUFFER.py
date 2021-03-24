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


def dsm_importdata_withreadbuffer(con, thread_id):
    sql = """
                declare 
                 sto varchar;
                 iops int;
                 is_err int;
                 begin
                    select sto_id into sto from write_store order by STO_ID  limit """ + str(thread_id) + """,1;
                    dbms_output.put_line(sto);
                    SYS.DBMS_IOPS.TEST_DSM_READ_BUFF(sto, iops, is_err);
                    insert into read_store values(sto,iops,is_err);
                    commit;
                 end;
            """
    con.short_execute_sql(sql)
    print('write_buffer' + '-' + str(thread_id).zfill(3) + ' ok!')


def main():
    import multiprocessing as mp

    for a in range(321):
        '''每个节点做不同表的insert'''
        pread1 = mp.Process(target=dsm_importdata_withreadbuffer,
                            args=(con_class0, a,))
        pread1.start()
        pread2 = mp.Process(target=dsm_importdata_withreadbuffer,
                            args=(con_class1, a,))
        pread2.start()


if __name__ == '__main__':
    main()
