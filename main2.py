import socket
import threading
from urllib import parse

def default_http_port(): return 80


def server(port): #start server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostbyname(socket.gethostname())
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port)) # local host
    connection_count = 10 #maxium connection at once
    sock.listen(connection_count) 
    print('Listening at', sock.getsockname())
    return sock #return socket object for other functions

class App:
    __get_path_dict = dict()

    @staticmethod
    def GET(url: str,header,client):
        if url in App.__get_path_dict:
            client.send(App.__get_path_dict[url](header))
        else:
            p = url.rsplit("?",1)
            path = p[0]
            query = ""
            if len(p) == 2:
                query = p[1]
            if path in App.__get_path_dict:
                client.send(App.__get_path_dict[path](header,query))
            else:
                f = open("404.html", "rb")
                L = f.read()
                header = """HTTP/1.1 404 NOT FOUND    Content-Length: %d

                """ % len(L)
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


def index(header,query = ""):
    f = open("index.html")
    L = f.read()
    res = """HTTP/1.1 200 OK  
    Content-Type: text/html 
    Content-Length: %d\r\n\r\n""" % len(L)    
    res += L
    return res.encode()

def download(header,query = ""):  
    query_dict = parse.parse_qs(query)
    res = ""
    if "file" in query_dict:
        f = ()
        if len(query_dict["file"]) != 1:
            res = """HTTP/1.1 505 Internal Error
                Content-type: application/jpg
                Content-Disposition: attachment; filename="picture.jpg"
                Content-Length: 0\r\n\r\n""".encode()
            print("Internal Error")
        else:
            try:
                f = open(query_dict["file"][0],"rb")
                L = f.read()
                res = """HTTP/1.1 200 OK  
                Content-type: application/jpg
                Content-Disposition: attachment; filename="picture.jpg"
                Content-Length: %d\r\n\r\n""" % len(L) 
                k = len(res)   
                res = res.encode()
                res += L
                # Do something with the file
            except IOError:
                res = """HTTP/1.1 404 File not found
                Content-type: application/jpg
                Content-Disposition: attachment; filename="picture.jpg"
                Content-Length: 0\r\n\r\n""".encode()
                print("File not found")
    else:
         res = """HTTP/1.1 400 Bad request  
            Content-Length: 0\r\n\r\n""".encode()
        
        
    
    return res

App.add_GET("/",index)        
App.add_GET("/download",download)        

if __name__ == "__main__":
    sock = server(default_http_port())
    Wait_for_connection(sock)