# !/usr/bin/python
# -*- coding: UTF-8 -*-
import copy
import json
import os
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import tkinter.font as tkFont
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.messagebox

from rjTools.utils import file2dict, create_file


class CronJobDialog(tk.Toplevel):
    def __init__(self, parent, base, data: dict = None):
        super().__init__()

        self.resizable(0, 0)  # 阻止Python GUI的大小调整
        self.baseWindow = base
        self.name = tk.StringVar()
        self.exec_cmd = tk.StringVar()
        self.exec_path = tk.StringVar()
        self.day_of_week = tk.StringVar()
        self.hour = tk.IntVar()
        self.minute = tk.IntVar()
        self.second = tk.IntVar()
        self.desc = tk.StringVar()
        self.enable = tk.IntVar()

        if data is not None:
            self.name.set(data.get('name') if data.get('name') is not None else '')
            self.exec_cmd.set(data.get('exec_cmd') if data.get('exec_cmd') is not None else '')
            self.exec_path.set(data.get('exec_path') if data.get('exec_path') is not None else '')
            self.day_of_week.set(data.get('day_of_week') if data.get('day_of_week') is not None else '')
            self.hour.set(data.get('hour') if data.get('hour') is not None else 0)
            self.minute.set(data.get('minute') if data.get('minute') is not None else 0)
            self.second.set(data.get('second') if data.get('second') is not None else 0)
            self.desc.set(data.get('desc') if data.get('desc') is not None else '')
            self.enable.set(data.get('enable') if data.get('enable') is not None else 1)

        self.title('设置定时任务信息')
        self.parent = parent  # 显式地保留父窗口
        self.jobdic = {}

        labelzize = 10
        entrysize = 30

        row1 = tk.Frame(self)
        row1.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row1, text='名称：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=0, column=0)
        tk.Entry(row1, textvariable=self.name, width=entrysize, font=('Times', 10)).grid(row=0, column=1)

        tk.Label(row1, text='执行命令：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=1, column=0)
        tk.Entry(row1, textvariable=self.exec_cmd, width=entrysize, font=('Times', 10)).grid(row=1, column=1)

        tk.Label(row1, text='执行路径：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=2, column=0)
        tk.Entry(row1, textvariable=self.exec_path, width=entrysize, font=('Times', 10)).grid(row=2, column=1)
        tk.Button(row1, text="...", command=self.selectPath, font=('Times', 10), height=1).grid(row=2, column=2, padx=5,
                                                                                                pady=1)

        tk.Label(row1, text='天：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=3, column=0)
        tk.Entry(row1, textvariable=self.day_of_week, width=entrysize, font=('Times', 10)).grid(row=3, column=1)

        tk.Label(row1, text='时：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=4, column=0)
        tk.Entry(row1, textvariable=self.hour, width=entrysize, font=('Times', 10)).grid(row=4, column=1)

        tk.Label(row1, text='分：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=5, column=0)
        tk.Entry(row1, textvariable=self.minute, width=entrysize, font=('Times', 10)).grid(row=5, column=1)

        tk.Label(row1, text='秒：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=6, column=0)
        tk.Entry(row1, textvariable=self.second, width=entrysize, font=('Times', 10)).grid(row=6, column=1)

        tk.Label(row1, text='描述：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=7, column=0)
        tk.Entry(row1, textvariable=self.desc, width=entrysize, font=('Times', 10)).grid(row=7, column=1)

        tk.Label(row1, text='激活：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=8, column=0)
        tk.Entry(row1, textvariable=self.enable, width=entrysize, font=('Times', 10)).grid(row=8, column=1)

        tk.Button(row1, text="确定", command=self.ok, anchor=NW, font=('Times', 10)).grid(row=9, column=0, padx=5, pady=5)
        tk.Button(row1, text="取消", command=self.cancel, anchor=NW, font=('Times', 10)).grid(row=9, column=1, padx=5,
                                                                                            pady=5)

        if data is not None:
            tk.Button(row1, text="删除", command=self.delete, anchor=NW, font=('Times', 10)).grid(row=9, column=2, padx=5,
                                                                                                pady=5)

    def selectFile(self):
        path_ = filedialog.askopenfilename()
        path_ = path_.replace("/", "\\\\")
        self.exec_path.set(path_)

    def selectPath(self):
        path_ = askdirectory()
        self.exec_path.set(path_)

    def ok(self):
        self.jobdic['name'] = self.name.get() if self.name.get() is not None else ''
        self.jobdic['exec_cmd'] = self.exec_cmd.get() if self.exec_cmd.get() is not None else ''
        self.jobdic['exec_path'] = self.exec_path.get() if self.exec_path.get() is not None else ''
        self.jobdic['job_type'] = 1  # 1 定时任务 3 间隔任务
        self.jobdic['day_of_week'] = self.day_of_week.get() if self.day_of_week.get() is not None else ''
        self.jobdic['hour'] = self.hour.get() if self.hour.get() is not None else 0
        self.jobdic['minute'] = self.minute.get() if self.minute.get() is not None else 0
        self.jobdic['second'] = self.second.get() if self.second.get() is not None else 0
        self.jobdic['desc'] = self.desc.get() if self.desc.get() is not None else ''
        self.jobdic['enable'] = self.enable.get() if self.enable.get() is not None else 1
        # self.parent
        print(self.jobdic)
        self.baseWindow.writeConfigFile(copy.deepcopy(self.jobdic))
        self.baseWindow.refreshList()
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.destroy()

    def delete(self):
        key = self.name.get()
        if key is not None:
            self.baseWindow.deleteWriteFile(key)
            self.baseWindow.refreshList()
        self.destroy()


class IntervalJobDialog(tk.Toplevel):
    """
    间隔任务添加对话框
    """

    def __init__(self, parent, base, data: dict = None):
        super().__init__()
        self.resizable(0, 0)  # 阻止Python GUI的大小调整
        self.baseWindow = base

        self.name = tk.StringVar()
        self.exec_cmd = tk.StringVar()
        self.exec_path = tk.StringVar()
        self.second = tk.IntVar()
        self.task_name = tk.StringVar()
        self.desc = tk.StringVar()
        self.enable = tk.IntVar()

        if data is not None:
            self.name.set(data.get('name') if data.get('name') is not None else '')
            self.exec_cmd.set(data.get('exec_cmd') if data.get('exec_cmd') is not None else '')
            self.exec_path.set(data.get('exec_path') if data.get('exec_path') is not None else '')
            self.second.set(data.get('second') if data.get('second') is not None else 5)
            self.task_name.set(data.get('task_name') if data.get('task_name') is not None else '')
            self.desc.set(data.get('desc') if data.get('desc') is not None else '')
            self.enable.set(data.get('enable') if data.get('enable') is not None else 1)

        self.title('设置间隔任务信息')
        self.parent = parent  # 显式地保留父窗口
        self.jobdic = {}

        labelzize = 15
        entrysize = 30

        row1 = tk.Frame(self)
        row1.pack(fill="x", ipadx=1, ipady=1)
        tk.Label(row1, text='名称(唯一)：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=0, column=0)
        tk.Entry(row1, textvariable=self.name, width=entrysize, font=('Times', 10)).grid(row=0, column=1)

        tk.Label(row1, text='执行命令：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=1, column=0)
        tk.Entry(row1, textvariable=self.exec_cmd, width=entrysize, font=('Times', 10)).grid(row=1, column=1)

        tk.Label(row1, text='执行路径：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=2, column=0)
        tk.Entry(row1, textvariable=self.exec_path, width=entrysize, font=('Times', 10)).grid(row=2, column=1)
        tk.Button(row1, text="...", command=self.selectPath, font=('Times', 10), height=1).grid(row=2, column=2, padx=5,
                                                                                                pady=1)

        tk.Label(row1, text='间隔触发(秒)：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=3, column=0)
        tk.Entry(row1, textvariable=self.second, width=entrysize, font=('Times', 10)).grid(row=3, column=1)

        tk.Label(row1, text='任务名：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=4, column=0)
        tk.Entry(row1, textvariable=self.task_name, width=entrysize, font=('Times', 10)).grid(row=4, column=1)

        tk.Label(row1, text='描述：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=5, column=0)
        tk.Entry(row1, textvariable=self.desc, width=entrysize, font=('Times', 10)).grid(row=5, column=1)

        tk.Label(row1, text='激活：', width=labelzize, anchor=NW, font=('Times', 10)).grid(row=6, column=0)
        tk.Entry(row1, textvariable=self.enable, width=entrysize, font=('Times', 10)).grid(row=6, column=1)

        tk.Button(row1, text="确定", command=self.ok, font=('Times', 10)).grid(row=7, column=0, padx=5, pady=5)
        tk.Button(row1, text="取消", command=self.cancel, font=('Times', 10)).grid(row=7, column=1, padx=5, pady=5)
        if data is not None:
            tk.Button(row1, text="删除", command=self.delete, anchor=NW, font=('Times', 10)).grid(row=7, column=2, padx=5,
                                                                                                pady=5)

    # def selectFile(self):
    #     path_ = filedialog.askopenfilename()
    #     path_ = path_.replace("/", "\\\\")
    #     self.exec_path.set(path_)

    def selectPath(self):
        path_ = askdirectory()
        self.exec_path.set(path_)

    def ok(self):
        self.jobdic['name'] = self.name.get() if self.name.get() is not None else ''
        self.jobdic['exec_cmd'] = self.exec_cmd.get() if self.exec_cmd.get() is not None else ''
        self.jobdic['exec_path'] = self.exec_path.get() if self.exec_path.get() is not None else ''
        self.jobdic['job_type'] = 3  # 1 定时任务 3 间隔任务
        self.jobdic['second'] = self.second.get() if self.second.get() is not None else 5
        self.jobdic['task_name'] = self.task_name.get() if self.task_name.get() is not None else ''
        self.jobdic['desc'] = self.desc.get() if self.desc.get() is not None else ''
        self.jobdic['enable'] = self.enable.get() if self.enable.get() is not None else 1
        # self.parent
        print(self.jobdic)
        self.baseWindow.writeConfigFile(copy.deepcopy(self.jobdic))
        self.baseWindow.refreshList()
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.destroy()

    def delete(self):
        key = self.name.get()
        if key is not None:
            self.baseWindow.deleteWriteFile(key)
            self.baseWindow.refreshList()
        self.destroy()


class SchedulerUI(Frame):
    ft = None
    path = ""
    treeview = None
    frm_right = None
    frm_list = None
    frm_log = None
    service_list = None
    configPath = ''

    def __init__(self, master, path: str):
        super().__init__(master)
        self.configPath = path
        create_file(path)

        self.service_list = file2dict(self.configPath)

        self.master = master
        self.initComponent(master)

    def initComponent(self, master):
        # 文件路径
        self.path = StringVar()
        # master.geometry('800x480+200+100')
        master.title('任务执行管理器')
        master.option_add("*Font", "宋体")
        master.minsize(1500, 480)
        # master.resizable(0, 0)  # 阻止Python GUI的大小调整

        # 设置最大化
        # w, h = root.maxsize()
        # root.geometry("{}x{}".format(w, h))  # 看好了，中间的是小写字母x

        # 设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        # self.ft = tkFont.Font(family='微软雅黑', size=12, weight='bold')  # 创建字体

        self.initMenu(master)

        # 设置继承类MWindow的grid布局位置，并向四个方向拉伸以填充顶级窗体
        self.grid(row=0, column=0, sticky=NSEW)
        # 设置继承类MWindow的行列权重，保证内建子组件会拉伸填充
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frm_right = ttk.Frame(master, relief=SUNKEN)  # 右侧Frame帧用于放置视频区域和控制按钮
        self.frm_right.grid(row=0, column=0, sticky=NSEW)  # 右侧Frame帧四个方向拉伸
        self.frm_right.columnconfigure(0, weight=1)  # 右侧Frame帧两行一列，配置列的权重
        self.frm_right.rowconfigure(0, weight=1)  # 右侧Frame帧两行的权重8:1
        # self.frm_right.rowconfigure(1, weight=1)
        # self.panewin.add(self.frm_right, weight=50)  # 将右侧Frame帧添加到推拉窗控件,右侧权重10

        s = ttk.Style()
        s.configure('www.TFrame', background='black')  # 视频区Frame帧添加样式

        # 右侧Frame帧第一行添加视频区Frame
        self.frm_list = ttk.Frame(self.frm_right, relief=RIDGE)
        self.frm_list.grid(row=0, column=0, sticky=NSEW)
        self.initList()

        # # 右侧Frame帧第二行添加控制按钮
        # self.frm_log = ttk.Frame(self.frm_right, relief=RIDGE)  # 四个方向拉伸, style="www.TFrame"
        # self.frm_log.grid(row=1, column=0, sticky=NSEW)
        #
        # tk.Label(self.frm_log, text='运行中任务：', anchor=NW).grid(row=0, column=0)
        # self.log_data_Text = Text(self.frm_log, height=10)  # 日志框
        # self.log_data_Text.grid(row=1, column=0, sticky=NSEW)
        #
        # # "insert" 索引表示插入光标当前的位置
        # self.log_data_Text.insert("insert", "I love ")
        # self.log_data_Text.insert("end", "Python.com!")
        #
        # self.frm_log = ttk.Frame(self.frm_right, relief=RIDGE)  # 四个方向拉伸, style="www.TFrame"
        # self.frm_log.grid(row=1, column=2, sticky=NSEW)

    def initMenu(self, master):
        """初始化菜单"""
        mbar = Menu(master)  # 定义顶级菜单实例
        fmenu = Menu(mbar, tearoff=False)  # 在顶级菜单下创建菜单项
        mbar.add_cascade(label=' 添加任务 ', menu=fmenu, font=('Times', 20, 'bold'))  # 添加子菜单
        fmenu.add_command(label="定时任务", command=self.addCornJob, font=('Times', 10))
        fmenu.add_command(label="循环任务", command=self.addIntervalJob, font=('Times', 10))
        # fmenu.add_separator()  # 添加分割线
        # fmenu.add_command(label="退出", command=master.quit(), font=('Times', 10))

        fmenu2 = Menu(mbar, tearoff=False)  # 在顶级菜单下创建菜单项
        mbar.add_cascade(label='开机服务 ', menu=fmenu2, font=('Times', 20, 'bold'))  # 添加子菜单
        fmenu2.add_command(label="设为开机启动", command=self.setPoweron, font=('Times', 10))
        fmenu2.add_command(label="取消开机启动", command=self.setPoweronFalse, font=('Times', 10))

        mbar.add_cascade(label='关于 ', command=self.showAbout, font=('Times', 20))  # 添加子菜单
        master.config(menu=mbar)  # 将顶级菜单注册到窗体

    def setPoweron(self):
        os.system("winsw install")

    def setPoweronFalse(self):
        os.system("winsw uninstall")

    def showAbout(self):
        # print("about")
        tkinter.messagebox.showinfo(title='关于', message='作者：Aaron\n联系方式：000\n描述：定时任务编辑工具')

    def initList(self):
        scrollbar = Scrollbar(self.frm_list)
        scrollbar.pack(side=RIGHT, fill=Y)

        title = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        self.treeview = ttk.Treeview(self.frm_list, columns=title,
                                     yscrollcommand=scrollbar.set,
                                     show='headings', )
        self.treeview.column('1', width=100, anchor='w')
        self.treeview.column('2', width=200, anchor='w')
        self.treeview.column('3', width=200, anchor='w')
        self.treeview.column('4', width=20, anchor='center')
        self.treeview.column('5', width=20, anchor='center')
        self.treeview.column('6', width=20, anchor='center')
        self.treeview.column('7', width=20, anchor='center')
        self.treeview.column('8', width=20, anchor='center')
        self.treeview.column('9', width=200, anchor='w')
        self.treeview.column('10', width=200, anchor='w')
        self.treeview.column('11', width=20, anchor='center')

        self.treeview.heading('1', text='名称')
        self.treeview.heading('2', text='命令')
        self.treeview.heading('3', text='路径')
        self.treeview.heading('4', text='类型')
        self.treeview.heading('5', text='天')
        self.treeview.heading('6', text='时')
        self.treeview.heading('7', text='分')
        self.treeview.heading('8', text='秒')
        self.treeview.heading('9', text='任务名')
        self.treeview.heading('10', text='描述')
        self.treeview.heading('11', text='激活')

        scrollbar.config(command=self.treeview.yview)  # 设置Scrollbar组件的command选项为该组件的yview()方法
        self.treeview.pack(fill=BOTH)
        # self.box.bind('<ButtonRelease-1>', self.treeviewClick)  # 绑定单击离开事件===========
        self.treeview.bind("<Double-1>", self.treeviewClick)  # 双击
        self.refreshList()

    def treeviewClick(self, event):  # 单击
        dd = self.treeview.selection()
        if dd is None or len(dd) == 0:
            return

        # for item in self.treeview.selection():
        item_text = self.treeview.item(dd[0], "values")
        # print(item_text[0])  # 输出所选行的第一列的值
        if item_text[0] is not None:
            for item in self.service_list:
                itemname = item.get('name') if item.get('name') is not None else ''
                key = str(item_text[0])
                if key == itemname:
                    if item.get('job_type') == 1:
                        pw = CronJobDialog(self.master, self, item)
                        self.master.wait_window(pw)  # 这一句很重要！！！
                    elif item.get('job_type') == 2:
                        pw = IntervalJobDialog(self.master, self, item)
                        self.master.wait_window(pw)  # 这一句很重要！！！
                    elif item.get('job_type') == 3:
                        pw = IntervalJobDialog(self.master, self, item)
                        self.master.wait_window(pw)  # 这一句很重要！！！
                    else:
                        print("无效类型")
                    break

    def refreshList(self):
        x = self.treeview.get_children()
        for item in x:
            self.treeview.delete(item)

        if self.service_list is None:
            return
        for ser in self.service_list:
            name = ser.get('name')
            cmd = ser.get('exec_cmd')
            path = ser.get('exec_path') if ser.get('exec_path') is not None else './'
            jobtype = ser.get('job_type')
            desc = ser.get('desc') if ser.get('desc') is not None else ''
            enable = ser.get('enable') if ser.get('enable') is not None else 1

            week = ''
            hour = ''
            minute = ''
            second = ''
            task_name = ''
            if jobtype == 1:
                jobMsg = '定时任务'
                week = ser.get('day_of_week') if ser.get('day_of_week') is not None else '0-6'
                hour = ser.get('hour') if ser.get('hour') is not None else 0
                minute = ser.get('minute') if ser.get('minute') is not None else 0
                second = ser.get('second') if ser.get('second') is not None else 0
            elif jobtype == 2:
                jobMsg = '保活任务'
                second = ser.get('second')
            elif jobtype == 3:
                jobMsg = '间隔任务'
                task_name = ser.get('task_name') if ser.get('task_name') is not None else ''
                second = ser.get('second') if ser.get('second') is not None else 5
            else:
                jobMsg = '无效的类型'
                print(f'任务:{name} 中无效的类型：{jobtype}')

            rst = [name, cmd, path, jobMsg, week, hour, minute, second, task_name, desc, enable]
            self.treeview.insert('', 'end', values=rst)

    def addIntervalJob(self):
        pw = IntervalJobDialog(self.master, self)
        self.master.wait_window(pw)  # 这一句很重要！！！

    def addCornJob(self):
        pw = CronJobDialog(self.master, self)
        self.master.wait_window(pw)  # 这一句很重要！！！

    def writeFile(self):
        with open(self.configPath, 'w') as file:
            bJson = json.dumps(self.service_list, ensure_ascii=False, indent=2, separators=(',', ': '))  # dict转json
            file.writelines(bJson)

    def writeConfigFile(self, data: dict):
        ischange = False
        if self.service_list is None:
            self.service_list = []
        for i, value in enumerate(self.service_list):
            # for i in range(len(self.service_list)):
            if value.get('name') == data.get('name'):
                # 存在记录更新
                ischange = True
                self.service_list[i] = data
                break
        if not ischange:
            self.service_list.append(data)
        self.writeFile()

    def deleteWriteFile(self, key: str):
        for i, value in enumerate(self.service_list):
            # for i in range(len(self.service_list)):
            if value.get('name') == key:
                del self.service_list[i]
        self.writeFile()


def ShowConfigureUI(configpath: str):
    root = Tk()
    # ui = SchedulerUI(root, "../../conf/task.conf")
    SchedulerUI(root, configpath)
    root.mainloop()


if __name__ == '__main__':
    ShowConfigureUI("./task.conf")
