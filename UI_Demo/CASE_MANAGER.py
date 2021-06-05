# -*- coding: UTF-8 -*-
"""
@author:ZHOU LEI
@file:CASE_MANAGER.py
@time:2021/03/04
"""
import tkinter as tk
import os
from tkinter import ttk, filedialog, messagebox
import chardet
import xml.dom.minidom as xml


class CreateUi:

    def __init__(self):
        """初始化界面"""
        self.con_list = []
        self.window = tk.Tk()
        self.window.title("九州昆仑用例管理")
        self.window.iconbitmap('./icon_images/window_icon.ico')
        """Menu菜单设置"""
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='打开文件', command=self.Menu_open_dir)
        filemenu.add_command(label='保存', command=lambda: self.Menu_save_files(self.select_tree_path()))
        filemenu.add_command(label='新建文件', command=self.Menu_new_files)
        filemenu.add_command(label='新建目录', command=self.Menu_new_directs)
        menubar.add_cascade(label='文件', menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label='运行选中对象', command=self.Menu_run_files)
        editmenu.add_command(label='运行所有', command=self.Menu_run_all)
        menubar.add_cascade(label='运行', menu=editmenu)
        conmenu = tk.Menu(menubar, tearoff=0)

        self.db_con = tk.StringVar()
        self.db_con.set('当前连接对象：')
        conmenu.add_command(label='添加数据库连接对象', command=self.add_con)
        conmenu.add_command(label='选择数据库连接对象', command=self.choose_con)
        menubar.add_cascade(label='数据库连接', menu=conmenu)
        self.window.config(menu=menubar)
        tk.Label(self.window, textvariable=self.db_con).pack(side='top', anchor='w')

        pane_window = tk.PanedWindow(self.window, orient='horizontal', sashrelief='sunken')
        pane_window.pack(expand=1, fill='both')

        """目录树结构"""
        self.foldimage = tk.PhotoImage(file='./icon_images/folder.png')
        self.init_path = 'D:\\pycharm\\py_project'
        self.tree_frame = tk.Frame(pane_window)
        self.dir_tree = ttk.Treeview(self.tree_frame, show="tree", selectmode="browse")
        self.tree_sbar = tk.Scrollbar(self.tree_frame, command=self.dir_tree.yview)
        self.dir_call(self.init_path)
        pane_window.add(self.tree_frame)
        self.tree_sbar.pack(side='right', fill='y')
        self.dir_tree.pack(expand=1, fill='both')
        self.dir_tree.config(yscrollcommand=self.tree_sbar.set)
        """点击tree中的元素绑定事件"""
        self.dir_tree.bind("<<TreeviewSelect>>", lambda event: self.open_file(self.select_tree_path()))

        """用例内容展示"""
        self.frame_text = tk.Frame(pane_window)
        self.case_text = tk.Text(self.frame_text, undo=True)
        """设置文本样式temp"""
        self.case_text.tag_configure('temp1', font=('Verdana', 12))
        self.case_text.tag_configure('temp2', font=('Arial', 12))
        """设置滚动条"""
        self.case_sbar = tk.Scrollbar(self.frame_text, command=self.case_text.yview)
        pane_window.add(self.frame_text)
        self.case_sbar.pack(side='right', fill='y')
        self.case_text.pack(expand=1, fill='both')
        start_tips = 'Welcome to use the Testool,' \
                     '\n\nYou may use it to run your python scripts or text cases from Java,' \
                     '\n\nHave a nice experience!'

        self.case_text.insert('end', start_tips, 'temp2')
        self.case_text.config(yscrollcommand=self.case_sbar.set)
        """设置文本用例相关弹出菜单"""
        self.case_menu = tk.Menu(pane_window, tearoff=0)
        self.case_menu.add_command(label='Run As Python Case', command=lambda: self.Menu_run_files())
        self.case_menu.add_command(label='Run As Java Case', command=lambda: self.Menu_run_files())
        self.case_menu.add_command(label='Reload', command=lambda: self.reload_tree())
        self.case_menu.add_command(label='Delete', command=lambda: self.del_file_dirs())
        """实现底部输出窗口"""
        self.output_window = tk.Frame(pane_window)
        self.output_text = tk.Text(self.output_window)
        self.output_sbar = tk.Scrollbar(self.output_window, command=self.output_text.yview)
        pane_window.add(self.output_window)
        self.output_sbar.pack(side='right', fill='y')
        self.output_text.pack(expand=1, fill='both')
        self.output_text.config(yscrollcommand=self.output_sbar.set)

        """事件绑定设置"""
        self.case_text.bind("<Control-KeyPress-s>", lambda event: self.Menu_save_files(self.select_tree_path()))
        self.case_text.bind("<Control-KeyPress-S>", lambda event: self.Menu_save_files(self.select_tree_path()))
        self.dir_tree.bind('<Button-3>', self.show_menu)
        self.window.mainloop()

    def show_menu(self, event):
        self.case_menu.post(event.x_root, event.y_root)

    def move(self):
        """文件撤销按钮"""
        try:
            self.case_text.edit_undo()
        except tk.TclError:
            pass

    def Menu_open_dir(self):
        """打开用例目录"""
        self.init_path = tk.filedialog.askdirectory()
        if self.init_path:
            """清除已存在的目录树"""
            a = tk.messagebox.askokcancel('Will You?', '是否覆盖当前已存在目录')
            if a:
                for item in self.dir_tree.get_children():
                    self.dir_tree.delete(item)
                self.dir_call(self.init_path)
            else:
                self.dir_call(self.init_path)

    def Menu_save_files(self, current_path):
        """保存文件"""
        if current_path:
            new_contents = self.case_text.get(1.0, 'end')
            if os.path.isfile(current_path):
                try:
                    with open(current_path, 'w', encoding=get_files_encode(current_path)) as f:
                        f.write(new_contents)
                        tk.messagebox.showinfo('tips', '保存成功！')
                except Exception as e:
                    print(str(e))
                    tk.messagebox.showerror('err info:', '无法保存该文件')

    def Menu_new_files(self):
        """新建文件"""
        if self.select_tree_path():
            if os.path.isfile(self.select_tree_path()):
                current_path = os.path.dirname(self.select_tree_path())
            elif os.path.isdir(self.select_tree_path()):
                current_path = self.select_tree_path()
            else:
                tk.messagebox.showerror('err info', '请先选择要新建文件的目录!')
                return
        else:
            tk.messagebox.showerror('err info', '请先选择要新建文件的目录!')
            return
        new_file_win = tk.Tk()
        new_file_win.title('The New File Name？')
        file_name_text = tk.Text(new_file_win, undo=True, width=50, height=1)
        file_name_text.pack()

        def get_text(win, text_window):
            context = text_window.get(1.0, 'end').strip('\n')
            if context:
                file = current_path + '\\' + context
                isexists = os.path.exists(file)
                """判断是否已存在该文件"""
                if not isexists:
                    with open(file, 'w+', encoding='UTF-8') as f:
                        f.write('')
                else:
                    tk.messagebox.showerror('err info', '该文件已存在!')
            else:
                tk.messagebox.showerror('err info', '请输入有效的文件名!')
            win.destroy()

        tk.Button(new_file_win, text='确定', command=lambda: get_text(new_file_win, file_name_text)).pack()

    def Menu_new_directs(self):
        """新建目录"""
        if self.select_tree_path():
            if os.path.isfile(self.select_tree_path()):
                current_path = os.path.dirname(self.select_tree_path())
            elif os.path.isdir(self.select_tree_path()):
                current_path = self.select_tree_path()
            else:
                tk.messagebox.showerror('err info', '请先选择要新建文件夹的目录!')
                return
        else:
            tk.messagebox.showerror('err info', '请先选择要新建文件夹的目录!')
            return

        new_win = tk.Tk()
        new_win.title('The New Dir Name？')
        file_name_text = tk.Text(new_win, undo=True, width=50, height=1)
        file_name_text.pack()

        def get_text(win, text_window):
            context = text_window.get(1.0, 'end').strip('\n')
            if context:
                dir = current_path + '\\' + context + '\\'
                """判断是否已存在该文件夹"""
                isexists = os.path.exists(dir)
                if not isexists:
                    os.makedirs(dir)
                else:
                    tk.messagebox.showerror('err info', '该文件夹已存在!')
            else:
                tk.messagebox.showerror('err info', '请输入有效的文件夹名!')
            win.destroy()

        tk.Button(new_win, text='确定', command=lambda: get_text(new_win, file_name_text)).pack()

    def Menu_run_files(self):
        """运行单个文件"""
        if os.path.isfile(self.select_tree_path()):
            res = os.popen('python ' + self.select_tree_path())
            context = res.read()
            self.output_text.delete(1.0, 'end')
            self.output_text.insert(1.0, context, 'temp2')

    def Menu_run_all(self):
        """运行所有用例"""
        pass

    def dir_call(self, path, root_dir=''):
        """treeview用例目录结构展示"""
        i = 0
        node_dict = {}
        for root, dirs, files in os.walk(path):
            path_var = os.path.split(root)
            dir_name = path_var[1]
            if i and root:
                if root in node_dict.keys():
                    last_node = node_dict[root]
                    node_dict.pop(root)
                    if files:
                        for file_name in files:
                            file_path = root + '\\' + file_name
                            self.dir_tree.insert(last_node, 'end', values=(file_path, last_node), text=file_name)
                    if dirs:
                        for dir in dirs:
                            dir_key = root + '\\' + dir
                            curr_node = self.dir_tree.insert(last_node, 'end', values=(dir_key, last_node), text=dir,
                                                             image=self.foldimage)
                            node_dict[dir_key] = curr_node
                i = + 1
            else:
                last_node = self.dir_tree.insert(root_dir, 'end', values=(root, root_dir), text=dir_name)
                if dirs:
                    for dir in dirs:
                        dir_key = root + '\\' + dir
                        curr_node = self.dir_tree.insert(last_node, 'end', values=(dir_key, last_node), text=dir,
                                                         image=self.foldimage)
                        node_dict[dir_key] = curr_node
                if files:
                    for file_name in files:
                        file_path = root + '\\' + file_name
                        self.dir_tree.insert(last_node, 'end', values=(file_path, last_node), text=file_name)
                i = + 1

    def select_tree_path(self):
        """获取点击对象的绝对路径"""
        try:
            nodeid = self.dir_tree.selection()[0]
            # print(self.dir_tree.item(nodeid))
            current_path = self.dir_tree.item(nodeid)['values'][0]
            # print(self.dir_tree.get_children(nodeid))
            return current_path
        except:
            pass

    def open_file(self, current_path):
        """打开文件并写入text控件"""
        if current_path:
            if os.path.isfile(current_path):
                try:
                    with open(current_path, 'r', encoding=get_files_encode(current_path)) as f:
                        contents = f.read()
                        self.case_text.delete(1.0, 'end')
                        self.case_text.insert(1.0, contents, 'temp2')
                except Exception:
                    tk.messagebox.showerror('err info:', '无法打开该文件')

    def del_file_dirs(self):
        """删除文件或者文件夹"""
        path = self.select_tree_path()
        if os.path.isfile(path):
            a = tk.messagebox.askyesno('Will You?', '确认删除？')
            if a:
                self.del_item()
                os.remove(path)
                tk.messagebox.showinfo('tips', '文件删除成功！')
        if os.path.isdir(path):
            b = tk.messagebox.askyesno('Will You?', '确认删除？')
            if b:
                self.del_item()
                os.rmdir(path)
                tk.messagebox.showinfo('tips', '文件夹删除成功！')

    def del_item(self):
        nodeid = self.dir_tree.selection()[0]
        self.dir_tree.delete(nodeid)

    def reload_tree(self):
        """重新加载目录"""
        nodeid = self.dir_tree.selection()[0]
        path = self.dir_tree.item(nodeid)['values'][0]
        last_node = self.dir_tree.item(nodeid)['values'][1]
        if os.path.isdir(path):
            self.dir_tree.delete(nodeid)
            self.dir_call(path, root_dir=last_node)

    def del_objects(self):
        a = tk.messagebox.askokcancel('Will You?', '删除实际文件？')

    def add_con(self):
        set_con_win = tk.Tk()
        set_con_win.title('The New Connection Info？')
        tk.Label(set_con_win, text='  数据库连接名称：').grid(row=0)
        tk.Label(set_con_win, text='    数据库连接IP：').grid(row=1)
        tk.Label(set_con_win, text='  数据库连接库名：').grid(row=2)
        tk.Label(set_con_win, text='数据库连接用户名：').grid(row=3)
        tk.Label(set_con_win, text='  数据库连接密码：').grid(row=4)

        con_name = tk.Entry(set_con_win)
        con_ip = tk.Entry(set_con_win)
        con_db = tk.Entry(set_con_win)
        con_user = tk.Entry(set_con_win)
        con_password = tk.Entry(set_con_win)
        con_name.grid(row=0, column=1, padx=30, pady=1)
        con_ip.grid(row=1, column=1, padx=30, pady=1)
        con_db.grid(row=2, column=1, padx=30, pady=1)
        con_user.grid(row=3, column=1, padx=30, pady=1)
        con_password.grid(row=4, column=1, padx=30, pady=1)

        def sure_butt():
            name_str = con_name.get()
            if name_str == '':
                tk.messagebox.showerror('err info:', '数据库连接名称不能为空!')
                quit_butt()
                return
            ip_str = con_ip.get()
            if ip_str == '':
                tk.messagebox.showerror('err info:', '数据库连接IP不能为空!')
                quit_butt()
                return
            db_str = con_db.get()
            if db_str == '':
                tk.messagebox.showerror('err info:', '数据库连接库名不能为空!')
                quit_butt()
                return
            user_str = con_user.get()
            if user_str == '':
                tk.messagebox.showerror('err info:', '数据库连接用户名不能为空!')
                quit_butt()
                return
            password_str = con_password.get()
            if password_str == '':
                tk.messagebox.showerror('err info:', '数据库连接密码不能为空!')
                quit_butt()
                return
            xml_config = './DBCONNECTION.xml'
            if os.path.exists(xml_config):
                doc = xml.Document()  # 建立空白XML文档
                root = doc.createElement('Managers')
                root.setAttribute('DBNAME', 'KunLunJdbc')
                root.setAttribute('OperatingSystem', 'Windows')
                doc.appendChild(root)
                """获取旧连接信息写入到新的空白文件"""
                domtree = xml.parse(xml_config)
                collection = domtree.documentElement
                managertags = collection.getElementsByTagName("Manager")
                for manager in managertags:
                    nodemanager = doc.createElement('Manager')
                    name_text = manager.getElementsByTagName("name")[0].childNodes[0].data
                    if name_str == name_text:
                        tk.messagebox.showerror('err info:', '%s 已存在' % name_str)
                        return
                    else:
                        nodename = doc.createElement('name')
                        nodename.appendChild(doc.createTextNode(name_text))

                        ip_text = manager.getElementsByTagName("ip")[0].childNodes[0].data
                        nodeip = doc.createElement('ip')
                        nodeip.appendChild(doc.createTextNode(ip_text))

                        db_text = manager.getElementsByTagName("db")[0].childNodes[0].data
                        nodedb = doc.createElement('db')
                        nodedb.appendChild(doc.createTextNode(db_text))

                        user_text = manager.getElementsByTagName("user")[0].childNodes[0].data
                        nodeuser = doc.createElement('user')
                        nodeuser.appendChild(doc.createTextNode(user_text))

                        password_text = manager.getElementsByTagName("password")[0].childNodes[0].data
                        nodepassword = doc.createElement('password')
                        nodepassword.appendChild(doc.createTextNode(password_text))

                        nodemanager.appendChild(nodename)
                        nodemanager.appendChild(nodeip)
                        nodemanager.appendChild(nodedb)
                        nodemanager.appendChild(nodeuser)
                        nodemanager.appendChild(nodepassword)
                        root.appendChild(nodemanager)
                """追加新配置"""
                nodemanager = doc.createElement('Manager')
                nodename = doc.createElement('name')
                nodename.appendChild(doc.createTextNode(name_str))
                nodeip = doc.createElement('ip')
                nodeip.appendChild(doc.createTextNode(ip_str))
                nodedb = doc.createElement('db')
                nodedb.appendChild(doc.createTextNode(db_str))
                nodeuser = doc.createElement('user')
                nodeuser.appendChild(doc.createTextNode(user_str))
                nodepassword = doc.createElement('password')
                nodepassword.appendChild(doc.createTextNode(password_str))
                nodemanager.appendChild(nodename)
                nodemanager.appendChild(nodeip)
                nodemanager.appendChild(nodedb)
                nodemanager.appendChild(nodeuser)
                nodemanager.appendChild(nodepassword)
                root.appendChild(nodemanager)
                with open(xml_config, 'w') as f:
                    doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding='utf-8')
            else:
                doc = xml.Document()
                root = doc.createElement('Managers')
                root.setAttribute('DBNAME', 'KunLunJdbc')
                root.setAttribute('OperatingSystem', 'Windows')
                doc.appendChild(root)
                nodemanager = doc.createElement('Manager')
                nodename = doc.createElement('name')
                nodename.appendChild(doc.createTextNode(name_str))
                nodeip = doc.createElement('ip')
                nodeip.appendChild(doc.createTextNode(ip_str))
                nodedb = doc.createElement('db')
                nodedb.appendChild(doc.createTextNode(db_str))
                nodeuser = doc.createElement('user')
                nodeuser.appendChild(doc.createTextNode(user_str))
                nodepassword = doc.createElement('password')
                nodepassword.appendChild(doc.createTextNode(password_str))
                nodemanager.appendChild(nodename)
                nodemanager.appendChild(nodeip)
                nodemanager.appendChild(nodedb)
                nodemanager.appendChild(nodeuser)
                nodemanager.appendChild(nodepassword)
                root.appendChild(nodemanager)
                with open(xml_config, 'w+') as f:
                    doc.writexml(f, indent='\t', addindent='\t', newl='\n', encoding='utf-8')

            set_con_win.destroy()

        def quit_butt():
            set_con_win.destroy()

        tk.Button(set_con_win, text='确定', width=15, command=sure_butt).grid(row=6, pady=2)
        tk.Button(set_con_win, text='退出', width=15, command=quit_butt).grid(row=6, column=1, pady=2, sticky='e')

    def choose_con(self):
        xml_config = './DBCONNECTION.xml'
        domtree = xml.parse(xml_config)
        collection = domtree.documentElement
        managertags = collection.getElementsByTagName("Manager")
        box_dir = {}
        box_tup = ()
        for manager in managertags:
            name_text = manager.getElementsByTagName("name")[0].childNodes[0].data
            box_tup = box_tup + (name_text,)
            ip_text = manager.getElementsByTagName("ip")[0].childNodes[0].data
            db_text = manager.getElementsByTagName("db")[0].childNodes[0].data
            user_text = manager.getElementsByTagName("user")[0].childNodes[0].data
            password_text = manager.getElementsByTagName("password")[0].childNodes[0].data
            box_dir[name_text] = [ip_text, db_text, user_text, password_text]
        sel_con_win = tk.Tk()
        sel_con_win.title('选择你的连接对象')
        con_name_choose = ttk.Combobox(sel_con_win)
        con_name_choose['values'] = box_tup
        tk.Label(sel_con_win, text='选择你的连接对象：').grid(row=0, column=0)
        con_name_choose.grid(row=0, column=1)
        con_name_choose.current(0)

        def quit_butt():
            sel_con_win.destroy()

        tk.Button(sel_con_win, text='确定', width=15,
                  command=lambda: self.sure_butt(con_name_choose, sel_con_win, box_dir)).grid(row=6, pady=2)
        tk.Button(sel_con_win, text='退出', width=15, command=quit_butt).grid(row=6, column=1, pady=2, sticky='e')

    def sure_butt(self, name, sel_con_win, box_dir):
        """动态显示连接对象"""
        name = name.get()
        text = '当前连接对象：' + name
        self.db_con.set(text)
        sel_con_win.destroy()
        self.con_list = []
        self.con_list.append(name)
        self.con_list.append(box_dir[name][0])
        self.con_list.append(box_dir[name][1])
        self.con_list.append(box_dir[name][2])
        self.con_list.append(box_dir[name][3])
        print(self.con_list)


def get_files_encode(path):
    if os.path.isfile(path):
        """判断是否是文件类型目录"""
        f = open(path, 'rb')
        data = f.read()
        f.close()
        result = chardet.detect(data)
        return result['encoding']
    else:
        raise TypeError('not a file, please give a file path!')


def dir_call(path):
    for root, dirs, files in os.walk(path):
        print('------')
        print(type(root), root + '\\')
        print(type(dirs), dirs)
        print(type(files), files)


def text_font():
    root = tk.Tk()
    # 创建一个Label
    for ft in (
            'Arial', ('Courier New',), ('Comic Sans MS',), 'Fixdsys', ('MS Sans Serif',), ('MS Serif',), 'Symbol',
            'System',
            ('Times New Roman',), 'Verdana'):
        tk.Label(root, text='hello sticky', font=ft).grid()

    root.mainloop()


def diropen():
    # 创建一个Label
    a = tk.filedialog.askdirectory()
    print(a)


if __name__ == '__main__':
    CreateUi()
    diropen()
    dir_call('D:\pycharm\workspace\mis3434\Java_scripts')
    # qwretrewtre1234423