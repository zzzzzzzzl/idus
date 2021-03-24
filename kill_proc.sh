#!/bin/bash

read -p '输入要终结的进程名:' pp
curr_con=`pwd`
p_num=`ps -aux|grep $pp|grep -v grep|grep -v usr|wc -l`
#判断是否存在该进程
if [ $p_num == 0 ]
then
{
	echo 'NO MATCH!'
}
else
{
	for pp_id in `ps -aux|grep $pp|grep -v grep|grep -v usr|awk {'print $2'}`
	do
{
		pp_con=`ls -l /proc/$pp_id/cwd`
		pp_cn=${pp_con##*'->'}
#判断是否是当前目录进程
	if [[ $pp_cn =~ $curr_con ]]; then
		echo $pp_cn
#kill本目录下的进程
		kill -9 $pp_id
		echo "KILLED $pp_cn/$pp:$pp_id"
	else
#提示非本目录下的进程
		echo 'NOT THE SAME CONTENT!'
		
	fi
}
done
}
fi
