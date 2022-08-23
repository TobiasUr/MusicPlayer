from distutils.cmd import Command
from logging import root
from pickle import STOP
from tkinter import*
from tkinter import filedialog
from turtle import clear
from winreg import DeleteKey
import pygame
import time
from mutagen.mp3 import MP3
import sys
import os
import keyboard
import tkinter.ttk as ttk


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


root = Tk()
root.title('MusicPlayer')
root.iconbitmap(resource_path('icon.ico'))
root.geometry("500x370")
global currentSong
currentSong = 'none'



pygame.mixer.init()

def playTime():
    if stopped:
        return
    global currentSong
    currentTime = pygame.mixer.music.get_pos() / 1000
    
    convertedCurrentTime = time.strftime('%H:%M:%S', time.gmtime(currentTime))
    
    currentOne = currentSong
    song = songBox.get(currentOne)
    songMut = MP3(song)
    global songLenght
    songLenght = songMut.info.length
    convertedTotalTime = time.strftime('%H:%M:%S', time.gmtime(songLenght))

    currentTime += 1

    if int(slider.get()) == int(songLenght):
        nextSong()
    elif paused:
        convertedCurrentTime = time.strftime('%H:%M:%S', time.gmtime(int(slider.get())))
    elif int(slider.get()) == int(currentTime):
        sliderPosition = int(songLenght)
        slider.config(to=sliderPosition, value=int(currentTime))

    else:
        sliderPosition = int(songLenght)
        slider.config(to=sliderPosition, value=int(slider.get()))

        convertedCurrentTime = time.strftime('%H:%M:%S', time.gmtime(int(slider.get())))

        nextTime = int(slider.get()) +1
        slider.config(value=nextTime)

    if stopped == False:
        statusBar.config(text=f'{convertedCurrentTime} / {convertedTotalTime}')

    statusBar.after(1000, playTime)


def addSong():
    song = filedialog.askopenfilename(initialdir='Music/', title="Choose a Song", filetypes=(("mp3 files", "*.mp3"), ("wav Files", "*.wav"), ))  
    songBox.insert(END, song)
    

def addManySongs():
    songs = filedialog.askopenfilenames(initialdir='Music/', title="Choose a Song", filetypes=(("mp3 files", "*.mp3"), ("wav Files", "*.wav"), ))

    for song in songs:
        songBox.insert(END, song)

def deleteSong():
    print("Delete")
    global currentSong
    ActiveSong = songBox.curselection()
    ActiveSong = ActiveSong[0]
    if currentSong == songBox.curselection():
        stop()
    songBox.delete(ACTIVE)


def deleteAllSongs():
    songBox.delete(0, END)
    stop()

def play():
    global currentSong
    song= songBox.get(ACTIVE)
    song= f'{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    currentSong = songBox.curselection()
    global stopped
    stopped = False
    playTime()

global stopped
stopped = False

def stop():
    slider.config(value=0)
    pygame.mixer.music.stop()
    songBox.select_clear(ACTIVE)
    statusBar.config(text='')

    global stopped
    stopped = True 

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused


    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:   
        pygame.mixer.music.pause()
        paused = True

def nextSong():
    global currentSong
    nextOne = currentSong
    nextOne = nextOne[0]+1
    song = songBox.get(nextOne)
    songBox.selection_clear(0, END)
    songBox.activate(nextOne) 
    songBox.select_set(nextOne, last=None)
    currentSong = songBox.curselection()
    slider.config(value=0)
    play()

def prevSong():
    global currentSong
    nextOne = currentSong
    nextOne = nextOne[0]-1
    song = songBox.get(nextOne)
    songBox.selection_clear(0, END)
    songBox.activate(nextOne)
    songBox.select_set(nextOne, last=None)
    currentSong = songBox.curselection()
    slider.config(value=0)
    play()


#sliderFunction
def slide(x):
    song= songBox.get(ACTIVE)
    song= f'{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(slider.get()))

songBox = Listbox(root, bg="grey", fg="black", width=60, selectbackground="gray", selectforeground="white")
songBox.pack(pady=20)

#defineButtons
backButtonImg = PhotoImage(file=resource_path('previoussong.png'))
forwardButtonImg= PhotoImage(file=resource_path('nextsong.png'))
playButtonImg= PhotoImage(file=resource_path('play.png'))
pauseButtonImg= PhotoImage(file=resource_path('pause.png'))
stopButtonImg= PhotoImage(file=resource_path('stop.png'))

#createFrames
controlsFrame = Frame(root)
controlsFrame.pack()

#createButtons
backButton = Button(controlsFrame, image=backButtonImg, borderwidth=0, command=prevSong) 
forwardButton = Button(controlsFrame, image=forwardButtonImg, borderwidth=0, command=nextSong)
playButton = Button(controlsFrame, image=playButtonImg, borderwidth=0, command=play)
pauseButton = Button(controlsFrame, image=pauseButtonImg, borderwidth=0, command=lambda: pause(paused))
stopButton = Button(controlsFrame, image=stopButtonImg, borderwidth=0, command=stop)

backButton.grid(row=0, column=0, padx=10)
forwardButton.grid(row=0, column=4, padx=10)
playButton.grid(row=0, column=1, padx=10)
pauseButton.grid(row=0, column=2, padx=10)
stopButton.grid(row=0, column=3, padx=10)


#createmenu
myMenu = Menu(root)
root.config(menu=myMenu)

#addSOngMenu
addSongMenu = Menu(myMenu)
myMenu.add_cascade(label="Add Songs", menu=addSongMenu)
addSongMenu.add_command(label="Add One Song to Playlist", command= addSong)
#AddManySongs
addSongMenu.add_command(label="Add Many Songs to Playlist", command= addManySongs)
#RemoveSong
removeSongMenu = Menu(myMenu)
myMenu.add_cascade(label="Remove Songs", menu=removeSongMenu)
removeSongMenu.add_command(label="Delete song from playlist", command=deleteSong)
removeSongMenu.add_command(label="Delete all songs from playlist", command=deleteAllSongs)

#crete status bar
statusBar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
statusBar.pack(fill=X, side=BOTTOM, ipady=2)

#CreatePositionSlider
slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
slider.pack(pady=20)


#Keyboard


root.mainloop()