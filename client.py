import socket

def interface():
    return

def name(client_socket):
    data = input("Enter Name: ")
    client_socket.send(data.encode('utf-8'))

def connect():
    #server_ip = input("Enter the server's IP address: ")
    server_ip = "192.168.101.159"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 95))
    name(client_socket) # Sending name to server
    return client_socket
    
if __name__ == '__main__':  
    client_socket = connect()
    while True:
        interface()
        data = input("Enter command: ")
        if data.lower() == "disconnect":
            break
        else:
            client_socket.send(data.encode('utf-8'))
            response = client_socket.recv(1024)
            print(response.decode("utf-8"))
        print("")

    client_socket.close()