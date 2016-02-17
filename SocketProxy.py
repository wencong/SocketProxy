#from gevent import socket, spawn, joinall, sleep
import asyncore
import socket

server_host = "192.168.31.143"
server_port = 2000

class Handler(asyncore.dispatcher):
    def __init__(self, sock, handler_name):
        asyncore.dispatcher.__init__(self, sock);
        self.buffers = []
        self.handler = None
        self.handler_name = handler_name
        pass

    def handle_connect(self):
        pass
 
    def handle_close(self):
        self.close()
       
    def handle_read(self):
        recv_data = self.recv(8192)
        if (self.handler == None):
            print "Handler is None";
        else:
            print "recv data from " + self.handler_name + " length: " + str(len(recv_data))
            self.handler.buffers.append(recv_data)
 
    def writable(self):
        return (len(self.buffers) > 0)
   
    def handle_write(self):
    	for i in range(len(self.buffers)):
            buff = self.buffers[i];
            print "send data to " + self.handler_name + " lenght: " + str(len(buff))
            self.send(buff)
        self.buffers = []


class Proxy(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.set_reuse_addr()  
        self.bind((host, port))  
        self.listen(5)
        print "proxy listening " + str(host) + " " + str(port);

    def handle_accept(self):  
        pair = self.accept()  
        if pair is None:  
            pass  
        else:  
            sock, addr = pair  
            print 'Incoming connection from %s' % repr(addr)  
            #handler = EchoHandler(sock)  
            c_handler = Handler(sock, "client");

            s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_sock.connect((server_host, server_port));
            s_handler = Handler(s_sock, "server");

            c_handler.handler = s_handler;
            s_handler.handler = c_handler;


if __name__ in ("main", "__main__"):
    #p1 = spawn(Proxy, "10.20.110.39", 9208, HandleToServerData, HandleToClientData)
    proxy = Proxy("", 2000);
    asyncore.loop();


