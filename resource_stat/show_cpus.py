# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import subprocess as sp

#模拟Linux命令行
def cmd(command):
    subp = sp.Popen(command,shell=True,stdout=sp.PIPE,stderr=sp.PIPE,encoding="utf-8",close_fds=True)
    subp.wait(100)
    if subp.poll() == 0:
        cmd_res = subp.communicate()[0]
#清空std流程 
        if subp.stdin:
            subp.stdin.close()

        if subp.stdout:
            subp.stdout.close()

        if subp.stderr:
            subp.stderr.close()
        
        try:
            subp.kill()

        except OSError:

            pass

        return cmd_res
        
    else:
        print(command + " 执行失败")
    
command = r"/home/kun-v1/zl/python_file/python/scripts/thonny_scripts/login.sh"

#单次搜集Linux相关进程的资源消耗
def anl_linux_info(str_info):

    p_list = []

    cpu_dirt = {}

    mem_dirt = {}

    if isinstance(str_info,str):
        
        if "NO MATCH!" in str_info:
            
            print('NO PROCESS MATCH!')
        
        else:
            
            single_res_list = str_info.strip().split("\n")

            for cmd_a in single_res_list:
                
                pp_name = cmd_a.split(" ")[0]
                
                cpu_ratio = cmd_a.split(" ")[1]
            
                mem_ratio = cmd_a.split(" ")[2]
                    
                p_list.append(pp_name)
                
                cpu_dirt[pp_name] = cpu_ratio
                
                mem_dirt[pp_name] = mem_ratio
            
            return (p_list,cpu_dirt,mem_dirt)
        

    else:

        print("NOT STR TYPE!")
    
    

#记录Linux系统信息
arry_cpu_dirt = {}

arry_mem_dirt = {}

try:
    
    x,y,z = anl_linux_info(cmd(command))

    for a in x:
            
        arry_cpu_dirt[a] = []
            
        arry_mem_dirt[a] = []
            
except TypeError:
        
    print('NO PROCESS MATCH!,CAN NOT GET INFO')
    

#获取10次系统进程状态
i = 1

x_list = []

while i < 10:
 
    try:
        
        x,y,z = anl_linux_info(cmd(command))

        for a in x:
            
            arry_cpu_dirt[a].append(y[a])

            arry_mem_dirt[a].append(z[a])
            

        i = i+1
    
        x_list.append(i)
        
    except TypeError:
        
        print('NO PROCESS MATCH!,CAN NOT GET INFO')
        
proc_list = []


#筛选信息
for proc in arry_cpu_dirt.keys():
    
    if proc == 'spawn':
        
        continue
    
    if '@' in proc:
        
        continue
    
    else:
    
        proc_list.append(proc)
        
#打印进程名
print('GET PROCESS HERE:')
print(proc_list)

#绘制图形
color_list = ['blue','orange','green','red','purple','brown','pink','gray','olive','cyan','lime','midnightblue','lightseagreen']

cpu_plot = []

proc_label_cpu = []

for i,elem in enumerate(proc_list):

    cpu_y = [float(x) for x in arry_cpu_dirt[proc_list[i]]]

    plt.subplot(211)
    
    cpu_info, = plt.plot(x_list,cpu_y,color=color_list[i],linewidth=1.0,linestyle='-')
    
    cpu_plot.append(cpu_info)
    
    proc_label_cpu.append(proc_list[i])
    

plt.legend(handles=cpu_plot,labels=proc_label_cpu,loc='best')



mem_plot = []

proc_label_mem = []

for i,elem in enumerate(proc_list):

    mem_y = [float(x) for x in arry_mem_dirt[proc_list[i]]]

    plt.subplot(212)
    
    mem_info, = plt.plot(x_list,mem_y,color=color_list[i],linewidth=1.0,linestyle='-')

    mem_plot.append(mem_info)
    
    proc_label_mem.append(proc_list[i])
    

plt.legend(handles=mem_plot,labels=proc_label_mem,loc='best')

plt.show()
