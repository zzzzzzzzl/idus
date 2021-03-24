# -*- coding: utf-8 -*-

import jaydebeapi
import sys
#from Create_data import *
#from Table_data import *
from datetime import *


now_date = datetime.now()

#接收表名入参
table_name = str(sys.argv[1])


url = r'jdbc:kunlun://192.168.3.138:6378/system'
driver = r'com.kunlun.jdbc.Driver'
jar_file = r'/home/zl/jm/kunlun_r3.jar'

user = 'SYSDBA'
passwd = 'SYSDBA'

def transfer_data(table_name):

	conn = jaydebeapi.connect(driver,url,[user,passwd],jar_file)

	curs = conn.cursor()

	exec_sql = r'select * from ' + table_name
	
	curs.execute(exec_sql)
	
	res = curs.fetchall()

	curs.close()
	conn.close()

	return res

try:
	print(table_name + ' data is transfering ..' )
	
	col_list = []
	
	file_name = table_name + '_data'

	with open(file_name,'w') as f:
		
		for a in transfer_data(table_name):
			
			b = [str(i) for i in a]
			
			str_val = ",".join(b)

			col_list.append(str_val)
			
		sql_data = "\n".join(col_list)
		
		f.write(sql_data)

	print(table_name + 'transfer ok !')

except jaydebeapi.DatabaseError as e:
	
	print(str(e) + ' : table name : ' + table_name) 
