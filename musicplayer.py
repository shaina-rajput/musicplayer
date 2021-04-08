import tkinter
from tkinter import messagebox
from tkinter import StringVar
from tkinter import IntVar
from tkinter.ttk import *
from tkinter import filedialog
from mutagen.mp3 import MP3
from pygame import mixer
import mysql.connector
import threading
import time
import os
import shutil

convar=mysql.connector.connect(
   host='localhost',
   user='root',
   passwd='',
   database='musicplayer'
    )
mycur=convar.cursor()
#variables
window1=None
window2=None
window3=None


playlist=[]

def window2opener():
    window1.destroy()
    musicplayer()


def window3opener():
    playsong()





#********************************************music player******************************
def browse():
    global info
    global audio_file_name
    global mycur
    global convar
    global list1
    audio_file_name = filedialog.askopenfilename(filetypes=(("Audio Files", ".wav .mp3"),("Music", "*.*")))
    filename=os.path.basename(audio_file_name)
    print(filename)
    mycur.execute('insert into music(songname) values("'+str(filename)+'")')
    convar.commit()
    list1.delete(0,'end')
    query1="SELECT *FROM music"
    mycur.execute(query1)
    music=mycur.fetchall()
    index=0
    for x in music:
        list1.insert(index,x)
        playlist.append(x)
        index=index+1
    print(playlist)
    path='D:\\'
    source=os.path.join(path,"New folder\\", filename)
    print(source)
    
    
    dest = shutil.copy(source,"C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python37 " )
    symlinks=True 
    print("Destination path:", dest) 

    
paused=False
def pausemusic():
    global paused
    global info
    global playit
    
    if(paused==False):
        paused=True
        mixer.music.pause()
        photo1=tkinter.PhotoImage(file='play (1).png')
        window2.one=photo1
        btnplay=tkinter.Button(window3,image=photo1,bg='black',activebackground='light pink',command=pausemusic)
        btnplay.image=photo1
        btnplay.place(x=800,y=450)
        info['text']=playit+'  music paused'

    else:
        mixer.music.unpause()
        photo3=tkinter.PhotoImage(file='shapes-and-symbols.png')
        window2.one=photo3
        btnpause=tkinter.Button(window3,image=photo3,bg='black',activebackground='light pink',command=pausemusic)
        btnpause.image=photo3
        btnpause.place(x=800,y=450)
        
        info['text']='Now playing  '+playit
        paused=False

   
def playmusic():
    global list1

    try:
            selected_song=list1.curselection()
            print(selected_song)
            selected_song=int(selected_song[0])
            playit=playlist[selected_song]
            playit=(playit[0])
            mixer.music.load(playit)
            mixer.music.play()
    except:
            tkinter.messagebox.showinfo('oops','no music found')

stop=False    
    
def stopmusic():
    global stop
    global info
    global playit
    if(stop==False):
        mixer.music.stop()
        stop=True
        photo1=tkinter.PhotoImage(file='play (1).png')
        window2.one=photo1
        btnplay=tkinter.Button(window3,image=photo1,bg='black',activebackground='light pink',command=stopmusic)
        btnplay.image=photo1
        btnplay.place(x=710,y=450)
        info['text']=playit+'  music stopped'
    else:
        stop=False
        mixer.music.play()
        photo2=tkinter.PhotoImage(file='stop (1).png')
        window2.one=photo2
        btnstop=tkinter.Button(window3,image=photo2,bg='black',activebackground='light pink',command=stopmusic)
        btnstop.image=photo2
        info['text']=playit+'  music stopped'
        info['text']='Now playing  '+playit
        btnstop.place(x=710,y=450)
        
        
    
mute=False
def mutemusic():
    global mute
    global btnmute
    global scale
    global playit
    if (mute==False):
        mute=True
        photo4=tkinter.PhotoImage(file='mute.png')
        window2.one=photo4
        btnmute=tkinter.Button(window3,image=photo4,bg='black',activebackground='light pink',command=mutemusic)
        btnmute.image=photo4
        btnmute.place(x=850,y=650)
        scale.set(0)
        mixer.music.set_volume(0)
        info['text']=playit+'  music muted'
        
    else:
        photo5=tkinter.PhotoImage(file='sound-on.png')
        window2.one=photo5
        btnmute=tkinter.Button(window3,image=photo5,bg='black',activebackground='light pink',command=mutemusic)
        btnmute.image=photo5
        btnmute.place(x=850,y=650)
        scale.set(50)
        mixer.music.set_volume(0.5)
        info['text']='Now playing  '+playit
        mute=False
        

    
def set_vol(val):
    volume=int(val)/100
    mixer.music.set_volume(volume)

def nextmusic():
    global selected_song1
    global playit
    global selected_song
    global playlist
    try:
        selected_song1+=1
        playit=playlist[selected_song1]
        playit=(playit[0])
        mixer.music.load(playit)
        mixer.music.play()
        info['text']='Now playing  '+playit
    except:
        playit=playlist[0]
        playit=playit[0]
        mixer.music.load(playit)
        mixer.music.play()
        info['text']='Now playing  '+playit

def prevmusic():
    global selected_song1
    global playit
    global selected_song
    global playlist
    try:
        selected_song1-=1
        playit=playlist[selected_song1]
        playit=(playit[0])
        mixer.music.load(playit)
        mixer.music.play()
        info['text']='Now playing  '+playit
    except:
        playit=playlist[-1]
        playit=playit[0]
        mixer.music.load(playit)
        mixer.music.play()
        info['text']='Now playing  '+playit
        
