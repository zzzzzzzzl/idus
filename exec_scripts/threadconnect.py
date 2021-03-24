from datetime import *
import jaydebeapi
import threading as td
from EXECUTING_SQL import *
from Table_data import *
from concurrent import futures


class my_execsql1():
    def __init__(self, url, driver, jar_file, user, passwd):
        self.__url__ = url
        self.__driver__ = driver
        self.__jar_file__ = jar_file
        self.__user__ = user
        self.__passwd__ = passwd

    def short_execute_sql(self, exec_sql, n=5, oper=1, a_out=0):
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
                # for i in range(n):
                #     p = td.Thread(target=g_curs.execute, args=(exec_sql,))
                #     p.start()
                #     # g_conn.commit()
                g_curs.execute(exec_sql)
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


def do_insert_cmcc_user_info(con, thread_id, my_port):
    i = 0
    while True:
        try:
            sql = DiyBusiness().insert_sql_cmcc_user_info(i, str(thread_id).zfill(3), str(my_port))
            con.short_execute_sql(sql)
            i = i + 1

        except Exception:
            break


if __name__ == '__main__':
    url0 = r'jdbc:kunlun://127.0.0.1:2001/UPBMS'
    url1 = r'jdbc:kunlun://127.0.0.1:2001/UPBMS'
    url2 = r'jdbc:kunlun://127.0.0.1:2001/UPBMS'
    url3 = r'jdbc:kunlun://127.0.0.1:2001/UPBMS'
    driver = r'com.kunlun.jdbc.Driver'
    jar_file = r'kunlun_r9.jar'
    user = 'UPBMS'
    passwd = 'UPBMS'

    con_class0 = my_execsql1(url0, driver, jar_file, user, passwd)
    con_class1 = my_execsql1(url1, driver, jar_file, user, passwd)
    con_class2 = my_execsql1(url2, driver, jar_file, user, passwd)
    con_class3 = my_execsql1(url3, driver, jar_file, user, passwd)
    con_list = [con_class0, con_class1, con_class2, con_class3]
    port = ['25690', '26690', '27690', '28690']
    # do_insert_cmcc_user_info(con_class0, 1, port[0])
    g_conn = jaydebeapi.connect(driver, url0, [user, passwd], jar_file)
    g_curs = g_conn.cursor()
    sql = DiyBusiness().insert_sql_cmcc_user_info(1, str(2).zfill(3), port[0])
    # for i in range(5):
    #     p = td.Thread(target=g_curs.execute, args=(sql,))
    #     p.start()
    with futures.ProcessPoolExecutor(15) as executor:
        to_do = []
        for i in range(9):
            future = executor.submit(do_insert_cmcc_user_info, con_class0, 1, port[0])
            to_do.append(future)
        for future in futures.as_completed(to_do):
            future.exception()
