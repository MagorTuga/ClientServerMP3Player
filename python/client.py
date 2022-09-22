import socket
from threading import Thread
import tkinter as tk
import time
import pygame
from tkinter.constants import ANCHOR, BOTH, CENTER, E, EW, HORIZONTAL, RIGHT, W
import os
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

global host
host = ''
PORT = 65432
FORMAT = 'utf-8'
HEADER = 1024
ADDR = (host, PORT)
SONGTOREQUEST = ''

username = ""
password = ""

global songplaying
songplaying = False

global song_array
song_array = []

pygame.mixer.init()

# USED BY THE LOGIN AND REGISTER WINDOWS TO COMMUNICATE WITH THE SERVER

def send(tosend):
    try:
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect(ADDR)
        print(f"Connected to {ADDR}")
        message = tosend.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        socket_client.send(send_length)
        socket_client.send(message)

    except:
        print("Could not connect to server.")

    receiving = True

    while receiving:
        msg = socket_client.recv(HEADER).decode(FORMAT)

        if msg == "#faillogin":
            print("Could not login.")
            receiving = False
            return 0

        elif msg == "#successlogin":
            print("Successfully logged in.")
            receiving = False
            main_window()

        elif msg == "#failregister":
            print("Could not register.")
            receiving = False
            return 0

        elif msg == "#successregister":
            print("Successfully registered.")
            receiving = False
            return 1

# USED BY THE MAIN WINDOW TO REQUEST THE LIST OF SONGS AND STORES THEM IN A LIST

def getsongslist(tosend, list):
    global song_array
    try:
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_client.connect(ADDR)
        print(f"Connected to {ADDR}")
        message = tosend.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        socket_client.send(send_length)
        socket_client.send(message)

    except:
        print("Could not connect to server.")

    receiving = True

    while receiving:
        msg = socket_client.recv(HEADER).decode(FORMAT)
        if len(msg) > 0:
            print("Incoming songs...")
            splitmsg = msg.split(',')
            song_array.clear()
            for x in splitmsg:
                if x != "#songlist" and len(x) > 0:
                    song_array.append(x)
                    list.insert("end", x)
            socket_client.close()
            print("Succesfully received songs.")
            quit()

# USED BY THE MAIN WINDOW TO SET THE SONG TO REQUEST WHEN CLICKING ON IT FROM THE LIST BOX

