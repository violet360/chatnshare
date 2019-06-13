import sys, socket, select, os






def d_file(s, filename):

    if filename != 'q':

        s.send(bytes(filename,'utf-8'))

        data = s.recv(1024).decode('utf-8')

        if data[:6]=="exists":

            filesize = int(data[6:])

            message = input("file exists, "+str(filesize)+"Bytes, download? (Y/N) -> ")

            if message == 'Y':

                s.send(bytes('OK', 'utf-8'))

                var =filename.split('.')

                var1 = var[1][var[1].find('(')+1:]

                var2 = var[2][:var[2].find(')')]


                print(var1, var2)

                filename1 = var1+'1.'+var2

                f = open(filename1, 'wb')

                while True:

                    data = s.recv(1024)

                    f.write(data)

                    if sys.getsizeof(data)<1024:

                        break

                   

                print("download complete")


        else:

            print("file does not exist!")
 
def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
     
    try :
        s.connect((socket.gethostname(), 1234))
    except :
        print ('oops something went wrong')
        sys.exit()
     
    print ('Connected........ready to go...')
    username = input("Your name>> ")
    sys.stdout.write('<%s> ' %username); sys.stdout.flush()
    s.send(username.encode()) 
    
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        
        read_sockets,write_sockets,error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = (sock.recv(4096))
                data = data.decode()
                if not data :
                    print(f'connection has been lost :(')
                    sys.exit()
                else :
                    #print (data)
                    sys.stdout.write(data)
                    sys.stdout.write('<%s> ' %username)
                    sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline().encode()
                # if msg.decode('utf-8').split('.')[0]=='event' and 'get' in msg.decode('utf-8').split('.')[1]:
                #     var = msg.decode('utf-8').split('.')
                #     if var[1] == 'get':
                #         s.send(msg)
                    #check server

                if msg.decode('utf-8').find('(')!=-1 and msg.decode('utf-8').find(')')!=-1:
                    x = msg.decode('utf-8')
                    d_file(s, x)

                s.send(msg)
                sys.stdout.write('<%s> ' %username)
                sys.stdout.flush() 

if __name__ == "__main__":
    main()

