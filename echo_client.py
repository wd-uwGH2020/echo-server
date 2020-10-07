import socket
import sys
import traceback

def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    sock_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    sock_c.connect(server_address)

    received_message = ''

    try:
        sock_c.sendall(msg.encode('utf-8'))
        print('sending "{0}"'.format(msg), file=log_buffer)
        received_message += msg
        while True:
            my_message = input("> ")
            if len(my_message) == 0:
                break
            sock_c.sendall(my_message.encode('utf-8'))

            chunk = sock_c.recv(16)
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            received_message += chunk.decode('utf8')
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        sock_c.close()
        print('closing socket', file=log_buffer)

        return received_message

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
