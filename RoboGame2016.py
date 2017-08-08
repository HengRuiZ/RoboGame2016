# coding=utf-8
import datetime
import time
import threading
import random
import winsound
from tkinter import *
from PIL import Image, ImageTk
#import messagebox

def resize(w, h, w_box, h_box, pil_image):
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2
  f2 = 1.0*h_box/h
  factor = min([f1, f2])
  width = int(w*factor)
  height = int(h*factor)
  return pil_image.resize((width, height), Image.ANTIALIAS)

def record(place):
    global sig
    if sig != 4:
        messagebox.showinfo('警告','还没有开始！')
        return
    print ("record:%d",place)
    global starttime
    a = place/12+1
    c = place%12/3+1
    b = place%12%3+2
    if result[place] == 1:
        file = open(filename,'a')
        file.write('%2d:%2d:%1d'%(minut-1,second,microsecond)+":%d架%d层%d列上架完成\n"%(a,b,c))
        file.close()
        result[place] = 2
    elif result[place] == 2:
        file = open(filename,'a')
        file.write('%2d:%2d:%1d'%(minut-1,second,microsecond)+":%d架%d层%d列上架取消\n"%(a,b,c))
        file.close()
        result[place] = 1
    elif result[place] == 0:
        file = open(filename,'a')
        file.write('%2d:%2d:%1d'%(minut-1,second,microsecond)+":%d架%d层%d列上架错误\n"%(a,b,c))
        file.close()
    cube[place].configure(bg = color[result[place]])
def initw():
    global name
    global filename
    global result
    global minut,second,microsecond
    global sig
    global x
    if sig > 1:
        messagebox.showinfo('警告','已经初始化！')
        return
    print ('初始化')
    for i in range(24):
        cube[i].configure(bg = 'white')
    result = [0]*24
    name = u.get()
    messagebox.showinfo('请确认参赛队名称',name)
    filename=name.encode('gbk')+b".txt"
    a = random.randrange(0,2)
    b = random.randrange(0,6)
    c = random.randrange(0,5)
    d = random.randrange(0,4)
    e = random.randrange(0,6)
    f = [0]*5
    f[c] = 2
    g = [0]*4
    g[order1[e][0]]=g[order1[e][1]]=1
    i=j=0
    for i in range(5):
      if(f[i]==0):
        f[i]=g[j]
        j+=1
    i=j=0
    book[0] = (1-a)*12+order1[b][0]*3+f[0]
    book[1] = (1-a)*12+order1[b][1]*3+f[1]
    book[2] = a*12+order2[d][0]*3+f[2]
    book[3] = a*12+order2[d][1]*3+f[3]
    book[4] = a*12+order2[d][2]*3+f[4]
    for i in range(5):
        result[book[i]] = 1
        cube[book[i]].configure(bg = 'yellow')
    minut,second,microsecond = 0,0,0
    time_wdgt.config(text = '%2d:%2d:%1d'%(minut,second,microsecond))
    time_wdgt.config(bg='white')
    sig = 1
    x = 0
def ready():
    global starttime
    global sig
    if sig == 0:
        messagebox.showinfo('警告','还未初始化！')
        return
    if sig != 1:
        messagebox.showinfo('警告','已经开始！')
        return
    print ('预备')
    file = open(filename,'a')
    file.write('%2d:%2d:%1d'%(minut,second,microsecond)+":预备\n")
    file.close()
    sig = 2
    time_wdgt.config(bg='yellow')
def start():
  global sig
  global minut,second,microsecond
  print ('开始')
  file = open(filename,'a')
  file.write('准备用时：%2d:%2d:%1d'%(minut,second,microsecond)+"\n\n")
  file.close()
  sig = 4
  minut,second,microsecond = 1,0,0
def timeit():
    global minut,second,microsecond
    global sig
    global x
    if (sig == 2):
        microsecond+=1
        second+=microsecond/10
        microsecond %= 10
        minut += second/60
        second %= 60
        a=59-second
        b=9-microsecond
        time_wdgt.config(text = '00:%2d:%1d'%(a,b))
        if(second==50 and microsecond==0):
          sig=3
    elif (sig==3):
        x+=1
        if(x%2):
          second+=1;
          a=60-second;
          time_wdgt.config(text = '00:%2d:0'%a)
          time.sleep(0.5)
        else:
          winsound.Beep(600,500)#音量，时长
        if (x==20):
          sig = 4
          minut=1
          second=0
          print ('开始')
          file = open(filename,'a')
          file.write('准备用时：1：00：0\n\n')
          file.close()
    elif (sig==4):
        microsecond+=1
        second+=microsecond/10
        microsecond %= 10
        minut += second/60
        second %= 60
        time_wdgt.config(text = '%2d:%2d:%1d'%(minut-1,second,microsecond))
    if (minut == 10 and second == 0 and microsecond == 0):
        winsound.Beep(600,1000)#音量，时长
        time_wdgt.config(bg='red')
    t = threading.Timer(0.094,timeit)
    t.start()
