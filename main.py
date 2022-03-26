from pytube import YouTube
from moviepy.editor import *
import os
import PySimpleGUI as sg


def link_taker():
    # take the link
    link = input('Enter the link: ')
    global yt
    yt = YouTube(link)


def info_spit():
    # spit it out
    print("Title: ", yt.title)
    print("Description: ", yt.description)
    print("Length: ", yt.length)


def mp4_maker():
    # print(yt.streams.filter(only_audio=True))
    ys = yt.streams.get_highest_resolution()
    ys.download()


def mp3_maker():
    # grab the title
    title = yt.title
    mp4_file = title + '.mp4'
    mp3_file = title + '.mp3'
    # convert it
    videoclip = VideoFileClip(mp4_file)
    audioclip = videoclip.audio
    audioclip.write_audiofile(mp3_file)
    # make it pretty
    audioclip.close()
    videoclip.close()
    # delete mp4
    os.remove(mp4_file)


def choice_question():
    while True:
        choice = input("MP4 or MP3? ")
        if choice.lower() == 'mp4':
            mp4_maker()
            break
        if choice.lower() == 'mp3':
            mp4_maker()
            mp3_maker()
            break
        else:
            print('Enter a valid format!')


def gui():
    sg.Window(title="Hello World!", layout=[[]], margins=(100, 50)).read()


link_taker()
info_spit()
choice_question()
