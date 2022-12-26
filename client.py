import socket

def name(client_socket):
    data = input("Enter Name: ")
    client_socket.send(data.encode('utf-8'))
    client_socket.recv(1024)

def connect():
    #server_ip = input("Enter the server's IP address: ")
    server_ip = "10.7.81.121"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 95))
    name(client_socket) # Sending name to server
    return client_socket
    
if __name__ == '__main__':  
    client_socket = connect()
    while True:
        data = input("Enter command: ")
        if data.lower() == "disconnect":
            break
        else:
            client_socket.send(data.encode('utf-8'))
            response = client_socket.recv(1024)
            print(response.decode("utf-8"))

    client_socket.close()