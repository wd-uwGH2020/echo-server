import socket
import sys
import traceback

def server(log_buffer=sys.stderr):
    address = ('127.0.0.1', 10000)
    sock_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    sock_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    sock_s.bind(address)
    sock_s.listen(1)


    try:
        while True:
            print('waiting for a connection', file=log_buffer)

            try: 
                conn, addr = sock_s.accept()
            
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                while True:
                    data = conn.recv(16)
                    print('received "{0}"'.format(data.decode('utf8')))
                    
                    conn.sendall(data.decode('utf8').encode('utf8'))
                    print('sent "{0}"'.format(data.decode('utf8')))

                    if len(data) < 16:
                        print('reached the end of the messages from client')
                        break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                conn.close()
                # sock_s.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        conn.close()
        # sock_s.close()
        print('quitting echo server', file=log_buffer)

if __name__ == '__main__':
    server()
    sys.exit(0)
