import threading
import socket

def get_machine_ip():
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(("8.8.8.8", 80)) #Connecting to Google DNS to get IP
    return ip.getsockname()[0]

def handle_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024)
            # if no data was received, the connection was closed
            if not data:
                break
            # print the received data
            print(f"Received data from {addr[0]}:{addr[1]}: {data.decode('utf-8')}")
            # send a response back to the client
            client_socket.send(b"Thank you for sending data!")

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