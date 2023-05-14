import socket
import time
from statistics import mean

ID1 = 6396
ID2 = 58

file_path = "receiver_file.txt"
file = open(file_path , 'wb')

part1_time = []
part2_time = []

receiver_ip = '127.0.0.1'
receiver_port = 9999

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
buffer_size = receiver_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)

print("Creating a connection...")
receiver_socket.bind((receiver_ip,receiver_port))

receiver_socket.listen(1)
print("listening on IP:",receiver_ip," Port:",receiver_port)

sender_socket, sender_address = receiver_socket.accept()
print("connection Succeeded!\n")

file_len = int(sender_socket.recv(buffer_size))

while file_len != -1:
    print("Defines the CC algorithm be reno.")
    receiver_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'reno')

    start_time = time.time()

    data_size1 = 0
    print("receives the first part of the file")
    while data_size1 < file_len // 2:
        chunk = sender_socket.recv(buffer_size)
        data_size1 += len(chunk.decode())
        file.write(chunk)

    first_part_time = time.time() - start_time
    part1_time.append(first_part_time)

    print("Sending OK to the sender\n")
    sender_socket.send((str(ID1 ^ ID2)).encode())

    print("Defines the CC algorithm be Cubic..")
    receiver_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

    start_time = time.time()
    print("receives the second part of the file")
    data_size2 = 0
    while data_size2 < file_len - data_size1:
        chunk = sender_socket.recv(buffer_size)
        data_size2 += len(chunk)
        file.write(chunk)

    second_part_time = time.time() - start_time
    part2_time.append(second_part_time)

    print("Sending OK to the sender\n")
    sender_socket.send((str(ID1 ^ ID2)).encode())

    decision = sender_socket.recv(buffer_size).decode()
    print(decision,'\n')
    if decision == "Stop sending the file":
        file_len = -1
        sender_socket.send("Thank you, goodbye!".encode())

for i in range(1, len(part1_time)+1):
    print("Time of receiving number " , i , ":")
    print("part 1: " , part1_time[i-1] , " seconds")
    print("part 2: " , part2_time[i-1] , " seconds\n")

print("Average of part 1:", mean(part1_time), "seconds")
print("Average of part 2:", mean(part2_time), "seconds")
print("Total Average: ", mean(part1_time+part2_time), "seconds\n")


print("Close the connection..")
receiver_socket.close()
file.close()