# -*- coding: utf-8 -*-

from datetime import *

from Table_data import *


# 创建xml表单
def Create_xml_label(xml_label, xml_val):
    label = random_list(xml_label)
    xml_label = '<' + label + '>' + "\n" + xml_val + "\n" + '<' + '/' + label + '>'
    return xml_label


# 总xml信息---后面可以添加信息内容
def Create_xml_element():
    xml_element = '<name>' + china_context(random.randint(2, 4), 'name') + '</name>' + "\n" + \
                  '<country>' + random_list(country) + '</country>' + "\n" + \
                  '<city>' + random_list(city) + '</city>' + "\n" + \
                  '<localtion>' + random_list(localtion) + '</localtion>' + "\n" + \
                  '<sex>' + sex_ran() + '</sex>' + "\n" + \
                  '<Account_ID>' + str(Account_ID()) + '</Account_ID>' + "\n" + \
                  '<Balance>' + str(Balance()) + '</Balance>' + "\n" + \
                  '<sequenceID>' + str(currentimestamp()) + '</sequenceID>' + "\n" + \
                  '<PhoneNumber>' + str(callNumber()) + '</PhoneNumber>' + "\n" + \
                  '<ID>' + str(identity()) + '</ID>' + "\n" + \
                  '<mail>' + mail() + '</mail>' + "\n" + \
                  '<car>' + random_list(car_list) + '</car>' + "\n" + \
                  '<Phone>' + random_list(phone_list) + '</Phone>' + "\n" + \
                  '<infoURL>' + url_data() + '</infoURL>' + "\n" + \
                  '<CreateDate>' + random_time('year') + '-' + random_time('moon') + '-' + random_time(
        'day') + '</CreateDate>' + "\n" + \
                  '<description>' + china_context(random.randint(10, 15), 'context') + '</description>'
    return xml_element


# 根据数量值随机选取xml信息，可用于多层嵌套
def random_xml_element(num):
    random_element_list = []
    element_list = Create_xml_element().split("\n")
    for i in range(num):
        random_element_list.append(element_list[random.randint(0, len(element_list) - 1)])
    random_element_str = "\n".join(random_element_list)
    return random_element_str


# 生成多个同级节点
def rows_node(num):
    rows_str_list = []
    for i in range(num):
        rows_str_list.append(Create_xml_label(xml_title_list, Create_xml_element()))
    rows_str = "\n".join(rows_str_list)
    return rows_str


# 生成xml数据
def create_xml_long(elems,nodes):
    xml_data_head = '<?xml version="1.0" encoding="utf-8"?>' + "\n"
    xml_body_1 = Create_xml_label(xml_title_list, random_xml_element(elems))
    xml_body_2 = xml_body_1 + "\n" + Create_xml_label(xml_title_list, random_xml_element(elems))
    xml_body_3 = Create_xml_label(xml_title_list, xml_body_2)
    xml_body_4 = xml_body_3 + "\n" + Create_xml_label(xml_title_list, random_xml_element(elems)) + "\n" + rows_node(nodes)
    xml_body_5 = Create_xml_label(xml_label_list, xml_body_4)
    xml_body_6 = xml_data_head + Create_xml_label(xml_label_list, xml_body_5)
    return xml_body_6


# 创建分区表的分区
def Create_tale_par(num, name):
    # 分区字段-按时间分区
    dt = datetime.now()
    partition_list = []

    for i in range(0, num + 1):
        # 当前时间+1天
        dt2 = dt + timedelta(days=i)
        partition_info = 'partition ' + name + "_" + str(dt2.strftime("%Y%m%d")) + " values less than " + "(TO_DATE('" + \
                         str(dt2)[0:19] + "'" + ',' + "'SYYYY-MM-DD HH24:MI:SS','NLS_CALENDAR=GREGORIAN'))"
        partition_list.append(partition_info)
    partition_str = ",\n".join(partition_list)
    return partition_str


