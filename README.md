# Client Server MP3 Player

![Preview](https://github.com/MagorTuga/ClientServerMP3Player/blob/main/preview.png?raw=true)

Server requires connection to a database named “distributedsystems” with “root” as its user and no password. SQL query provided as “createdatabase.sql”.

Server requires a “songs” folder in the same directory with all the songs having a .mp3 extension titled under the format “Artist_name-Song_name”.

Server requires port forwarding if it is to receive connections from other machines.

Client does not require any preparation as it creates the “temp_”songs” folder by itself, if needed.

To use, run both executable client and server files. Server will not boot without the database running first.

# Functionality

Application allows for bi-directional communication. However, no encryption is implemented.

Both server and client have their GUI built with the Tkinter library.

On start, the server creates a thread that listens for incoming connections. When a message is received, the thread creates a new thread that will handle the client’s requests. It will then close itself when it’s done.

The server stores all information in an SQL database, the required file with test date is annexed in this submission as “createdatabase.sql”. The .mp3 files are not annexed, however.

Client can log in and register an account after selecting an IP address to connect to. Client displays error messages whenever it is unable to connect to the server.

Music player can play, pause, and skip ahead in the songs.

Server will show a list of the addresses of every connection along with timestamps of events.
