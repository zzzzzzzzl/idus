# -*- coding: utf-8 -*-
"""本文件为各类sql语句的拼接定义"""
from datetime import *

from Table_data import *

partitions = int(2000)
now_date = datetime.now()
date_1 = datetime(2020, 1, 1, 0, 0, 0)


class BJCMCC:
    """"北京八张表的数据插入语句"""

    def __init__(self, table_name):
        self.__table_name__ = table_name

    def insert_sql_cmcc(self, a, thread):
        insert_data = ' values(' + "\n" + \
                      "'" + now_date.strftime('%Y%m%d%H%M%S') + str(thread) + str(a) + "'" + ",\n" + \
                      "'" + callNumber() + "'" + ",\n" + \
                      "'" + china_context(1000, 'context') + 'b-2-京' + random_str(200) + "'" + ",\n" + \
                      "'" + str(random.randint(10, 99)) + 'c-3-' + china_context(1, 'context') + "'" + ",\n" + \
                      '1' + ",\n" + \
                      "TO_DATE('" + str(now_date + timedelta(days=random.randint(0, partitions)))[
                                    0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS')" + ",\n" + \
                      "TO_DATE('" + str(now_date + timedelta(days=random.randint(0, partitions)))[
                                    0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS')" + ",\n" + \
                      "'" + random_str(100) + 'd-3-' + random_str(100) + "'" + ",\n" + \
                      "'" + random_str(10) + 'e-4-' + random_str(10) + "'" + ",\n" + \
                      str(random.randint(0, 1)) + ",\n" + \
                      "'" + str(random.randint(10, 99)) + 'f-5-' + china_context(1, 'context') + str(
            random.randint(10, 99)) + "'" + ",\n" + \
                      "'" + str(random.randint(1000, 9999)) + 'g-6-' + china_context(1, 'context') + random_spec_str(
            100) + "'" + ",\n" + \
                      "TO_DATE('" + str(now_date + timedelta(days=random.randint(0, partitions)))[
                                    0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS')" + ",\n" + \
                      "'" + random_lower_str(15) + "'" + ",\n" + \
                      str(random.randint(0, 9)) + ",\n" + \
                      str(random.randint(0, 9999)) + ",\n" + \
                      "'" + random_lower_str(15) + "'" + ",\n" + \
                      "'" + str(random.randint(0, 1)) + "'" + ')'

        sql = 'insert into ' + self.__table_name__ + insert_data
        return sql

    def update_sql_cmcc(self, i):
        """北京八张表的数据更新语句"""
        update_data = ' SET status  = ' + str(random.randint(0, 99)) + ', repeatcount  = ' + str(i) + \
                      ', endtime = sysdate WHERE STATUS = ' + str(random.randint(10, 999))
        update_sql = 'UPDATE /*+ index(IDX_' + self.__table_name__ + '_MOBILE)*/ ' + self.__table_name__ + update_data
        return update_sql

    def update_sql_index(self):
        """北京移动八张表强制走index优化update语句"""
        update_data = 'UPDATE /*+ index( s IDX_ ' + self.__table_name__ + '_MOBILE )*/' + self.__table_name__ + ' s SET' + '''
                                s.isreply = 2,
                                s.statusreporttime = sysdate,
                                s.status = 2,
                                s.stat =                                           	          
                                    (CASE WHEN INSTR (s.msgid, ',') > 0  
                                    THEN (CASE WHEN s.stat IS NULL  
                                    THEN '56551-DELIVRD'  
                                    ELSE s.stat || ',' || '56551-DELIVRD'      
                                    END)        
                                    ELSE '56551-DELIVRD'                     
                                    END)  WHERE s.status = 1 and rownum < 16 '''
        return update_data


