import threading
import socket
from FMS import classes
from FMS import functions
import sys
import os

home_directory = classes.Directory(name='home', hashTable=functions.loadFromDat(), path="/")
current_directory = home_directory
current_file = ""

def exec_command(command):
    global home_directory
    global current_directory
    global current_file
    with open(f'temp.txt', 'w') as sys.stdout:  #all print statements directed to file
        if "mkdir" in command:  
            words = command.split()    #1 = dir_name
            functions.mkDir(current_directory, words[1])
        elif "chdir" in command:
            words = command.split()    #1 = dir_name, 2 = mode
            words[1] = words[1].replace(',',"")    #removing comma
            if words[2] == "p":
                current_directory = functions.chDir(home_directory, current_directory, mode="parent")
            elif words[2] == "c":   #child
                current_directory = functions.chDir(current_directory,words[1], mode="child")
            elif words[2] == "f":   #full path
                current_directory = functions.chDir(home_directory, new_directory=words[1], mode = "path")
        elif "open" in command:
            words = command.split()    #1 = file_name, 2 = mode
            words[1] = words[1].replace(',',"")    #removing comma
            if words[2] == 'w':
                words[2] = "write"
            elif words[2] == 'r':
                words[2] = "read"
            current_file = functions.Open(current_directory, words[1], words[2])
        elif "close" in command:
            words = command.split()    #1 = file_name
            current_file = functions.Close(current_file)
        elif "create" in command:
            words = command.split()    #1 = file_name
            functions.create(current_directory, words[1])
        elif "delete" in command:
            words = command.split()    #1 = file_name
            functions.delete(current_directory, words[1])
        elif "write" in command:
            words = command.split()    #1 = file_name, 2 = text
            words[1] = words[1].replace(',',"")    #removing comma
            if isinstance(current_file, classes.File):
                current_file.writeToFile(text=words[2])
        elif "read" in command:
            words = command.split()    #1 = file_name
            print("\nContent: ")
            if isinstance(current_file, classes.File):
                current_file.writeToFile(text=words[2])
        elif "memory" in command:
            functions.printMemoryMap(home_directory)
        else:
            print("Invalid command")
        sys.stdout = sys.__stdout__     #redirect Output -> Failsafe incase threading fails before redirecting

def get_machine_ip():
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(("8.8.8.8", 80)) #Connecting to Google DNS to get IP
    return ip.getsockname()[0]

def handle_client(client_socket, addr):
    try:
        # Receive Name
        data = client_socket.recv(1024)
        name = data.decode('utf-8')
        print(name)
        while True:
            data = client_socket.recv(1024)
            # if no data was received, the connection was closed
            if not data:
                break
            # print the received data
            print(f"Received data from {addr[0]}:{addr[1]}: {data.decode('utf-8')}")
            ##### FMS ######
            exec_command(data.decode('utf-8'))
            with open('temp.txt', 'r') as file:
                data = file.read()
            os.remove("temp.txt")
            ################
            # send a response back to the client
            client_socket.send(data.encode('utf-8'))

    except Exception as e:
        print(f"An error occurred while handling the client {addr[0]}:{addr[1]}: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    device_ip = get_machine_ip()
    port = 95

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    server_socket.bind((host, port))

    server_socket.listen(5)
    print(f"Listening for incoming connections on {device_ip}:{port}...")

    while True:
        # Establish a connection
        client_socket, addr = server_socket.accept()

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()