# -*- coding: utf-8 -*-
import socket
import os
import sys
import struct
from Tkinter import *
from tkMessageBox import *


def socket_client():
    if humiEntry.get() == "" or temEntry.get() == "":
        showerror(u'错误！', u'输入不能为空！')
        return
    elif not (temEntry.get().isdigit() and humiEntry.get().isdigit):
        showerror(u'错误！', u'输入只能是纯数字！')
        return
    fp = open("config.txt", 'wb')
    fp.write(temEntry.get())
    fp.write('\n')
    fp.write(humiEntry.get())
    fp.close()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.connect(("127.0.0.1", 51423))
        s.connect(("198.13.44.67", 51423))
    except socket.error as msg:
        print msg
        sys.exit(1)
    print "here"
    print s.recv(1024)

    while 1:
        #filepath = raw_input('please input file path: ')
        filepath = "config.txt"
        if os.path.isfile(filepath):
            # 定义定义文件信息。128s表示文件名为128bytes长，l表示一个int或log文件类型，在此为文件大小
            fileinfo_size = struct.calcsize('128sl')
            # 定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl', os.path.basename(filepath),
                                os.stat(filepath).st_size)
            s.send(fhead)
            print 'client filepath: {0}'.format(filepath)

            fp = open(filepath, 'rb')
            while 1:
                data = fp.read(1024)
                if not data:
                    print '{0} file send over...'.format(filepath)
                    break
                s.send(data)
        s.close()
        break

root = Tk()
frame = Frame(root)
root.title(u'服务器阈值设置')
frame.pack(padx = 10, pady = 10)
Label(frame, text = u'温度阈值:').grid(row = 0, column = 0)
Label(frame, text = u'湿度阈值:').grid(row = 1, column = 0)
temEntry = Entry(frame)
temEntry.grid(row = 0, column = 1)
humiEntry = Entry(frame)
humiEntry.grid(row = 1, column = 1)
Button(frame, text = u'设置', command = socket_client).grid(row = 2, columnspan = 2)
root.mainloop()
