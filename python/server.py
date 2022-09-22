import socket
import threading
from threading import Thread
import tkinter as tk
import mysql.connector as sql
import datetime
import sys

# HOST VARIES DEPENDING ON THE MACHINE IT IS RUNNING ON

HOST = '192.168.0.38'
PORT = 65432
FORMAT = 'utf-8'
HEADER = 1024
ADDR = (HOST, PORT)

# CONNECTS TO DATABASE

db = sql.connect(
    host='localhost',
    user='root',
    password='',
    database='distributedsystems'
)

cursor = db.cursor()
listcursor = db.cursor()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

# UPDATES LIST OF SONG AT THE START BY FETCHING THEM FROM THE DATABASE

def update_listbox():
    sql = ("SELECT artist.Name AS artist, song.Name AS song FROM song INNER JOIN album ON album.ID=song.Album_ID INNER JOIN artist ON album.Artist_ID=artist.ID")
    listcursor.execute(sql)
    songslist = listcursor.fetchall()

    for x in songslist:
        song_listbox.insert("end", x[0] + "-" + x[1])

# THREAD THAT IS CREATED EVERYTIME A CLIENT MAKES A REQUEST

def handle_client(conn, addr):
    connected = True

    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            splitmsg = msg.split('#')

            if splitmsg[1] == 'register':
                sql = ("SELECT Username FROM account WHERE Username = %s")
                val = (splitmsg[2],)
                cursor.execute(sql, val)
                row = cursor.fetchall()

                try:
                    if row[0] == val:
                        connected_listbox.insert("end", str(addr) + " : Register fail at " + str(datetime.datetime.now()))
                        conn.send("#failregister".encode(FORMAT))
                except:
                    connected_listbox.insert("end", str(addr) + " : Register success at " + str(datetime.datetime.now()))
                    sql = ("INSERT INTO account (Username, Password) VALUES (%s, %s)")
                    val = (splitmsg[2],splitmsg[3])
                    cursor.execute(sql, val)

                    db.commit()
                    conn.send("#successregister".encode(FORMAT))

            elif splitmsg[1] == 'login':
                sql = ("SELECT Username, Password FROM account WHERE Username = %s")
                val = (splitmsg[2],)
                cursor.execute(sql, val)

                row = cursor.fetchall()
                newlist = (splitmsg[2],splitmsg[3])

                try:
                    if row[0] == newlist:
                        connected_listbox.insert("end", str(addr) + " : Login success at " + str(datetime.datetime.now()))
                        conn.send("#successlogin".encode(FORMAT))
                    else:
                        connected_listbox.insert("end", str(addr) + " : Login fail at " + str(datetime.datetime.now()))
                        conn.send("#faillogin".encode(FORMAT))

                except:
                    conn.send("#faillogin".encode(FORMAT))

            elif splitmsg[1] == 'songlist':
                songlist = "#songlist,"
                for x, entry in enumerate(song_listbox.get(0, "end")):
                    songlist += entry + ","
                conn.send(songlist.encode(FORMAT))
                connected_listbox.insert("end", str(addr) + " : Song list request at " + str(datetime.datetime.now()))
            
            elif splitmsg[1] == 'songrequest':
                connected_listbox.insert("end", str(addr) + " : Song request at " + str(datetime.datetime.now()))
                file = open("songs/"+splitmsg[2]+".mp3", 'rb')
                file_data = file.read()
                conn.sendall(file_data)
                file.close()
            
            cursor.reset()
            connected = False
            conn.close()
            sys.exit()
    
# STARTS THE SERVER AND CREATES NEW THREAD THAT LISTENS TO INCOMING MESSAGES

def start():
    print(f"Server is listening on {HOST}")

    server_socket.listen()
    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def quit():
    sys.exit()

def main():

    print(f"Server is starting...")

    # CREATES MAIN WINDOW

    window = tk.Tk()
    window.title('Server')
    window.columnconfigure([0, 1], weight=1, minsize=20)
    window.rowconfigure([0, 1, 2], weight=1, minsize=30)

    connected_label = tk.Label(text="Connection history:", height=1)
    connected_label.grid(row=0, column=0, sticky="nsew")

    songlist_label = tk.Label(text="Songs:", height=1)
    songlist_label.grid(row=0, column=1, sticky="nsew")

    global song_listbox
    song_listbox = tk.Listbox(width=40, height=30)
    song_listbox.grid(row=1, column=1, sticky="nsew")

    global connected_listbox
    connected_listbox = tk.Listbox(width=50, height=10)
    connected_listbox.grid(row=1, column=0, sticky="nsew")

    disconnect = tk.Button(text="Close Server", command=quit, height=3)
    disconnect.grid(row=2, column=1, sticky="wes")

    update_listbox()

    control_thread = Thread(target=start, daemon=True)
    control_thread.start()

    window.mainloop()
    control_thread.join()

if __name__ == "__main__":
    main()