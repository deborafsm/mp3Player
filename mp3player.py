from ast import Lambda
from cProfile import label
from platform import libc_ver
from tkinter import *
from tkinter import filedialog
import time

import pygame 

root = Tk()
root.title('Mp3 Play - Wisp')
root.iconbitmap('music.ico')
root.geometry("355x350")
# initialze pygame mixer
pygame.mixer.init()

#get music time info 
def time_music():
    current_time = pygame.mixer.music.get_pos()/ 1000

    # time status convert
    convert_time_info_music = time.strftime('%H:%M:%S', time.gmtime(current_time))
    # Adiciona texto no status bar 
    status_bar.config(text=convert_time_info_music)
    # up time
    status_bar.after(1000, time_music)


# Add songs function
def delete_song():
    # Delete a song song
    box_player.delete(ANCHOR)
    pygame.mixer.music.stop()
def delete_all_songs():
    # Delete all song
    box_player.delete(0, END)
    pygame.mixer.music.stop()
def add_song():
    song = filedialog.askopenfilename(initialdir = "music", title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
    # Strip out the directory info and .mp3 
    song = song.replace("C:/Users/Code/Documents/GitHub/mp3Player/music", "")
    song = song.replace(".mp3", "")
    # Add Songs in list
    box_player.insert(END, song)
def many_song():
    songs = filedialog.askopenfilenames(initialdir = "music", title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"),))
#  Loop Many song
    for song in songs:
        song = song.replace("C:/Users/Code/Documents/GitHub/mp3Player/music/", "")
        song = song.replace(".mp3", "")
        # Insert songs in playList
        box_player.insert(END, song)
# Play Select song
def play():
    song =  box_player.get(ACTIVE)
    song = f'music/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Call the play time function
    time_music()
#var global 
global paused
paused = False
# Pause and UnPause Song
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        # Pause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # UnPause
        pygame.mixer.music.pause()
        paused = True
# Stop Song
def stop():
    pygame.mixer.music.stop()
    box_player.select_clear(ACTIVE)
        
def next_song():
    # pega a musica atual "get current"
    next_one = box_player.curselection()
    # acrescenta mais um "add one to the current song"
    next_one = next_one[0]+1
    # pega o titulo da musica  "grab the title"
    song = box_player.get(next_one)
    # adiciona ao diretorio 
    song = f'music/{song}.mp3'
    # Executa a musica
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Clear active bar in playlist listbox
    box_player.select_clear(0, END)
    #Active bar in the song "Ativa a seleção na proxima musica"
    box_player.activate(next_song)
    box_player.selection_set(next_one,last=None)
def back_song():
    # pega a musica atual "get current"
    back_one = box_player.curselection()
    # acrescenta menos um "add one to the current song"
    back_one = back_one[0]-1
    # pega o titulo da musica  "grab the title"
    song = box_player.get(back_one)
    # adiciona ao diretorio 
    song = f'music/{song}.mp3'
    # Executa a musica
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    #Clear active bar in playlist listbox
    box_player.select_clear(0, END)
    #Active bar in the song "Ativa a seleção na proxima musica"
    box_player.activate(next_song)
    box_player.selection_set(back_one,last=None)
# Create player box
# bg is background 
# fg is font color
# width is size of player box'
box_player = Listbox(root, bg="#15F244", fg="#15F244",highlightbackground='#080808',highlightcolor='#080808',background= '#080808',width=200, selectbackground='#080808')
box_player.pack(pady=10)

# Define box player buttons image
back_button_img  = PhotoImage(file='back.png')
play_button_img = PhotoImage(file='play.png')
pause_button_img = PhotoImage(file='pause.png')
stop_button_img =  PhotoImage(file='stop.png')
forward_button_img = PhotoImage(file= 'forward.png')

# Create Player control frames
controls_frame = Frame(root)
controls_frame.pack()
# Create Player control with buttons
back_button = Button(controls_frame, image= back_button_img,borderwidth=0, command=back_song)
play_button = Button(controls_frame, image=play_button_img,borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_button_img, borderwidth=0,command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_button_img, borderwidth=0,command=stop)
forward_button = Button(controls_frame, image=forward_button_img, borderwidth=0, command=next_song)

back_button.grid(row=0, column=0)
play_button.grid(row=0, column=1)
pause_button.grid(row=0, column=2)
stop_button.grid(row=0, column=3)
forward_button.grid(row=0, column=4)





# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add Songs
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add Many Song to PlayList", command=many_song)
add_song_menu.add_command(label="Add One Song to PlayList", command=add_song)

# Delete Song 
menu_del_song = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=menu_del_song)
menu_del_song.add_command(label="Delete a Song from Playlist", command=delete_song)
menu_del_song.add_command(label="Delete ALL Song from Playlist", command=delete_all_songs)


# status bar
status_bar = Label(root, text = '', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipadx=2)
root.mainloop() 