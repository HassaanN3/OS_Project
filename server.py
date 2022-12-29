import threading
import socket
from FMS import classes
from FMS import functions
import sys
import os

interface = """
\tDistributed File Management System

1. mkdir <dir_name>\t\t2. chdir <dir_name>, <mode>
3. create <file_name>\t\t4. delete <file_name>
5. open <file_name>, <mode>\t6. close <file_name>
7. read <file_name>\t\t8. write <file_name>, <content>
9. show_memory_map\t\t10. print
"""

# home_directory = classes.Directory(name='home', hashTable=functions.loadFromDat(), path="/")

home_directory = classes.Directory(name='home', hashTable=dict(), path="/")

def get_machine_ip():
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(("8.8.8.8", 80)) #Connecting to Google DNS to get IP
    return ip.getsockname()[0]

def exec_command(command, current_directory, current_file, name):
    global home_directory
    with open(f'temp{name}.txt', 'w') as sys.stdout:  #all print statements directed to file
        if "mkdir" in command:
            try:
                words = command.split()    #1 = dir_name
                functions.mkDir(current_directory, words[1])
            except IndexError:
                print("Provide proper arguments.")
                print("mkdir <dir_name>")
        elif "chdir" in command:
            try:
                words = command.split()    #1 = dir_name, 2 = mode
                words[1] = words[1].replace(',',"")    #removing comma
                if words[2] == "p":
                    current_directory = functions.chDir(home_directory, current_directory, mode="parent")
                elif words[2] == "c":   #child
                    current_directory = functions.chDir(current_directory,words[1], mode="child")
                elif words[2] == "f":   #full path
                    current_directory = functions.chDir(home_directory, new_directory=words[1], mode = "path")
            except IndexError:
                print("Provide proper arguments.")
                print("chdir <new_dir>, <mode>")
                print("mode can be 'p' for parent, 'c' for child, or empty for fullpath")
        elif "open" in command:
            try:
                words = command.split()    #1 = file_name, 2 = mode
                words[1] = words[1].replace(',',"")    #removing comma
                if words[2] == 'w':
                    words[2] = "write"
                elif words[2] == 'r':
                    words[2] = "read"
                current_file = functions.Open(current_directory, words[1], words[2], name)
            except IndexError:
                print("Provide proper arguments.")
                print("open <file_name.extension>, <mode>")
                print("mode can be 'w' for write, or 'r' for read")
        elif "close" in command:
            if (isinstance(current_file, classes.File)):
                current_file = functions.Close(current_file)
            else:
                print("No file currently opened")
        elif "create" in command:
            try:
                words = command.split()    #1 = file_name
                functions.create(current_directory, words[1])
            except IndexError:
                print("Provide proper arguments.")
                print("create <file_name.extension>")
        elif "delete" in command:
            try:
                words = command.split()    #1 = file_name
                functions.delete(current_directory, words[1])
            except:
                print("Provide proper arguments.")
                print("delete <file_name.extension>")
        elif "write" in command:
            try:
                words = command.split()    #1 = file_name, 2 = text
                words[1] = words[1].replace(',',"")    #removing comma
                if isinstance(current_file, classes.File):
                    current_file.writeToFile(text=words[2])
                else:
                    print("No file open")
            except IndexError:
                print("Provide proper arguments.")
                print("write <file_name.extension, <content>")
        elif "read" in command:
            try:
                words = command.split()    #1 = file_name
                print("\nContent: ")
                if isinstance(current_file, classes.File):
                    current_file.readFromFile()
                else:
                    print("No file open")
            except IndexError:
                print("Provide proper arguments.")
                print("read <file_name.extension>")
        elif "memory" in command:
            functions.printMemoryMap(home_directory)
        elif "print" in command:
            functions.printElements(current_directory)
        elif "save" in command:
            functions.saveInDat(home_directory)
        else:
            print("Invalid command")
        sys.stdout = sys.__stdout__     #redirect Output -> Failsafe incase threading fails before redirecting
        return current_directory, current_file

def handle_client(client_socket, addr):
    try:
        global interface
        global home_directory
        current_directory = home_directory
        current_file = ""
        client_socket.send(interface.encode('utf-8'))
        # Receive Name
        command = client_socket.recv(1024)
        name = command.decode('utf-8')
        print(f"\n{name} connected with ip {addr[0]}:{addr[1]}")
        while True:
            command = client_socket.recv(1024)
            # if no command was received, the connection was closed
            if command.decode('utf-8').lower() == 'disconnect':
                print(f"\nUsername: {name}, ip: {addr[0]}:{addr[1]} disconnected from server")
                break
            # print the received command
            print(f"\nReceived from {addr[0]}:{addr[1]}\nUsername: {name}\nCommand: {command.decode('utf-8')}")
            ##### FMS ######
            current_directory, current_file = exec_command(command.decode('utf-8'), current_directory, current_file, name)
            with open(f'temp{name}.txt', 'r') as file:
                response = file.read()
            os.remove(f"temp{name}.txt")
            ################
            # send a response back to the client
            client_socket.send(response.encode('utf-8'))

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