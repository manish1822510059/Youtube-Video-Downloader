def VideoUrl():
    DownloadingBarTextLable.configure(text='')
    DownloadingLabelResult.configure(text='')
    DownloadingSizeLabelResult.configure(text='')
    DownloadingLabelTimeLeft.configure(text='')
    getdetail = threading.Thread(target=getvideo)
    getdetail.start()


def getvideo():
    global streams
    listbox.delete(0,END)
    url = urltext.get()
    data = pafy.new(url)
    streams = data.allstreams
    index = 0
    for i in streams:
        du = '{:0.1f}'.format(i.get_filesize()//(1024*1024))
        data = str(index) + '.'.ljust(3, ' ') + str(i.quality).ljust(10, ' ') + str(i.extension).ljust(5, ' ') + str(i.mediatype) + '  ' + du.rjust(10, ' ') + 'MB'
        listbox.insert(END,data)
        index+=1

def selectcursor(evt):
    global downloadindex
    listboxdata = listbox.get(listbox.curselection())
    print(listboxdata)
    downloadstream = listboxdata[:3]
    downloadindex = int(''.join(x for x in downloadstream if x.isdigit()))
    



def DownloadVideo():
    getdata = threading.Thread(target=DownloadVideoData)
    getdata.start()

def DownloadVideoData():
    global downloadindex
    fld = filedialog.askdirectory()
    DownloadingBarTextLable.configure(text='Downloaded......')
    def mycallback(total,recvd,ratio,rate,eta):
        global total12
        total12 = float('{:.5}'.format(total/(1024*1024)))
        DownloadingProgressBar.configure(maximum=total12)
        recieved1 = '{:.5} mb'.format(recvd / (1024 * 1024))
        eta1 = '{:.2f} sec'.format(eta)
        DownloadingSizeLabelResult.configure(text=total12)
        DownloadingLabelResult.configure(text=recieved1)
        DownloadingLabelTimeLeft.configure(text=eta1)
        DownloadingProgressBar['value'] = recvd/(1024*1024)
        

    streams[downloadindex].download(filepath=fld,quiet=True,callback = mycallback)
    DownloadingBarTextLable.configure(text="Downloaded")



def ChangeIntroLabelColor():
    ss = random.choice(colors)
    introlabel.configure(fg=ss)
    introlabel.after(20,ChangeIntroLabelColor)






from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import filedialog
import random
import threading
import pafy

root = Tk()
root.title('Youtube Downloader...')
root.geometry('780x500')
root.iconbitmap(r'youtube1.ico',)
root.configure(bg='skyblue')
root.resizable(False,False)
downloadindex  = 0
total12 = 0
count = 0
text = ''


colors = ['red','green','blue','yellow','gold','pink']


######################## slider ##########################
ss="Developed By Manish Kumar"

SliderLabel = Label(root,text=ss,bg='lightskyblue',font=('arial',12,'italic bold' ))
SliderLabel.place(x=0,y=480)
def IntroLabelTrick():
    global count,text
    if(count>=len(ss)):
        count = -1
        text = ''
        SliderLabel.configure(text=text)
    else:
        text = text+ss[count]
        SliderLabel.configure(text=text)
    count+=1
    SliderLabel.after(200,IntroLabelTrick)
IntroLabelTrick()    

######################Scroll bar#################################
scrollbar = Scrollbar(root)
scrollbar.place(x=477,y=230,height=193,width=20)

#######################URL TEXT ##################################3
urltext = StringVar()
urlEntry = Entry(root,textvariable=urltext,font=('arial',20,'italic bold'),width=31,bg='light yellow')
urlEntry.place(x=20,y=150)

############################# Labels ##############################
introlabel = Label(root,text="Welcome to youtube Audio Video Downloder",width=36,relief='ridge',bd=3,bg = "#ffdead",font=('chiller',40,'italic bold'),fg='black')
introlabel.place(x=10,y=20)
ChangeIntroLabelColor()

listbox = Listbox(root,yscrollcommand=scrollbar.set,width=50,height=10,font=('arial',12,'italic bold'),relief='solid',bd=2,highlightcolor='yellow',highlightbackground='orange',highlightthickness=2)
listbox.place(x=20,y=230)
listbox.bind("<<ListboxSelect>>", selectcursor)

DownloadingSizeLabel = Label(root,text='Total size : ',font=('arial',13,'italic bold'),bg='skyblue')
DownloadingSizeLabel.place(x=500,y=240)

DownloadingSizeLabel = Label(root,text='Recived size : ',font=('arial',13,'italic bold'),bg='skyblue')
DownloadingSizeLabel.place(x=500,y=290)

DownloadingSizeLabel = Label(root,text='Time Left : ',font=('arial',13,'italic bold'),bg='skyblue')
DownloadingSizeLabel.place(x=500,y=340)

DownloadingSizeLabelResult = Label(root,text=' ',font=('arial',13,'italic bold'),bg='skyblue')
DownloadingSizeLabelResult.place(x=650,y=240)

DownloadingLabelResult = Label(root,text=' ',font=('arial',13,'italic bold'),bg='skyblue')
DownloadingLabelResult.place(x=650,y=290)

DownloadingLabelTimeLeft= Label(root,text=' ',font=('arial',13,'italic bold'),bg='skyblue')
DownloadingLabelTimeLeft.place(x=650,y=340)

DownloadingBarTextLable = Label(root,text='Downloading bar',width=36,font=('chiller',23,'italic bold'),fg='red',bg='skyblue',)
DownloadingBarTextLable.place(x=370,y=445)

DownloadingProgressBarLable = Label(root,text='',width=36,font=('chiller',40,'italic bold'),fg='red',bg='skyblue',relief='raised')
DownloadingProgressBarLable.place(x=20, y=445)

################################progress bar ################################
DownloadingProgressBar = Progressbar(DownloadingProgressBarLable,orient=HORIZONTAL,value=0,length=100,maximum=total12)
DownloadingProgressBar.grid(row=0, column=0, ipadx=185, ipady=3)


############################ BUTTONS ########################################
ClickButton = Button(root,text="Enter Url And Click",font=('Arial',10,'italic bold'),bg='#a81c07',fg='white',activebackground='#4169e1',width=23,bd=6,command=VideoUrl)
ClickButton.place(x=530,y=150)

DownloadButton = Button(root,text='Download',font=('Arial',10,'italic bold'),bg='#66023c',fg='white',activebackground='#8b0000',width=23,bd=6,command=DownloadVideo)
DownloadButton.place(x=530,y=370)

root.mainloop()