class DiyBusiness:
    """diy业务语句"""

    @staticmethod
    def update_sql_user_account(i):
        """diy业务USER_ACCOUNT开户更新初始余额语句"""
        a = str(10000 + i)
        update_date = 'update_account(' + str(Balance()) + ',' + a + ')'
        return update_date

    @staticmethod
    def transfer_pro():
        """"diy业务转账语句"""
        sql = "call SP_TRANSFER_MONEY('USER_ACCOUNT','USER_ACCOUNT'," + str(
            random.randint(100000000000000000, 100000000000100000)) + ',' + str(
            random.randint(100000000000000000, 100000000000100000)) + ',' + str(
            Balance()) + ',' + "'" + 'BALANCE' + "'" + ',' + "'" + 'IDENTIFICATION' + "'" + ")"
        return sql

    @staticmethod
    def insert_sql_cmcc_user_info(a, thread, port):
        # 'callnumber.nextval' + ",\n" + \   'IDENTIFICATION.nextval'
        """"CMCC_USER_INFO表数据插入语句 """
        insert_data_cmcc_user_info = ' values(' + "\n" + \
                                     "'" + now_date.strftime('%Y%m%d%H%M%S') + str(thread) + str(a) + str(
            port) + "'" + ",\n" + \
                                     'callnumber.nextval' + ",\n" + \
                                     "'" + china_context(random.randint(2, 5), 'context') + "'" + ",\n" + \
                                     '0' + ",\n" + \
                                     'sysdate,\n' + \
                                     "'" + sex_ran() + "'" + ",\n" + \
                                     "'" + china_context(100, 'context') + 'b-2-京' + random_str(100) + "'" + ",\n" + \
                                     'IDENTIFICATION.nextval' + ')'

        sql = 'insert into ' + 'CMCC_USER_INFO' + insert_data_cmcc_user_info + ';\n'
        return sql

    @staticmethod
    def del_data_with_date(tab_name):
        table_list = ['ERR_TRANSFER_LOG', 'SUCC_TRANSFER_LOG']
        if tab_name in table_list:
            sql = 'delete from ' + tab_name + ' where sysdate-TRANSFERDATE > 40/24/60 and rownum < 16'
            return sql
        else:
            print("please input table as 'ERR_TRANSFER_LOG' or 'SUCC_TRANSFER_LOG'")
            raise Exception("Invalid table_name", tab_name)

    def product_info_tab(self):
        PRODUCT_TYPE = ['语音', '视频', '文字', '娱乐', '办公', '虚拟化', '运动']
        SOLD_TYPE = ['day_rent', 'moon_rent', 'year_rent']
        day_rent = str("%.2f" % random.random())
        moon_rent = str("%.2f" % random.random())
        year_rent = str("%.2f" % random.random())
        DISCOUNT = [day_rent, moon_rent, year_rent]
        DISCOUNT_INFO = [day_rent + ' for day_rent', moon_rent + ' for moon_rent', year_rent + ' for year_rent']
        i = random.randint(0, 2)
        table_data = 'insert into PRODUCT_INFO_TAB values' + '(' + \
                     "'" + PRODUCT_TYPE[random.randint(0, len(PRODUCT_TYPE) - 1)] + "'" + ',' + \
                     "'" + china_context(6, 'context') + "'" + ',' + \
                     Balance(100000000) + "," + \
                     "'" + SOLD_TYPE[i] + "'" + ',' + \
                     "'" + china_context(random.randint(2000, 6000), 'context') + "'" + ',' + \
                     "'" + DISCOUNT_INFO[i] + "'" + ',' + \
                     "'" + SOLD_TYPE[i] + "'" + ',' + \
                     "'" + DISCOUNT[i] + "'" + ',' + \
                     "'" + china_context(random.randint(2000, 6000), 'context') + "'" + ',' + \
                     'sysdate' + ')'
        return table_data

    def product_info_tab_clob(self):
        PRODUCT_TYPE = ['语音', '视频', '文字', '娱乐', '办公', '虚拟化', '运动']
        SOLD_TYPE = ['day_rent', 'moon_rent', 'year_rent']
        day_rent = str("%.2f" % random.random())
        moon_rent = str("%.2f" % random.random())
        year_rent = str("%.2f" % random.random())
        DISCOUNT = [day_rent, moon_rent, year_rent]
        DISCOUNT_INFO = [day_rent + ' for day_rent', moon_rent + ' for moon_rent', year_rent + ' for year_rent']
        i = random.randint(0, 2)
        table_data = 'insert into PRODUCT_INFO_TAB_CLOB values' + '(' + \
                     "'" + PRODUCT_TYPE[random.randint(0, len(PRODUCT_TYPE) - 1)] + "'" + ',' + \
                     "'" + china_context(6, 'context') + "'" + ',' + \
                     Balance() + "," + \
                     "'" + SOLD_TYPE[i] + "'" + ',' + \
                     OvAndLob.xml_column() + ',' + \
                     "'" + DISCOUNT_INFO[i] + "'" + ',' + \
                     "'" + SOLD_TYPE[i] + "'" + ',' + \
                     "'" + DISCOUNT[i] + "'" + ',' + \
                     OvAndLob.xml_column() + ',' + \
                     'sysdate' + ')'
        return table_data


