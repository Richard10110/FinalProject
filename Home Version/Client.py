import socket



Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Client.connect(('127.0.0.1', 8080))



def upload():
    file_name = input("Enter file name: ")
    Client.send(file_name.encode())

def delete():
    file_name = input("Enter file name: ")
    Client.send(file_name.encode())

def download():
    file_name = input("Enter file name: ")
    Client.send(file_name.encode())




if __name__ == '__main__':

    while True:
        action = input("what is your action? ")
        Client.send(action.encode())
        match action:
            case "upload":
                upload()
            case "delete":
                delete()
            case "download":
                download()
            case "exit":
                Client.close()
                break