def end():
    global sig
    print ('end')
    k = 0
    sig = 0
    for i in range(24):
        if (result[i] == 2):
            k+=1
    file = open(filename,'a')
    file.write('%2d:%2d:%1d'%(minut-1,second,microsecond)+":结束\n\n")
    file.write('%2d:%2d:%1d'%(minut-1,second,microsecond)+":共完成%d本\n"%k)
    file.close()
def excpt():
    global starttime
    print ('exception')
    print (v.get())
    file = open(filename,'a')
    file.write('%2d:%2d:%1d'%(minut,second,microsecond)+'exception:'+v.get()+"\n")
    file.close()
#全局变量
name = u"队伍名"
filename=name.encode('gbk')+b".txt"
books = [0,0,0,0,0]
order1 = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
order2 = [[0,1,2],[0,1,3],[0,2,3],[1,2,3]]
sig = 0
starttime = datetime.datetime.now()
endtime = datetime.datetime.now()
period = 0.00
minut,second,microsecond = 0,0,0
result = [0]*24
color = ["white","yellow","green"]
book = [0]*5
a=[0]*24
x=0
for i in range(24):
    a[i]=i

"""
#创建多线程
play = threading.Event()
t1 = threading.Thread(target=warning,args=(play,),name='t1')
t1.start()
"""
#建立根结点
root=Tk()
root.title('图书上架比赛程序')
root.geometry('1100x650')

canvas = Canvas(root,width = 1100,height = 650,bg = 'white')
image = Image.open("2016RoboGame.jpg")
w,h=image.size
image_resized = resize(w, h, 1100, 100,image)
im = ImageTk.PhotoImage(image_resized)
canvas.create_image(550,40,image = im)      # 使用create_image将图片添加到Canvas组件中   
canvas.pack()         # 将Canvas添加到主窗口   

#建立书架窗格
lab1 = Label(root,text='书架1')
lab1.place(x=280,y=410)
lab2 = Label(root,text='书架2')
lab2.place(x=780,y=410)
lab3 = Label(root,text='第四层')
lab3.place(x=520,y=140)
lab4 = Label(root,text='第三层')
lab4.place(x=520,y=240)
lab5 = Label(root,text='第二层')
lab5.place(x=520,y=340)
cube = [Button(root,bg = "red",width = 100,height = 100,command = record)]*24
#var0.set("")
for i in range(2):
    for j in range(4):
        for k in range(3):
            num = i*12+j*3+k
            cube[num] = Button(root,bg = color[result[num]],width = 12,height = 5,text = '%d'%(num),command = lambda:record(a[i*12+j*3+k]))
            cube[num].place(x=100+500*i+100*j,y=300-100*k)
cube[0].configure(command = lambda:record(0))
cube[1].configure(command = lambda:record(1))
cube[2].configure(command = lambda:record(2))
cube[3].configure(command = lambda:record(3))
cube[4].configure(command = lambda:record(4))
cube[5].configure(command = lambda:record(5))
cube[6].configure(command = lambda:record(6))
cube[7].configure(command = lambda:record(7))
cube[8].configure(command = lambda:record(8))
cube[9].configure(command = lambda:record(9))
cube[10].configure(command = lambda:record(10))
cube[11].configure(command = lambda:record(11))
cube[12].configure(command = lambda:record(12))
cube[13].configure(command = lambda:record(13))
cube[14].configure(command = lambda:record(14))
cube[15].configure(command = lambda:record(15))
cube[16].configure(command = lambda:record(16))
cube[17].configure(command = lambda:record(17))
cube[18].configure(command = lambda:record(18))
cube[19].configure(command = lambda:record(19))
cube[20].configure(command = lambda:record(20))
cube[21].configure(command = lambda:record(21))
cube[22].configure(command = lambda:record(22))
cube[23].configure(command = lambda:record(23))
#建立按钮和计时窗口
u = StringVar()
v = StringVar()
init_wdgt = Button(root,text='初始化',command=initw)
init_wdgt.place(x=100,y=450)
ready_wdgt = Button(root,text='准备',command=ready)
ready_wdgt.place(x=180,y=450)
start_wdgt = Button(root,text='开始',command=start)
start_wdgt.place(x=250,y=450)
end_wdgt = Button(root,text='结束',command=end)
end_wdgt.place(x=320,y=450)
excpt_wdgt = Button(root,text='记录消息',command=excpt)
excpt_wdgt.place(x=400,y=450)
name_hint = Label(root,text='参赛队：')
name_hint.place(x=100,y=500)
name_input = Entry(root, textvariable=u)
name_input.place(x=200,y=500)
excpt_input = Entry(root, textvariable=v)
excpt_input.place(x=200,y=540)
excpt_hint = Label(root,text='消息：')
excpt_hint.place(x=100,y=540)
time_wdgt = Button(root,text='%2d:%2d:%1d'%(minut,second,microsecond),font=('times',40,'bold'),width=15,height=1)
time_wdgt.place(x=550,y=470)
#建立计时器
t = threading.Timer(0.1,timeit)
t.start()
mainloop()
