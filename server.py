import sys, socket, select, os

the_list = []

def broadcast_packets(server_socket, sock, message):
    for socket in the_list:
        
        if socket != server_socket and socket != sock :
            try :
                socket.send(message.encode())
            except :
               
                socket.close()
                
                if socket in the_list:
                    the_list.remove(socket)




def send_stuff(clientsocket, f_name):

    print(f_name)

    print(os.path.isfile(f_name))

    if os.path.isfile(f_name):

        clientsocket.send(bytes("exists"+str(os.path.getsize(f_name)),'utf-8'))

        u_res = clientsocket.recv(1024).decode('utf-8')

        if u_res[:2] == 'OK':

            with open(f_name, 'rb') as f:

                while True:

                    bytestosend = f.read(1024)

                    clientsocket.send(bytestosend)

                    if sys.getsizeof(bytestosend) < 1024:

                        break


    else:

        clientsocket.send(bytes("err",'utf-8'))





def main():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((socket.gethostname(), 1234))
    server_socket.listen(10)
    the_list.append(server_socket)
    user = dict()
 
    print (f"port {str(1234)} has been setup.....")
 
    while 1:


        try:
            read_sockets,write_sockets,error_sockets = select.select(the_list,[],[],0)
        except:
            sys.exit("\n")

        for sock in read_sockets:

            if sock == server_socket: 
                sock0, addr = server_socket.accept()
                the_list.append(sock0)

                print (f"{addr} has joined")
                 
                broadcast_packets(server_socket, sock0, f"{addr} has joined us")
             

            else:
 
                try:

                    data = sock.recv(1024).decode()
                    print(data)


                    if(sock.getpeername() not in user):
                        user[sock.getpeername()] = data
                        continue

                    if data:

                        if "(" in data and ")" in data and "event" in data and "get" in data and '.' in data:

                            x = data[data.find('(')+1:data.find(')')]
                            send_stuff(sock, x)



                            
                                
                        broadcast_packets(server_socket, sock, "\r" + '<' + user[sock.getpeername()] + '> '+ data) 
                    else:
   
                        if sock in the_list:
                            the_list.remove(sock)


                        broadcast_packets(server_socket, sock, "[*] %s is now offline\n" % user[sock.getpeername()]) 

                except:
                    broadcast_packets(server_socket, sock, "[*] %s is now offline\n" % user[sock.getpeername()])
                    continue

    server_socket.close()
    


 
if __name__ == "__main__":
    main()


         
