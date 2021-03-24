# -*- coding: utf-8 -*-
'''本文件为各类sql语句执行的方法定义'''
from datetime import *
import jaydebeapi
from Table_data import *

partitions = int(2000)
now_date = datetime.now()
date_1 = datetime(2020, 1, 1, 0, 0, 0)
desc_sql_part = '''
SELECT
COL_NO,
COLUMN_NAME,
case when scale is null
        then name
else
        NAME||'('||SCALE||')'
end DATA_TYPE,
IS_NULL,
DEF_VAL FROM (
SELECT
C.COL_NO,
C.COL_NAME COLUMN_NAME,
CASE WHEN C.TYPE_NAME = 'CHAR' AND C."VARYING" = 'F'
        THEN 'CHAR'
WHEN C.TYPE_NAME = 'CHAR' AND C."VARYING" = 'T'
        THEN 'VARCHAR'
WHEN C.TYPE_NAME ='NUMERIC' AND C.SCALE <=0
        THEN 'INTEGER'
ELSE C.TYPE_NAME
END NAME,
CASE WHEN C.TYPE_NAME = 'NUMERIC' AND C.SCALE > 0
        THEN TRUNC(C.SCALE/65536)||','||MOD(C.SCALE,65536)
WHEN C.TYPE_NAME = 'CHAR'
        THEN TO_CHAR(C.SCALE)
ELSE NULL
END SCALE,
case WHEN C.NOT_NULL='F'
        THEN 'NO' ELSE 'YES'
END IS_NULL,
case when C.DEF_VAL is null
        then ' ' else c.def_val
end def_val,
C.COL_NO FROM
ALL_SCHEMAS S, ALL_TABLES T, ALL_COLUMNS C WHERE S.SCHEMA_ID=T.SCHEMA_ID AND 
T.TABLE_ID=C.TABLE_ID AND S.SCHEMA_NAME = '''

desc_sql_part_r9 = '''
SELECT
C.COL_NO,
C.COL_NAME COLUMN_NAME,
CASE WHEN C.TYPE_NAME = 'CHAR' AND C."VARYING" = 'F'
        THEN 'CHAR'
WHEN C.TYPE_NAME = 'CHAR' AND C."VARYING" = 'T'
        THEN 'VARCHAR'
WHEN C.TYPE_NAME ='NUMERIC' AND C.SCALE <=0
        THEN 'INTEGER'
ELSE C.TYPE_NAME
END NAME,
CASE WHEN C.TYPE_NAME = 'NUMERIC' AND C.SCALE > 0
        THEN TRUNC(C.SCALE/65536)||','||MOD(C.SCALE,65536)
WHEN C.TYPE_NAME = 'CHAR'
        THEN TO_CHAR(C.SCALE)
ELSE NULL
END SCALE,
case WHEN C.NOT_NULL='F'
        THEN 'NO' ELSE 'YES'
END IS_NULL,
case when C.DEF_VAL is null
        then ' ' else c.def_val
end def_val,
C.COL_NO FROM
ALL_SCHEMAS S, ALL_TABLES T, ALL_COLUMNS C WHERE S.SCHEMA_ID=T.SCHEMA_ID AND 
T.TABLE_ID=C.TABLE_ID AND S.SCHEMA_NAME = '''


