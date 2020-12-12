import socket


def gogoImage(x, filename):
        with open(filename, 'rb') as f:
            L = f.read()
            header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)

        print(header)
        header = bytes(header, 'utf-8') + L
        x.send(header)
        x.close()



def serverUniqueForImage(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port)) # local host
    sock.listen(2)
    print('Listening at', sock.getsockname())
    commandPhamTien = "GET /PhamTien.jpg HTTP/1.1"
    visitedPhamTien = 0
    commandVinhSon = "GET /VinhSon.jpg HTTP/1.1"
    visitedVinhSon = 0
    while True:
        sc, sockname = sock.accept()
        re = sc.recv(4096).decode()
        print(re)
        if (commandPhamTien in re) and (visitedPhamTien == 0):
            gogoImage(sc, "PhamTien.jpg")
            visitedPhamTien = 1

        elif (commandVinhSon in re) and (visitedVinhSon == 0):
            gogoImage(sc, "VinhSon.jpg")
            sock.close()
            return sc, re




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
        print(re)
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
Location: http://localhost:20001/info.html

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

        serverUniqueForImage(20001)

    else:

        headernew = """HTTP/1.1 301 Moved Permanently
Location: http://localhost:20001/404.html

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
    header = """HTTP/1.1.200 OK

"""
    print(header)
    header += L.decode()
    x.send(bytes(header, "utf-8"))
    x.close()



def serverUniqueforDownload(port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port)) # local host
    sock.listen(1)
    print('Listening at', sock.getsockname())

    while True:
        print('Waiting for a new connection')
        sc, sockname = sock.accept()
        re = sc.recv(4096).decode()
        print(re)
        if ("GET /2020-12-12%2011-10-49.mkv HTTP/1.1"):
            gogoImage(sc, "2020-12-12 11-10-49.mkv")






if __name__ == "__main__":
    command = "GET / HTTP/1.1"
    port = 20000

    x, z = server(port, command) # x is client and z is respone from x
    gogoIndex(x, port)


    portnew = 20001

    commandInfo = "POST / HTTP/1.1"
    y, t = server(portnew, commandInfo) # y is client and t is respone from y
    gogoInfo(y, t)
    y.close()

    portneww = 20002
    commandFile = "GET /file.html HTTP/1.1"

    epsilon, theta = server(portneww, commandFile)
    gogoFile(epsilon)

    serverUniqueforDownload(20002)
    

    
        
        
