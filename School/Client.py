import socket
import functions_oop

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("10.0.0.22",2020))


def file_info():
    while True:
        action = input('What is your action? : ')
        client.send(action.encode())
        if action == 'upload':
            fn = input("file name: ")

            file_breaker = functions_oop.file_information(fn)
            finalized_data = file_breaker.get_pickled()

            client.send(finalized_data)

            success_meta_flag = client.recv(1024).decode()
            if success_meta_flag == "metadata":

                print("MetaData recieved successfully")

                client.send(file_breaker.file_content())

                success_file_flag = client.recv(1024).decode()
                if success_file_flag == "Success":
                    print("File was sent successfully")
                else:
                    print("File fail")
            else:
                print("Meta fail")


        elif action == 'del':
            fn = input("file name: ")
            client.send(fn.encode())
            msg = client.recv(1024).decode()
            if msg == "Success":
                print(f"{fn} was deleted Successfully")
            else:
                print("file's name is invalid/doesn't exist")


        elif action == "download":
            fn = input("file name: ")
            client.send(fn.encode())
            size = client.recv(1024).decode()
            size = int(size) # casting it string --> integer
            file_content = client.recv(size)
            with open(f"downloaded_{fn}","wb") as w_file:
                w_file.write(file_content)
            client.send("Success".encode())
            flag = client.recv(1024).decode()
            if flag == "Success":
                print(f"Downloaded successfully {fn}")



if __name__ == '__main__':
    file_info()