class my_execsql():
    def __init__(self, url, driver, jar_file, user, passwd):
        self.__url__ = url
        self.__driver__ = driver
        self.__jar_file__ = jar_file
        self.__user__ = user
        self.__passwd__ = passwd

    def short_execute_sql(self, exec_sql, oper=1, a_out=0):
        # short connect:短连(先建jdbc连接再执行sql然后断开连接)
        """全局化conn和curs 使得在异常时也可以调用到这2个参数"""
        global g_curs, g_conn
        try:
            g_conn = jaydebeapi.connect(self.__driver__, self.__url__, [self.__user__, self.__passwd__],
                                        self.__jar_file__)
            g_curs = g_conn.cursor()
            if oper == 0:   
                col_list = []
                g_curs.execute(exec_sql)
                des_list = [str(a) for a in g_curs.description]
                col_name = '  '.join(des_list)
                res = g_curs.fetchall()
                g_curs.close()
                g_conn.close()
                for a in res:
                    b = [str(i) for i in a]
                    str_val = "  ".join(b)
                    col_list.append(str_val)
                sql_data = "\n".join(col_list)
                return col_name, sql_data, res

            elif oper == 1:
                g_curs.execute(exec_sql)
                g_conn.commit()
                g_curs.close()
                g_conn.close()
            else:
                print('oper err !: please input oper as 0(表示语句有结果输出)/1(表示语句无结果输出)')

        except Exception as e:
            if a_out == 0:
                print('\33[31m%s\33[0m' % str(e))
                log = 'my_db_err: ' + self.__url__ + ' ' + str(e) + "\n" + 'sql: ' + str(exec_sql) + "\n\n"
                with open('my_db_err.log', 'a+') as f:
                    f.write(log)
            if g_conn:
                g_curs.close()
                g_conn.close()
            return

    # 语句根据具体情况改

    '''table data of CMCC_USER_INFO'''

    def INSERT_SQL_CMCC_USER_INFO(self, a, thread):
        insert_data = ' values(' + "\n" + \
                      "'" + now_date.strftime('%Y%m%d%H%M%S') + str(thread) + str(a) + "'" + ",\n" + \
                      'callnumber.nextval' + ",\n" + \
                      "'" + china_context(random.randint(2, 5), 'context') + "'" + ",\n" + \
                      '0' + ",\n" + \
                      "TO_DATE('" + str(date_1 + timedelta(days=random.randint(0, partitions - 2)))[
                                    0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS')" + ",\n" + \
                      "'" + sex_ran() + "'" + ",\n" + \
                      "'" + china_context(100, 'context') + 'b-2-京' + random_str(100) + "'" + ",\n" + \
                      'IDENTIFICATION.nextval' + ')'

        sql = 'insert into ' + 'CMCC_USER_INFO' + insert_data

        return sql

    '''为新用户开通账户'''

    '''同步更新用户表和账户表 15rows/t'''

    def UPDATE_SQL_USER_ACCOUNT(self):
        update_date = '''
        begin
        update USER_ACCOUNT set ACCOUNTID = acc_id.nextval,
                STATUS = 1,
                BALANCE = ''' + Balance() + ' where STATUS = 0 and rownum < 16;' + '\n' + 'update CMCC_USER_INFO set ' \
                                                                                          'status = 1 where STATUS = ' \
                                                                                          '0 and rownum < 6;end;'
        return update_date

    def transfer_pro(self):
        sql = "call SP_TRANSFER_MONEY('USER_ACCOUNT','USER_ACCOUNT'," + str(
            random.randint(100000000000000000, 100000000000100000)) + ',' + str(
            random.randint(100000000000000000, 100000000000100000)) + ',' + str(
            Balance()) + ',' + "'" + 'BALANCE' + "'" + ',' + "'" + 'IDENTIFICATION' + "'" + ")"
        return sql

    # 运行多次短连
    def run_many(self, exec_sql, t, oper=1):
        i = 0
        while True:
            i = i + 1
            self.short_execute_sql(exec_sql, oper)
            if i == int(t):
                break

    # long connect:长连(先建jdbc连接再多次执行sql最后断开连接)
    def long_execute_sql(self, exec_sql, t):
        i = 0
        try:
            conn = jaydebeapi.connect(self.__driver__, self.__url__, [self.__user__, self.__passwd__],
                                      self.__jar_file__)
            curs = conn.cursor()
            while True:
                try:
                    curs.execute(exec_sql)
                    print('execute ok !')
                    if i == int(t):
                        curs.close()
                        conn.close()
                        break
                except Exception as e:
                    log = 'my_db_err: ' + self.__url__ + ' ' + str(e) + "\n" + 'sql: ' + exec_sql + "\n\n"
                    with open('my_db_err.log', 'a+') as f:
                        f.write(log)
                    print('\33[31m%s\33[0m' % str(e))

        except Exception as e:
            print('\33[31m%s\33[0m' % str(e))
            log = 'my_connect_err: ' + self.__url__ + ' ' + str(e) + "\n" + 'sql: ' + exec_sql + "\n\n"
            with open('my_connect_err.log', 'a+') as f:
                f.write(log)

                # 执行并查询结果

    def pcons_data(self, exec_sql, oper):

        try:
            if oper == 0:
                col_name, data = self.short_execute_sql(exec_sql, oper=oper)[0], \
                                 self.short_execute_sql(exec_sql, oper=oper)[2]
                col_list = [col_name]
                for a in data:
                    b = [str(i) for i in a]
                    str_val = "  ".join(b)
                    col_list.append(str_val)
                sql_data = "\n".join(col_list)
                return sql_data
            elif oper == 1:
                self.short_execute_sql(exec_sql, oper=oper)
            else:
                raise Exception('please input oper with 0/1!')
        except Exception as e:
            print('err: ' + str(e) + "\n" + 'sql: ' + exec_sql)

    # 数据导出
    def transfer_data(self, table_name, exec_sql):

        try:
            data = self.short_execute_sql(exec_sql, oper=0)[2]
            print(table_name + ' data is transferring ...')
            col_list = []
            file_name = table_name + '_data'
            with open(file_name, 'w') as f:
                for a in data:
                    b = [str(i) for i in a]
                    str_val = "@^|^@".join(b)
                    col_list.append(str_val)
                sql_data = "\n".join(col_list)
                f.write(sql_data)
            print(table_name + 'transfer ok !')
        except Exception as e:
            print(str(e) + ' : table name : ' + table_name)

    # 按数据导出的方式导入数据
    def import_data(self, schema, table_name):
        try:
            desc_sql = desc_sql_part + "'" + schema.upper() + "'" + ' AND TABLE_NAME = ' + "'" + table_name.upper() + \
                       "'" + ' ) ORDER BY COL_NO'
            print(table_name + ' data is importing ..')
            file_name = table_name + '_data'
            str1 = r'\n'
            with open(file_name, 'r', encoding='UTF-8') as f:
                if not self.short_execute_sql(desc_sql, 0):
                    print('NO FOUND TABLE ' + table_name)
                else:
                    for row_nums, line in enumerate(f.readlines()):
                        line = line.strip(str1).split('@^|^@')
                        col_list = []
                        for num, a in enumerate(self.short_execute_sql(desc_sql, 0)):
                            b = [str(i) for i in a]
                            type_name = b[2]
                            if 'VARCHAR' in type_name or 'DATE' in type_name or 'STAMP' in type_name:
                                new_val = "'" + line[num] + "'"
                                if 'None' in new_val:
                                    new_val = 'Null'
                                    col_list.append(new_val)
                                else:
                                    col_list.append(new_val)
                            else:
                                new_val = line[num]
                                if 'None' in new_val:
                                    new_val = 'Null'
                                    col_list.append(new_val)
                                else:
                                    col_list.append(new_val)
                        values_col = ','.join(col_list)
                        insert_sql = 'insert into ' + table_name.upper() + ' values(' + values_col + ')'
                        self.short_execute_sql(insert_sql, 1)
                        if row_nums >= 10000 and row_nums % 10000 == 0:
                            print(table_name + ': ' + str(row_nums) + ' inserted')
                    print(file_name + ' ' + str(row_nums + 1) + ' rows inserted ok !')
        except jaydebeapi.DatabaseError as e:
            print(str(e) + ' : table name : ' + table_name + ' data_line :' + str(row_nums + 1))
            print('sql:' + insert_sql)

    def import_data_common(self, schema, table_name, file_name, str_com):
        try:
            desc_sql = desc_sql_part_r9 + "'" + schema.upper() + "'" + ' AND TABLE_NAME = ' + "'" + table_name.upper() + \
                       "'" + '  ORDER BY COL_NO'
            print(table_name + ' data is importing ..')
            str1 = r'\n'
            with open(file_name, 'r', encoding='UTF-8') as f:
                if not self.short_execute_sql(desc_sql, 0):
                    print('NO FOUND TABLE ' + table_name)
                else:
                    for row_nums, line in enumerate(f.readlines()):
                        line = line.strip(str1).split(str_com)
                        col_list = []
                        for num, a in enumerate(self.short_execute_sql(desc_sql, 0)):
                            b = [str(i) for i in a]
                            print(b)
                            type_name = b[2]
                            if 'VARCHAR' in type_name or 'DATE' in type_name or 'STAMP' in type_name:
                                new_val = "'" + line[num] + "'"
                                if 'None' in new_val:
                                    new_val = 'Null'
                                    col_list.append(new_val)
                                else:
                                    col_list.append(new_val)
                            else:
                                new_val = line[num]
                                if 'None' in new_val:
                                    new_val = 'Null'
                                    col_list.append(new_val)
                                else:
                                    col_list.append(new_val)
                        values_col = ','.join(col_list)
                        insert_sql = 'insert into ' + table_name.upper() + ' values(' + values_col + ')'
                        print(insert_sql)
                        self.short_execute_sql(insert_sql, 1)
                        if row_nums >= 10000 and row_nums % 10000 == 0:
                            print(table_name + ': ' + str(row_nums) + ' inserted')
                    print(file_name + ' ' + str(row_nums + 1) + ' rows inserted ok !')
        except jaydebeapi.DatabaseError as e:
            print(str(e) + ' : table name : ' + table_name + ' data_line :' + str(row_nums + 1))
            print('sql:' + insert_sql)

    def create_upbms(self):
        SQL_list = ['create database  UPBMS', 'use UPBMS', "create user UPBMS identified by 'UPBMS'",
                    'grant dba to UPBMS']
        try:
            conn = jaydebeapi.connect(self.__driver__, self.__url__, [self.__user__, self.__passwd__],
                                      self.__jar_file__)
            curs = conn.cursor()
            for exec_sql in SQL_list:
                try:
                    curs.execute(exec_sql)
                    print(str(exec_sql) + ' ok !')
                except Exception as e:
                    log = 'my_db_err: ' + self.__url__ + ' ' + str(e) + "\n" + 'sql: ' + str(exec_sql) + "\n\n"
                    with open('my_db_err.log', 'a+') as f:
                        f.write(log)
                    print('\33[31m%s\33[0m' % str(e))
            curs.close()
            conn.close()

        except Exception as e:
            print('\33[31m%s\33[0m' % str(e))
            log = 'my_connect_err: ' + self.__url__ + ' ' + str(e) + "\n\n"
            with open('my_connect_err.log', 'a+') as f:
                f.write(log)


