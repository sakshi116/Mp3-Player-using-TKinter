from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()


root.title("MP3 Player")
root.geometry("500x450")

#initalize pygame
pygame.mixer.init()

#create function for current time
def play_time():
	#check to see if song is stopped
	if stopped:
		return 
	#grab current song time
	current_time = pygame.mixer.music.get_pos()/1000
	#convert song time to time format
	converted_current_time= time.strftime('%M:%S',time.gmtime(current_time))

	#reconstucting song with directory structure 
	song = playlist_box.get(ACTIVE)
	song = f'C:/Users/sakshi/Desktop/mp3 player/audio/{song}.mp3'

	#find current song length
	song_mut= MP3(song)
	global song_length
	song_length = song_mut.info.length

	#convert to time format
	converted_song_length = time.strftime('%M:%S',time.gmtime(song_length))
	#check to see if song is over
	if int(song_slider.get())==int(song_length):
		stop()


	elif paused:
		#check to sree if paused , if so- pass
		song_slider.config(value=current_time)
	else:
		#move slider along 1 second at a time
		next_time= int(song_slider.get())+1

		#new time on slider
		song_slider.config(to=song_length, value=next_time)

		#convert slider positioning 
		converted_current_time= time.strftime('%M:%S',time.gmtime(int(song_slider.get())))

		#output slider
		status_bar.config(text=f'')

	#add current time to status bar
	if current_time >= 1:
		status_bar.config(text=f'Time Elapsed:{converted_current_time} of {converted_song_length}  ')

	# create loop to check the time every second
	status_bar.after(1000, play_time)
# Add one Song
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files","*.mp3 "), ))
	#strip out directory structure and .mp3 extantiom
	song = song.replace("C:/Users/sakshi/Desktop/mp3 player/audio/", "") 
	song = song.replace(".mp3", "")
	#add to end of playlist
	playlist_box.insert(END, song)


# ADD many songs
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files","*.mp3 "), ))
	
	#loop thru song list and replace directory structure  and mp3 from song name
	for song in songs:
		#strip out directory structure and .mp3 extantiom
		song = song.replace("C:/Users/sakshi/Desktop/mp3 player/audio/", "") 
		song = song.replace(".mp3", "")
    	#add to end of playlist
		playlist_box.insert(END, song)

# create function to delete one song
def delete_song():
	playlist_box.delete(ANCHOR)

#create function to delete all songs
def delete_all_songs():

	playlist_box.delete(0, END)

#create play function
def play():
	#set stopped to flase as a song is playing
	global stopped
	stopped= False
	#reconstucting song with directory structure 
	song = playlist_box.get(ACTIVE)
	song = f'C:/Users/sakshi/Desktop/mp3 player/audio/{song}.mp3'
	#load song with pygame mixer
	pygame.mixer.music.load(song)
	#play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#get song time
	play_time()
#create stopped variable
global stopped
stopped = False

# stop fuction
def stop():
	#stop song
	pygame.mixer.music.stop()
	#clear playlist bar
	playlist_box.selection_clear(ACTIVE)

	status_bar.config(text='')

	#set our slider to zero
	song_slider.config(value=0)

	#set stop variableto true
	global stopped
	stopped = True

#create function for play next song
def next_song():
	#reset slider position to play the next song
	status_bar.config(text='')
	song_slider.config(value=0)

	#get current song number
	next_one = playlist_box.curselection()
	#add one to cuurent song
	next_one = next_one[0]+1
	#grab song title from yhe playlist
	song = playlist_box.get(next_one)
	#add directory structure stuff
	song = f'C:/Users/sakshi/Desktop/mp3 player/audio/{song}.mp3'
	#load song with pygame mixer
	pygame.mixer.music.load(song)
	#play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#clear active bar
	playlist_box.selection_clear(0, END)
	
	#move active barc
	playlist_box.activate(next_one)

	#set active bar
	playlist_box.selection_set(next_one, last=None)

#create function for play previous song
def previous_song():
	#reset slider position to play the next song
	status_bar.config(text='')
	song_slider.config(value=0)

	#get current song number
	next_one = playlist_box.curselection()
	#add one to cuurent song
	next_one = next_one[0]-1
	#grab song title from yhe playlist
	song = playlist_box.get(next_one)
	#add directory structure stuff
	song = f'C:/Users/sakshi/Desktop/mp3 player/audio/{song}.mp3'
	#load song with pygame mixer
	pygame.mixer.music.load(song)
	#play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	#clear active bar
	playlist_box.selection_clear(0, END)
	
	#move active barc
	playlist_box.activate(next_one)

	#set active bar
	playlist_box.selection_set(next_one, last=None)


#create paused variable
global paused
paused = False
#create pause function
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		#unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		#pause
		pygame.mixer.music.pause()
		paused = True

#create volume function
def volume(x):
	pygame.mixer.music.set_volume(volume_slider.get())

#slide function for song positioning
def slide(x):

	#reconstucting song with directory structure 
	song = playlist_box.get(ACTIVE)
	song = f'C:/Users/sakshi/Desktop/mp3 player/audio/{song}.mp3'
	#load song with pygame mixer
	pygame.mixer.music.load(song)
	#play song with pygame mixer
	pygame.mixer.music.play(loops=0, start= song_slider.get())

#create main frame
main_frame = Frame(root)
main_frame.pack(pady=20)

# Create Playlist Box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="blue")
playlist_box.grid(row=0, column=0)

#create volume slider frame
volume_frame = LabelFrame(main_frame, text="volume")
volume_frame.grid(row=0,column=1,padx=20)

#create volume slider
volume_slider = ttk.Scale(volume_frame, from_ =0, to=1, orient= VERTICAL, length=125, value=1, command=volume)
volume_slider.pack(pady=10)

#create song slider 
song_slider = ttk.Scale(main_frame, from_ =0, to=100, orient= HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)

#Define Button Images For Controls
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img = PhotoImage(file='images/forward.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')

# Create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

#Create Play/stop etc Buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command= next_song)
play_button = Button(control_frame, image= play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image= pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

#Create Menu
my_menu =  Menu(root)
root.config(menu=my_menu)

#Create Add Song Menu Dropdowns
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu= add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist",command=add_song)
add_song_menu.add_command(label="Add Many Songs To Playlist",command=add_many_songs)

# Create delete song manu dropdowns
remove_song_menu =Menu(my_menu)
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete One Song To Playlist",command=delete_song)
remove_song_menu.add_command(label="Delete All Songs To Playlist",command=delete_all_songs)

# create status bar
status_bar = Label(root, text='', bd=1, relief= GROOVE, anchor=E)
status_bar.pack(fill=X, side= BOTTOM, ipady=2)

# Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)

root.mainloop()