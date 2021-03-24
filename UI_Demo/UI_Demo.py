# -*- coding: UTF-8 -*-
"""
@author:ZHOU LEI
@file:UI_Demo.py
@time:2021/02/18
"""
import tkinter as tk
import time
import os
import threading as thr
import multiprocessing as mlp
from exec_scripts.connect_demo import *
from SOCKET_SERVER_FOR_STATISTICS import *

window = tk.Tk()
window.title('demo_win')
"""获取最大屏幕参数"""
max_wid = window.winfo_screenwidth()
max_hig = window.winfo_screenheight()
"""设置成最大屏幕参数的8成"""
window.geometry("{}x{}".format(round(max_wid * .8), round(max_hig * .8)))

var = tk.StringVar()
l = tk.Label(window, text='测试平台运行', bg='green', fg='white', font=('Arial', 12), width=30, height=2)
l.grid(row=0, columnspan=2)

go = True


# socket_server_for_statistics('127.0.0.1', '56789', 2000)


def do_java_re():
    b1["text"] = 'running'
    b1["state"] = 'disabled'
    p = thr.Thread(target=os.system, args=('python exec_scripts\connect_demo.py',))
    p.start()
    p.join()
    b1["text"] = 'start'
    b1["state"] = 'normal'
    # os.system('python exec_scripts\connect_demo.py')


def p_num(n=None):
    global go
    i = 0
    b1["text"] = 'running'
    b1["state"] = 'disabled'
    if n:
        while i < n:
            if not go:
                print('suspend')
                b1["text"] = 'start'
                b1["state"] = 'normal'
                go = True
                break
            print(i)
            time.sleep(1)
            i += 1
        print('over')
        b1["text"] = 'start'
        b1["state"] = 'normal'
        go = True
    else:
        while True:
            if not go:
                print('suspend')
                b1["text"] = 'start'
                b1["state"] = 'normal'
                go = True
                break
            print(i)
            time.sleep(1)
            i += 1


def start_num(n=None):
    p = thr.Thread(target=p_num, args=(n,))
    p.start()


def stop_num():
    global go
    go = False


"""启停按钮"""
b1 = tk.Button(window, text='start', font=('Arial', 12), width=13, height=1, command=lambda: do_java_re())
b1.grid(row=1, sticky='W')
b2 = tk.Button(window, text='stop', font=('Arial', 12), width=13, height=1, command=stop_num)
b2.grid(row=1, column=1, sticky='E')

separator = tk.Frame(master=window,
                     bg='red',
                     bd=10,
                     relief='groove',
                     padx=1,
                     pady=1,
                     cursor='fleur')
separator.grid(row=2, column=0)
"""菜单按钮"""
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
window.config(menu=menubar)

tk.Button(separator, text="two", width=10, height=10).grid(row=0, column=1)
tk.Button(separator, text="three", width=10, height=10).grid(row=0, column=2)
# tk.Label(separator, text="three").grid(row=1, column=1, columnspan=1, sticky='E')

# 弹窗模块
from tkinter import messagebox

x = tk.messagebox.askokcancel('Python Demo', '发射核弹？')
if x:
    print('发射成功！')

window.mainloop()
