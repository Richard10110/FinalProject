import threading
import functions_oop
import socket
import pickle
import json

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("10.0.0.22",2020))
server.listen()

def server_handle():
    client,addr = server.accept()
    # needs to find a way to save all clients and access
    # them easily in code.
    th1 = threading.Thread(target=server_response,args=(client,)).start()


def server_response(cli):
    central_point = functions_oop.mongo()
    while True:
        action = cli.recv(1024).decode()
        if action == "upload":
            meta_data = cli.recv(1024)
            metadata = meta_data

            cli.send("metadata".encode())
            file_size = json.loads(pickle.loads(meta_data))['size']

            file_data = cli.recv(file_size)
            cli.send("Success".encode())
            central_point.upload_file(metadata,file_data)


        elif action == "del":
            file_name = cli.recv(1024).decode()
            central_point.del_file(file_name)
            cli.send("Success".encode())


        elif action == "download":
            file_name = cli.recv(1024).decode()
            file_binary, size = central_point.download_file(file_name)
            print(size)
            print(file_binary)
            # cli.send(size.encode())
            # cli.send(file_binary.read())
            # flag = cli.recv(1024).decode()
            # if flag =="Success" :
            #     cli.send("Success".encode())







if __name__ == '__main__':
    server_handle()
