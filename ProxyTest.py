import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 2000))
print "connect successfully"

nTotal = 2
nCurrent = 0;

print sock.recv(1024)

while (True):
    if (nCurrent > nTotal):
        break
    data = "ccc "
    sock.send(data);

    nCurrent += 1

print sock.recv(1024)
sock.close()