class OvAndLob:
    """ov and lob column"""

    @staticmethod
    def ov_cmcc(a, thread, table_name, num=5000):
        """以北京的八张表数据为数据原型,num表示comment字段的大小 = num*2 + 200 + 6"""
        insert_data = ' values(' + "\n" + \
                      "'" + now_date.strftime('%Y%m%d%H%M%S') + str(thread) + str(a) + "'" + ",\n" + \
                      "'" + callNumber() + "'" + ",\n" + \
                      "'" + china_context(num, 'context') + 'b-2-京' + random_str(200) + "'" + ",\n" + \
                      "'" + str(random.randint(10, 99)) + 'c-3-' + china_context(1, 'context') + "'" + ",\n" + \
                      '1' + ",\n" + \
                      "TO_DATE('" + str(now_date + timedelta(days=random.randint(0, partitions)))[
                                    0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS')" + ",\n" + \
                      "TO_DATE('" + str(now_date + timedelta(days=random.randint(0, partitions)))[
                                    0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS')" + ",\n" + \
                      "'" + random_str(100) + 'd-3-' + random_str(100) + "'" + ",\n" + \
                      "'" + random_str(10) + 'e-4-' + random_str(10) + "'" + ",\n" + \
                      str(random.randint(0, 1)) + ",\n" + \
                      "'" + str(random.randint(10, 99)) + 'f-5-' + china_context(1, 'context') + str(
            random.randint(10, 99)) + "'" + ",\n" + \
                      "'" + str(random.randint(1000, 9999)) + 'g-6-' + china_context(1, 'context') + random_spec_str(
            100) + "'" + ",\n" + \
                      "TO_DATE('" + str(now_date + timedelta(days=random.randint(0, partitions)))[
                                    0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS')" + ",\n" + \
                      "'" + random_lower_str(15) + "'" + ",\n" + \
                      str(random.randint(0, 9)) + ",\n" + \
                      str(random.randint(0, 9999)) + ",\n" + \
                      "'" + random_lower_str(15) + "'" + ",\n" + \
                      "'" + str(random.randint(0, 1)) + "'" + ')'

        sql = 'insert into ' + table_name + insert_data
        return sql

    @staticmethod
    def xml_column():
        import create_data
        xml_data = create_data.create_xml_long(random.randint(1, 20), random.randint(1, 30))
        xml_column = 'sys.xmltype.createXML(' + "'" + xml_data + "')"
        return xml_column


class UndoTest:

    def create_undo_table(self, i):
        create_table_sql = 'create table' + ' CMCC_USER_INFO' + str(i) + '''(
            "USRID" VARCHAR(40),
            "MOBILE" VARCHAR(32) NOT NULL ,
            "USER_NAME" VARCHAR(10) NOT NULL ,
            "STATUS" NUMBER DEFAULT 0  NOT NULL ,
            "LOGIN_DATE" DATE DEFAULT SYSDATE NOT NULL ,
            "SEX" VARCHAR(10),
            "LOCATION" VARCHAR(1024),
            "IDENTIFICATION" numeric NOT NULL)
            partition by mod("USRID") partitions 10
        '''
        return create_table_sql

    def insert_loop(self, i):
        sql_v = '''declare
                i int;
                begin
                ''' + \
                "insert into " + "CMCC_USER_INFO" + str(
            i) + " values('20200902105558',1,'萨皇街银蒙',0,TO_DATE('2020-07-04 00:00:00','SYYYY-MM-DD HH24:MI:SS'),'男'," \
                 "'区玛萨依架睛既桌止禁坏船藸急遇速景',IDENTIFICATION.nextval); " + \
                ''' 
                for i in 1..100000 loop
                ''' + 'insert into ' + 'CMCC_USER_INFO' + str(i) + ' values(' + "\n" + \
                "'" + now_date.strftime('%Y%m%d%H%M%S') + "'" + ",\n" + \
                'callnumber.nextval' + ",\n" + \
                "'" + china_context(random.randint(2, 5), 'context') + "'" + ",\n" + \
                '0' + ",\n" + \
                "TO_DATE('" + str(date_1 + timedelta(days=random.randint(0, partitions - 2)))[
                              0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS')" + ",\n" + \
                "'" + sex_ran() + "'" + ",\n" + \
                "'" + china_context(100, 'context') + 'b-2-京' + random_str(100) + "'" + ",\n" + \
                'IDENTIFICATION.nextval' + ');' + '''
                end loop;
                ''' + \
                "insert into " + "CMCC_USER_INFO" + str(
            i) + " values('20200902105558',1,'萨皇街银蒙',0,TO_DATE('2020-07-04 00:00:00','SYYYY-MM-DD HH24:MI:SS'),'男'," \
                 "'区玛萨依架睛既桌止禁坏船藸急遇速景',IDENTIFICATION.nextval); " + \
                '''
                end;
                '''

        return sql_v


if __name__ == '__main__':
    print(DiyBusiness().insert_sql_cmcc_user_info(1, 2, 3))