# 生成表纯数据文件
def Create_Tabdata_file(idx, filename):
    now_date = datetime.now()
    i = 0
    val_list = []

    RSPCONTENT_list = [
        '{"res_code":"999999","res_desc":{"_defClass":"java.lang.NullPointerException","detailMessage":null,'
        '"cause":null,"stackTrace":[{"declaringClass":"com.huawei.bme.commons.util.proxy.OmProxyUtil",'
        '"methodName":"getOmProxy","fileName":"OmProxyUtil.java","lineNumber":110},'
        '{"declaringClass":"com.huawei.bme.commons.util.trace.TraceMgr","methodName":"removeOverTimeTasks",'
        '"fileName":"TraceMgr.java","lineNumber":396},{"declaringClass":"com.huawei.bme.commons.util.trace.TraceMgr",'
        '"methodName":"commit","fileName":"TraceMgr.java","lineNumber":256},'
        '{"declaringClass":"com.huawei.csc.foundation.adapter.log.trace.TraceServiceImpl","methodName":"commit",'
        '"fileName":"TraceServiceImpl.java","lineNumber":41},'
        '{"declaringClass":"com.huawei.csc.kernel.api.log.trace.TraceMgr","methodName":"commit",'
        '"fileName":"TraceMgr.java","lineNumber":130},{"declaringClass":"com.huawei.ebus.core.trace.LogTrace",'
        '"methodName":"startLogTrace","fileName":"LogTrace.java","lineNumber":196},'
        '{"declaringClass":"com.huawei.ebus.connector.http.HttpConnector",',
        '{"res_code":"0","res_desc":"成功","result":{"BUSIINFOS":{"CUSTID":"6345000300965","CUSTNAME":"刘*",'
        '"ORGNAME":"莱芜","STATUSNAME":"在网","STATUSDATE":"2018-05-03","CERTTYPENAME":"居民身份证",'
        '"CERTID":"130828********533*","CERTSTARTDATE":"","CERTENDDATE":"","LINKADDR":"","POSTCODE":"789450",'
        '"LINKMAN":"","LINKPHONE":"","WORKNAME":"","EDULEVELNAME":"","BIRTHDAY":"","GENDERNAME":"女",'
        '"CUSTTYPENAME":"普通用户","INLEVELNAME":"普通用户","CUSTCLASS1NAME":"普通客户","CUSTCLASS2NAME":"普通客户",'
        '"CREDITLEVEL":"无","CERTADDR":"********","SHORTNAME":"","HOMETEL":"","EMAIL":"","TELNUM":"","OFFICENAME":"",'
        '"OFFICETEL":"","OFFICEADDR":"","MOBILETEL":"","RESERVETEL":"","FOREIGNERNAME":"本地私人","NATIONALITYNAME":"",'
        '"FAVORITENAME":"","NOTES":"","OWNERAREANAME":"","CURRENTCUSTMGR":"","CUSTMGRNAME":"","ISREALNAME":"已认证",'
        '"REALNAMETYPE":"已认证","birthday":"","ownerOrgId":"SD.LP","custName":"刘包","certID":"130828194006265331",'
        '"custType":"PersonCustomer","certType":"IdCard","workId":"']

    while i < idx:
        i += 1

        REQSEQ = str(random.randint(10000000000000000000, 99999999999999999999)) + '+' + str(
            random.randint(0, 24)).zfill(2) + ':' + str(random.randint(0, 999999999)).zfill(9)
        APPID = str(random.randint(0, 999999999))
        APIID = str(random.randint(0, 999999999))
        REQUESTIP = str(random.randint(0, 255)) + '.' + str(random.randint(0, 255)) + '.' + str(
            random.randint(0, 255)) + '.' + str(random.randint(0, 255))
        BEGINTIME = str(now_date - timedelta(days=random.randint(30, 60)))[0:23]
        ENDTIME = str(now_date - timedelta(days=random.randint(0, 30)))[0:19]
        servElapsePeriod = random_str(random.randint(1, 30))
        INTIME = random_time('year') + '-' + random_time('moon') + '-' + random_time('day') + ' ' + str(
            random.randint(0, 23)).zfill(2) + ':' + str(random.randint(0, 59)).zfill(2) + ':' + str(
            random.randint(0, 59)).zfill(2)
        RETCODE = str(i)
        RETMSG = random_str(random.randint(1, 50))
        RSPCONTENT = RSPCONTENT_list[random.randint(0, 1)]
        CHANNELID = str(random.randint(0, 99))
        VERSION = random_str(random.randint(1, 30))
        OID = str(['null', Balance()][random.randint(0, 1)])
        AREACODE = str(['null', Balance()][random.randint(0, 1)])
        ROUTETYPE = str(['null', random.randint(0, 20)][random.randint(0, 1)])
        ROUTEVALUE = '"' + china_context(random.randint(1, 8), 'context') + '"'
        ISCACHE = ['"yes"', '"no"'][random.randint(0, 1)]
        SERVICEID = str(random.randint(0, 999999999))
        SRCCODE = str(random.randint(0, 999999999))

        #    line = REQSEQ + '^' + APPID + '^' + APIID + '^' + REQUESTIP + '^' + BEGINTIME + '^' + ENDTIME + '^' + servElapsePeriod + '^' + INTIME + '^' + RETCODE + '^' + RETMSG + '^' + RSPCONTENT + '^' + CHANNELID + '^' + \
        #           VERSION + '^' + OID + '^' + AREACODE + '^' + ROUTETYPE + '^' + ROUTEVALUE + '^' + ISCACHE + '^' + SERVICEID + '^' + SRCCODE

        line = REQSEQ + '^' + RSPCONTENT + '^' + RSPCONTENT + '^' + REQUESTIP + '^' + REQUESTIP

        val_list.append(line)

    # 切换文件输出目录
    os.chdir(os.getcwd() + r'/result')

    ft = open(filename + '-' + str(idx), 'w+')
    # 列表转为str 以换行连接
    val_str = "\n".join(val_list)

    ft.write(val_str)
    ft.close()


# 建表
def Create_tab_body(name, **kwargs):
    val_list = []
    tab_ele = list(kwargs.keys())
    for i in range(len(tab_ele)):
        table_param = tab_ele[i] + " " + kwargs[tab_ele[i]]
        val_list.append(table_param)
    tab_ele_str = ",\n".join(val_list)
    Create_sql = "Create table" + " " + name + "(" + "\n" + tab_ele_str + ")"
    return Create_sql


if __name__ == "__main__":
    print(create_xml_long())
