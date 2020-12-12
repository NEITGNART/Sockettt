import socket
import io
import json
from email.parser import BytesParser


def server(port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port)) # local host
    sock.listen(1)
    print('Listening at', sock.getsockname())

    while True:
        print('Waiting for a new connection')
        sc, sockname = sock.accept()
        re = sc.recv(4096).decode()
        if command in re:
            sock.close()
            return sc, re


def gogoIndex(x, port):
    f = open("index.html", "rb")
    L = f.read()
    header = """HTTP/1.1.200 OK    Content-Length: %d

""" % len(L)
    print(header)
    header += L.decode()
    x.send(bytes(header, "utf-8"))
    x.close()



def gogoInfo(y, checkPass):


    if "Username=admin&Password=admin" in checkPass :


        headernew = """HTTP/1.1 301 Moved Permanently
Location: http://localhost:15001/info.html

"""

        print("Headernew", headernew)
        y.send(bytes(headernew, "utf-8"))


        m, n = server(portnew, "GET /info.html HTTP/1.1")
        f = open("info.html", "rb")
        l = f.read()
        header = """HTTP/1.1.200 OK    Content-Length: %d

    """ % len(l)
        header += l.decode()
        m.send(bytes(header, "utf-8"))



    else:

        headernew = """HTTP/1.1 301 Moved Permanently
Location: http://localhost:15001/404.html

"""
        y.send(bytes(headernew, "utf-8"))

        m, n = server(portnew, "GET /404.html HTTP/1.1")
        f = open("404.html", "rb")
        l = f.read()
        header = """HTTP/1.1 404 Not Found    Content-Length: %d

    """ % len(l)
        header += l.decode()
        m.send(bytes(header, "utf-8"))



def gogoFile(x):
    f = open("file.html", "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK 
    Content-Type: text/plain
    Transfer-Encoding: chunked 

"""
    print(header)
    header += L.decode()
    x.send(bytes(header, "utf-8"))
    x.close()



if __name__ == "__main__":
    command = "GET / HTTP/1.1"
    port = 15000

    x, z = server(port, command) # x is client and z is response from x
    gogoIndex(x, port)


    portnew = 15001

    commandInfo = "POST / HTTP/1.1"
    y, t = server(portnew, commandInfo) # y is client and t is response from y
    gogoInfo(y, t)
    y.close()
    portneww = 15002
    commandFile = "GET / HTTP/1.1"

    epsilon, theta = server(portneww, commandFile)
    gogoFile(epsilon)

