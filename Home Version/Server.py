import threading
import socket



Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(('127.0.0.1', 8080))
Server.listen()





def get_clients():
    while True:
        Client, Address = Server.accept()
        th1 = threading.Thread(target=handle_clients, args=(Client,)).start()



def upload():
    pass

def delete():
    pass

def download():
    pass


def handle_clients(client):
    while True:
        action = client.recv(1024).decode()

        match action:
            case "upload":
                upload()
            case "delete":
                delete()
            case "download":
                download()
            case "exit":
                client.close()
                break





if __name__ == '__main__':
    pass