def setsongtorequest(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            global SONGTOREQUEST
            SONGTOREQUEST = event.widget.get(index)

# USED BY THE MAIN WINDOW TO REQUEST A SONG FROM THE SERVER AND/OR PLAY IT

def requestsong():
    global SONGTOREQUEST
    global songplaying
    global song_length
    print("Requesting song...")
    
    if len(SONGTOREQUEST) > 0:

        progress_bar.config(value=0)
        songtofind = SONGTOREQUEST.replace(" ", "_")
        if os.path.isfile('temp_songs/'+songtofind+'.mp3'):

            pygame.mixer.music.load('temp_songs/'+songtofind+'.mp3')
            pygame.mixer.music.play()
            songplaying = True

            songpath = "temp_songs/" +SONGTOREQUEST.replace(" ", "_")+".mp3"
            song_mut = MP3(songpath)
            song_length = song_mut.info.length
            converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
            song_length_label.config(text=converted_song_length)

            slider_position = int(song_length)
            progress_bar.config(to=slider_position)

        else:
            try:
                socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_client.connect(ADDR)
                print(f"Connected to {ADDR}")
                message = ('#songrequest#' + songtofind).encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                socket_client.send(send_length)
                socket_client.send(message)

                print("Requesting ", songtofind)
                file = open("temp_songs/"+songtofind+".mp3", 'wb')

                receiving = True

                while receiving:
                    msg = socket_client.recv(4096)
                    file.write(msg)
                    if len(msg) < 1:
                        file.close()
                        socket_client.close()
                        receiving = False
                        print("Song retrieved! Playing...")
                        pygame.mixer.music.load('temp_songs/'+songtofind+'.mp3')
                        pygame.mixer.music.play()
                        songplaying = True

                        songpath = "temp_songs/" +SONGTOREQUEST.replace(" ", "_")+".mp3"
                        song_mut = MP3(songpath)
                        song_length = song_mut.info.length
                        converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
                        song_length_label.config(text=converted_song_length)


                        slider_position = int(song_length)
                        progress_bar.config(to=slider_position)

            except:
                print("Could not get song.")
            
    else:
        print("No song selected.")

# USED BY THE MAIN WINDOW TO PAUSE OR UNPAUSE THE CURRENTLY PLAYING SONG

def pause():
    global songplaying
    if songplaying:
        pygame.mixer.music.pause()
        songplaying = False
    else:
        pygame.mixer.music.unpause()
        songplaying = True

# THREAD INITIALIZED ALONG WITH THE MAIN WINDOW, KEEPS TRACK OF THE TIME OF THE CURRENT SONG AND UPDATES THE SCREEN EVERY SECOND WHEN PLAYING

def playtime():
    threadrunning=True
    global current_time
    global song_length
    current_time = 0
    while threadrunning: 
        global songplaying
        if songplaying:
            if int(progress_bar.get()) != current_time:
                current_time = int(progress_bar.get())
            if int(progress_bar.get()) == song_length:
                pygame.mixer.music.stop()
                songplaying = False
                print("Song has ended.")
            
            progress_bar.config(value=int(progress_bar.get()+1))

            fixed_current_time = time.strftime('%M:%S', time.gmtime(current_time))
            song_current_time.config(text=fixed_current_time)

            print(f'{current_time} and {int(pygame.mixer.music.get_pos() / 1000)}')

        time.sleep(1)

# STARTS THE ABOVE MENTIONED THREAD

def start_playtime():
    time_thread = Thread(target=playtime, daemon=True)
    time_thread.start()

def progress(self):
    pygame.mixer.music.set_pos(int(progress_bar.get()))

# USED BY THE MAIN WINDOW TO NARROW THE LIST OF SONGS SHOWN IN THE LIST BOX

def search(param, songlist):
    global song_array
    print("Entered search")
    songlist.delete(0, "end")
    if param == "":
        for x in song_array:
            songlist.insert("end", x)
    else:
        for x in song_array:
            if x.find(param) > 0:
                songlist.insert("end", x)

# CREATES CLIENT WINDOW, USED FIRST BY THE LOGIN SCREEN

window = tk.Tk()
window.title('Client')
frame = tk.Frame(window)
frame.columnconfigure([0,1], weight=1, minsize=10)
frame.rowconfigure([0,1,2,3,4,5], weight=1, minsize=10)

# CALLED AFTER A SUCCESSFUL LOGIN ATTEMPT, CLEARS THE CURRENT FRAME AND CREATES THE MAIN WINDOW

def main_window():

    start_playtime()

    global loggedinuser
    global frame
    frame.destroy()
    frame = tk.Frame(window)

    frame.columnconfigure([0,1], weight=1, minsize=10)
    frame.rowconfigure([0,1,2,3,4,5], weight=1, minsize=10)

    list_of_songs = tk.Listbox(width=40)
    list_of_songs.grid(in_=frame, row=0, column=0, columnspan=2)

    search_bar = tk.Entry()
    search_bar.grid(in_=frame, row=1, column=0, sticky=EW)

    search_button = tk.Button(text="Search", bg="grey", fg="black", command= lambda: search(search_bar.get(), list_of_songs))
    search_button.grid(in_=frame, row=1, column=1, sticky=EW)

    global progress_bar
    progress_bar = ttk.Scale(from_=0, to=100, orient=HORIZONTAL, value=0, command=progress)
    progress_bar.grid(in_=frame, row=2, column=0, columnspan=2, sticky=EW)

    global song_current_time
    song_current_time = tk.Label(text="")
    song_current_time.grid(in_=frame, row=3, column=0)

    global song_length_label
    song_length_label = tk.Label(text="")
    song_length_label.grid(in_=frame, row=3, column=1)

    song_play = tk.Button(text="Play", bg="black", fg="white", command=requestsong)
    song_play.grid(in_=frame, row=4, column=0, sticky=W)

    song_pause = tk.Button(text="Pause/Unpause", bg="black", fg="white", command=pause)
    song_pause.grid(in_=frame, row=4, column=1, sticky=E)
    
    user_name = tk.Label(text=loggedinuser)
    user_name.grid(in_=frame, row=5, column=0, sticky=W)

    logout_button = tk.Button(text="Logout", bg="grey", fg="black", command= lambda: [pygame.mixer.music.stop(), login_window()])
    logout_button.grid(in_=frame, row=5, column=1, sticky=E)

    frame.pack()

    list_of_songs.bind("<<ListboxSelect>>", setsongtorequest)

    getsongslist("#songlist", list_of_songs)

# CLEARS THE CURRENT FRAME TO CREATE THE REGISTER WINDOW

def register_window():

    global frame
    frame.destroy()
    frame = tk.Frame(window)


    register_user_label = tk.Label(text="Username:")
    register_user_label.grid(in_=frame, row=0, column=0)

    register_user_entry = tk.Entry(width=20)
    register_user_entry.grid(in_=frame, row=0, column=1)

    register_password_label = tk.Label(text="Password:")
    register_password_label.grid(in_=frame, row=1, column=0)

    register_password_entry = tk.Entry(width=20)
    register_password_entry.grid(in_=frame, row=1, column=1)

    register_message_label = tk.Label(text="")
    register_message_label.grid(in_=frame, row=2, column=0, columnspan=2)

    register_ip_label = tk.Label(text="Server IP:")
    register_ip_label.grid(in_=frame, row=3, column=0)

    register_ip_entry = tk.Entry(width=20)
    register_ip_entry.grid(in_=frame, row=3, column=1)

    register_register_button = tk.Button(text="Create Account", width=20, height=1, command= lambda: access_account("#register", register_message_label, register_user_entry.get(),register_password_entry.get(), register_ip_entry.get()))
    register_register_button.grid(in_=frame, row=4, columnspan=2)

    register_cancel_button = tk.Button(text="Cancel", width=20, height=1, command=login_window)
    register_cancel_button.grid(in_=frame, row=5, columnspan=2)

    frame.pack()

# USED BY THE LOGIN WINDOW TO CONNECT TO THE SERVER

def access_account(type, messagefield, username, password, ip):

    global loggedinuser
    loggedinuser = username

    global host
    host = ip

    global ADDR
    ADDR = (host, PORT)
    
    try:
        userpass = type + "#" + username + "#" + password
        if send(userpass) == 1:
            messagefield["text"] = "Successfully registered"
        else:
            messagefield["text"] = "Failed to register"
    except:
        messagefield["text"] = "Attempt to connect failed"

# CLEARS THE CURRENT FRAME TO CREATE THE LOGIN WINDOW

def login_window():

    global frame

    try:
        frame.destroy()
        frame = tk.Frame(window)
    except:
        print("No frame to destroy.")

    login_user_label = tk.Label(text="Username:")
    login_user_label.grid(in_=frame, row=0, column=0)

    login_user_entry = tk.Entry(width=20)
    login_user_entry.grid(in_=frame, row=0, column=1)

    login_password_label = tk.Label(text="Password:")
    login_password_label.grid(in_=frame, row=1, column=0)

    login_password_entry = tk.Entry(width=20)
    login_password_entry.grid(in_=frame, row=1, column=1)

    login_message_label = tk.Label(text="")
    login_message_label.grid(in_=frame, row=2, column=0, columnspan=2)

    login_ip_label = tk.Label(text="Server IP:")
    login_ip_label.grid(in_=frame, row=3, column=0)

    login_ip_entry = tk.Entry(width=20)
    login_ip_entry.grid(in_=frame, row=3, column=1)

    login_login_button = tk.Button(text="Login", width=20, height=1, command= lambda: access_account("#login", login_message_label, login_user_entry.get(), login_password_entry.get(), login_ip_entry.get()))
    login_login_button.grid(in_=frame, row=4, columnspan=2)

    login_register_button = tk.Button(text="Register", width=20, height=1, command=register_window)
    login_register_button.grid(in_=frame, row=5, columnspan=2)
    frame.pack()

def main():

    try:
     os.mkdir("temp_songs")
    finally:
        login_window()
        window.resizable(False, False)
        window.mainloop()

if __name__ == "__main__":
    main()
