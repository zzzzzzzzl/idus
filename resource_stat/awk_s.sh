#!/bin/bash

p_name=$1
str1="gdb"
str2='/bin/bash'
str3='kworker'
str4='/usr/'
p_num=`ps -ef | grep $p_name | grep -v grep | grep -v "$str1" | grep -v "$str2" | grep -v "$str3"  | grep -v $str4 | wc -l`
if [ $p_num == 0 ]
then
{
	echo 'NO MATCH!'
}
else
{
	for i in $(ps -ef | grep $p_name | grep -v grep | grep -v "$str1" | grep -v "$str2" | grep -v "$str3"  | grep -v $str4 | awk {'print $2'})
	do
	{	
		a=`top -b -n1 | grep $i | grep $p_name | grep -v grep | awk {'print $9'}`
		b=`ps -aux | grep $i | grep $p_name | grep -v grep | awk {'print $11'}`
		c=`top -b -n1 | grep $i | grep $p_name | grep -v grep | awk {'print $10'}`
		echo $b $a $c
	}	
	done
}
fi
