import socket
import threading
def default_http_port(): return 80


def server(port): #start server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', port)) # local host
    connection_count = 10 #maxium connection at once
    sock.listen(connection_count) 
    print('Listening at', sock.getsockname())
    return sock #return socket object for other functions

def request_handler(req):
    # Handle request nhu binh thuong
    pass


def Wait_for_connection(sock):
    while(True):
        req = sock.recv(4096) # 4096KB
        threading.Thread(target=request_handler,args=(req,)).start()
        

if __name__ == "__main__":
    sock = server(default_http_port())
    Wait_for_connection(sock)