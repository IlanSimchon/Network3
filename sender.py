import socket
import os

ID1 = 6396
ID2 = 58


def check_got(xor):
    bool = xor == (ID1 ^ ID2)
    return bool

file_path = "myFile1.txt"
file = open(file_path, "r" )

file_len = os.path.getsize(file_path)
half_len = file_len // 2

receiver_ip = '127.0.0.1'
receiver_port = 9999

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buffer_size = sender_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

print("Connecting to receiver...")
sender_socket.connect((receiver_ip, receiver_port))

print("connection Succeeded!")

# read and split the file
file_read = file.read()

part1 = file_read[:half_len]
part2 = file_read[half_len:]

file.close()
print("Sending the len of the file")
sender_socket.send(str(file_len).encode())

send = True
while send is True:
    print("Sending the len of the file")
    sender_socket.send(str(file_len).encode())

    print("Defines the CC algorithm be Reno.")
    sender_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')


    print("Sending the first part of the file..")
    sender_socket.send(part1.encode())

    xor = float(sender_socket.recv(buffer_size).decode())
    if check_got(xor) is False:
        Exception
    else:
        print("Succeeded!")

    print("Defines the CC algorithm be Cubic")
    sender_socket.setsockopt(socket.IPPROTO_TCP , socket.TCP_CONGESTION , b'cubic')

    print("Sending the second part of thr file..")
    sender_socket.send(part2.encode())

    xor = float(sender_socket.recv(buffer_size).decode())
    if check_got(xor) is False:
        raise Exception
    else:
        print("Succeeded!")

    again = input("Should you send the file again? (y/n):")
    if again == "n":
        send = False
        sender_socket.send("Stop sending the file".encode())
        sender_socket.recv(buffer_size).decode()
    else:
        sender_socket.send("Sending the file again!".encode())

sender_socket.close()

