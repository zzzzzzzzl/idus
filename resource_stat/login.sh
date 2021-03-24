#!/usr/bin/expect 

spawn ssh root@192.168.3.135 "/home/kun-v1/zl/show_cpus/awk_s.sh r9"
expect "*password:"
send "123456\n"
interact