def do_create_upbms(url):
    driver = r'com.kunlun.jdbc.Driver'
    jar_file = r'kunlun_r9.jar'
    user = 'SYSDBA'
    passwd = 'SYSDBA'
    con_sys = my_execsql(url, driver, jar_file, user, passwd)
    con_sys.create_upbms()


def read_sqlfile(file):
    """读取文件中的sql"""
    sp_str = '/\n'
    new_lines = []
    use_sql_list = []
    with open(file, encoding='utf-8') as f:
        lines = f.readlines()
        for elem in lines:
            if elem == sp_str:
                new_lines.append(elem)
            else:
                new_lines.append(elem.strip('\n'))
        sp_lines = '\n'.join(new_lines).split(sp_str)
        for sql_str in sp_lines:
            if 'end;\n' in sql_str[-8:] or 'END;\n' in sql_str[-8:]:
                use_sql_list.append(sql_str.strip('\n'))
            else:
                use_sql_list.append(sql_str.strip(';\n').strip('\n'))
        while '' in use_sql_list:
            use_sql_list.remove('')
        return use_sql_list


if __name__ == '__main__':
    url0 = r'jdbc:kunlun://192.168.3.138:25690/SYSDB'
    # url1 = r'jdbc:kunlun://192.168.3.138:6690/UPBMS'
    # url2 = r'jdbc:kunlun://192.168.3.138:7690/UPBMS'
    driver = r'com.kunlun.jdbc.Driver'
    jar_file = r'/home/zl/jm/kunlun_r9.jar'
    user = 'SYSDBA'
    passwd = 'SYSDBA'
    sql = 'select NODE_ID,ZONE_ID,KFS_PUT_POS,KFS_WRT_POS,KFS_CKPT,REDO_PUT_POS,REDO_WRT_POS,REDO_CKPT from sys.sys_server_zones'
    con_class0 = my_execsql(url0, driver, jar_file, user, passwd)
    print(con_class0.short_execute_sql(sql, oper=0))
