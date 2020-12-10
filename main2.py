import socket
import threading
from email.parser import BytesParser

def default_http_port(): return 80


def server(port): #start server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port)) # local host
    connection_count = 10 #maxium connection at once
    sock.listen(connection_count) 
    print('Listening at', sock.getsockname())
    return sock #return socket object for other functions

class App:
    __get_path_dict = dict()

    @staticmethod
    def GET(path: str,header,client):
        if path in App.__get_path_dict:
            client.send(App.__get_path_dict[path](header).encode())
        else:
            f = open("404.html", "rb")
            L = f.read()
            header = """HTTP/1.1 404 NOT FOUND    Content-Length: %d

        """ % len(L)
            print(header)
            header += L.decode()
            client.send(bytes(header, "utf-8"))

    @staticmethod
    def add_GET(path:str,function: callable):
        App.__get_path_dict[path] = function


def request_handler(client):
    # Handle request nhu binh thuong    
    data = b''
    while b'\r\n\r\n' not in data:
        data += client.recv(1)
    k, headers = data.split(b"\r\n",1)
    k = k.decode().split(' ')
    start_line = {"method":k[0],"path":k[1],"proto":k[2]}
    if start_line["method"] == "GET":
        App.GET(start_line["path"],headers.decode(),client)
    client.close()


def Wait_for_connection(sock):
    while(True):
        client, adrr = sock.accept()
        threading.Thread(target=request_handler,args=(client,)).start()


def index(header):
    f = open("index.html")
    L = f.read()
    res = """HTTP/1.1 200 OK    Content-Length: %d

    """ % len(L)    
    print(header)
    res += L
    return res

App.add_GET("/",index)        

if __name__ == "__main__":
    sock = server(default_http_port())
    Wait_for_connection(sock)