def searchsong():
    global search
    musicvalue=search.get()
    try:
        index=Listbox.get(0,'end').index(musicvalue)
        return index
    except:
        tkinter.messagebox.showinfo('oops','no music found')

    
def playsong():
    global music
    global list1
    global btnmute
    global scale
    global info
    global playit
    global selected_song1
    global selected_song
    selected_song=list1.curselection()
    print(selected_song)
    selected_song1=int(selected_song[0])
    print(selected_song1)
    playit=playlist[selected_song1]
    
    playit=(playit[0])
    mixer.music.load(playit)
    mixer.music.play()
    info=tkinter.Label(window3,bg='black',fg='light pink',font=('Gabriola',20))
    info['text']='Now playing  '+playit
    info.place(x=650,y=20)
    lengthlabel=tkinter.Label(window3,bg='black',fg='light pink',font=('Gabriola'))
    lengthlabel.place(x=900,y=400)
    audio=MP3(playit)
    total_length=audio.info.length
    mins,secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text']='Total length  -   '+timeformat
    lengthlabel.place(x=950,y=420)
    photo=tkinter.PhotoImage(file='mainmusic (1).png')
    window2.one=photo
    lblpic=tkinter.Label(window2,image=photo,bg='black')
    lblpic.image=photo
    lblpic.place(x=600,y=70)

    photo2=tkinter.PhotoImage(file='stop (1).png')
    window2.one=photo2
    btnstop=tkinter.Button(window3,image=photo2,bg='black',activebackground='light pink',command=stopmusic)
    btnstop.image=photo2
    btnstop.place(x=710,y=450)
    
    photo3=tkinter.PhotoImage(file='shapes-and-symbols.png')
    window2.one=photo3
    btnpause=tkinter.Button(window3,image=photo3,bg='black',activebackground='light pink',command=pausemusic)
    btnpause.image=photo3
    btnpause.place(x=800,y=450)

    photo3=tkinter.PhotoImage(file='next.png')
    window2.one=photo3
    btnnext=tkinter.Button(window3,image=photo3,bg='black',activebackground='light pink',command=nextmusic)
    btnnext.image=photo3
    btnnext.place(x=890,y=470)

    photo3=tkinter.PhotoImage(file='back.png')
    window2.one=photo3
    btnprev=tkinter.Button(window3,image=photo3,bg='black',activebackground='light pink',command=prevmusic)
    btnprev.image=photo3
    btnprev.place(x=650,y=470)
    
    photo5=tkinter.PhotoImage(file='sound-on.png')
    window2.one=photo5
    btnmute=tkinter.Button(window3,image=photo5,bg='black',activebackground='light pink',command=mutemusic)
    btnmute.image=photo5
    btnmute.place(x=850,y=650)

    scale=tkinter.Scale(window3,from_=0,to=100,orient='horizontal', background='black', cursor='heart',relief='groove',troughcolor='black' ,fg='light pink', activebackground='light pink',command=set_vol)
    scale.set(50)
    scale.place(x=920,y=645,height=50,width=200)

def musicplayer():
    global window2
    global search1
    global music
    global playlist
    global list1
    global search
    window2=tkinter.Tk()
    window2.geometry('1150x700+80+0')
    search1=StringVar(window2)
    window2.configure(background='black')
    window2.title('la musica',)
    window2.iconbitmap(r'favicon (5).ico')
    search=tkinter.Button(window2,bg='black',fg='light pink',command=browse)
    search.place(x=140,y=30,height=30,width=360)

    photo3=tkinter.PhotoImage(file='search.png')

    btnplay=tkinter.Label(window2,image=photo3,bg='black')
    btnplay.image=photo3
    btnplay.place(x=100,y=25)

    list1=tkinter.Listbox(window2,bg='black',fg='light pink',selectbackground='light pink')
    list1.place(x=100,y=80,height=400,width=400)

    query1="SELECT *FROM music"
    mycur.execute(query1)
    music=mycur.fetchall()
    index=0
    for x in music:
        list1.insert(index,x)
        playlist.append(x)
        index=index+1
    print(playlist)

    photo1=tkinter.PhotoImage(file='google-play-music.png')
    window2.one=photo1
    btnplay=tkinter.Button(window2,image=photo1,bg='black',activebackground='light pink',command=window3opener)
    btnplay.image=photo1
    btnplay.place(x=330,y=500)

    ply=tkinter.Label(window2,text='PLAY',font=('Forte',25),bg='black',fg='light pink')
    ply.place(x=220,y=520)
   
#****************************************musicplayer ends***************************
#************************************main page**************************************
window1=tkinter.Tk()

mixer.init()

window1.geometry('600x600+400+50')

window1.configure(background='black')
window1.title('la musica',)
window1.iconbitmap(r'favicon (5).ico')
head=tkinter.Label(window1,text='La Musica',font=('Jokerman',80),fg='light pink',bg='black')
head.pack()

usrlbl=tkinter.Label(window1,text='When words fails MUSIC speaks',font=('Forte',15),bg='black',fg='light pink')
usrlbl.place(x=220,y=150)

photo=tkinter.PhotoImage(file='play.png')
btnplay=tkinter.Button(window1,image=photo,bg='black',activebackground='light pink',command=window2opener)
btnplay.place(x=250,y=260)

usrlbl=tkinter.Label(window1,text='lets make some noise',font=('Forte',15),bg='black',fg='light pink')
usrlbl.place(x=220,y=450)

photo1=tkinter.PhotoImage(file='sing.png')
btnpic=tkinter.Label(window1,image=photo1,bg='black',activebackground='light pink')
btnpic.place(x=80,y=450)
#***********************************main page ends*******************************************
