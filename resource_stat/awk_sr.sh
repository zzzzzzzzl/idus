#!/bin/bash

p_name=$1
gdb='gdb '
str1="$gdb$p_name"
str2='/bin/bash'
p_num=`ps -ef | grep $p_name | grep -v grep | grep -v "$str1" | grep -v "$str2" | wc -l`
if [ $p_num == 0 ]
then
{
	echo 'NO MATCH!'
}
else
{
	for i in $(ps -ef | grep $p_name | grep -v grep | grep -v "$str1" | grep -v "$str2" | awk {'print $2'})
	do
	{	
		a=`top -p $i | grep $p_name | grep -v grep | awk {'print $9'}`
		b=`top -p $i | grep $p_name | grep -v grep | awk {'print $10'}`
#		c=`ps -aux | grep $i | grep $p_name | grep -v grep | awk {'print $4'}`
		echo $b $a
	}	
	done
}
fi
