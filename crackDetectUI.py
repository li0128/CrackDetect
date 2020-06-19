from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showinfo

import time

import os

import CrackDetect

from shutil import copyfile, copy

frameT = Tk()
frameT.geometry('500x200+400+200')
frameT.title('选择需要输入处理的文件')
frame = Frame(frameT)
frame.pack(padx=10, pady=10)  # 设置外边距
frame_1 = Frame(frameT)
frame_1.pack(padx=10, pady=10)  # 设置外边距
frame1 = Frame(frameT)
frame1.pack(padx=10, pady=10)
frame_processbar = Frame(frameT)
frame_processbar.pack(padx=10, pady=10)
v1 = StringVar()
v2 = StringVar()
ent = Entry(frame, width=50, textvariable=v1).pack(fill=X, side=LEFT)  # x方向填充,靠左
ent = Entry(frame_1, width=50, textvariable=v2).pack(fill=X, side=LEFT)  # x方向填充,靠左


def inputDirectoryOpen():
    input_dir = askdirectory()
    if input_dir:
        v1.set(input_dir)


def outputDirectoryOpen():
    output_dir = askdirectory()
    if output_dir:
        v2.set(output_dir)


def count_images(dir_path):
    count = 0
    dir_files = os.listdir(dir_path)  # 得到该文件夹下所有的文件
    for file in dir_files:
        file_path = os.path.join(dir_path, file)  # 路径拼接成绝对路径
        if os.path.isfile(file_path):  # 如果是文件，就打印这个文件路径
            if (file_path.lower().endswith(
                    ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))):
                print(file_path)
                count = count + 1

        if os.path.isdir(file_path):  # 如果目录，就递归子目录
            count = count_images(file_path) + count

    return count


def process_images(input_dir, output_dir, pb, total, count):
    dir_files = os.listdir(input_dir)  # 得到该文件夹下所有的文件
    for file in dir_files:
        print("input_dir:   " + input_dir)
        print("file:    " + file)
        file_path = input_dir + "/" + file  # os.path.join(input_dir, file)  # 路径拼接成绝对路径
        print("file_path:   " + file_path)
        if os.path.isfile(file_path):
            if (file_path.lower().endswith(
                    ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))):
                count = train(count, file, file_path, output_dir, pb, total)

        sub_output_dir = os.path.join(output_dir, file)
        if os.path.isdir(file_path):  # 如果目录，就递归子目录
            count = process_images(file_path, sub_output_dir, pb, total, count)

    return count


def train(count, file, file_path, output_dir, pb, total):
    print("crackPath:   " + file_path)
    flag = CrackDetect.crackDetect(file_path)  # ('F:/crackDetect.jpg') #
    print("crackFlag:   " + flag.__str__())

    if flag > 10000:
        if not os.path.exists(os.path.join(output_dir, 'with_cave')):
            os.makedirs(os.path.join(output_dir, 'with_cave'))
        copy(file_path, os.path.join(output_dir, 'with_cave', file))
    elif flag < 100:
        if not os.path.exists(os.path.join(output_dir, 'without_cave')):
            os.makedirs(os.path.join(output_dir, 'without_cave'))
        copy(file_path, os.path.join(output_dir, 'without_cave', file))
    else:
        if not os.path.exists(os.path.join(output_dir, 'unknow')):
            os.makedirs(os.path.join(output_dir, 'unknow'))
        copy(file_path, os.path.join(output_dir, 'unknow', file))

    count = fresh_processbar(count, pb, total)
    return count


def fresh_processbar(count, pb, total):
    count = count + 1
    value = count * 100 / total
    pb["value"] = value
    frameT.update()
    print(count)
    # time.sleep(1)
    return count


def start():
    pb = ttk.Progressbar(frame_processbar, length=400, value=0, maximum=100, mode="determinate")
    pb.grid(row=1, column=1)
    pb["maximum"] = 100
    pb["value"] = 0
    # n = IntVar()
    # pb["variable"] = n

    if (os.path.exists(v1.get())):
        total = count_images(v1.get())
        print(total)
        process_images(input_dir=v1.get(), output_dir=v2.get(), pb=pb, total=total, count=0)

        # 刷新总进度
        fresh_processbar(total, pb, total)
    #
    #
    # for i in range(100):
    #     pb["value"] = i + 1
    #     frameT.update()
    #     time.sleep(0.1)


def main():
    btn = Button(frame, width=20, text='输入目录', font=("宋体", 14), command=inputDirectoryOpen).pack(fil=X, padx=10)
    btn_1 = Button(frame_1, width=20, text='输出目录', font=("宋体", 14), command=outputDirectoryOpen).pack(fil=X, padx=10)
    ext = Button(frame1, width=10, text='运行', font=("宋体", 14), command=start).pack(fill=X, side=LEFT)
    etb = Button(frame1, width=10, text='退出', font=("宋体", 14), command=frameT.quit).pack(fill=Y, padx=10)

    frameT.mainloop()


if __name__ == '__main__':
    main()
