import socket

if __name__ == '__main__':
    #server_ip = input("Enter the server's IP address: ")
    server_ip = "10.7.81.121"
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 95))

    while True:
        # send data to the server
        data = input("Enter command: ")
        client_socket.send(data.encode('utf-8'))

        # receive data from the server
        response = client_socket.recv(1024)

        print(response.decode("utf-8"))

    # close the client socket
    client_socket.close()