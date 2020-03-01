#-*-coding:utf8;-*-
#qpy:console

print "This is console module"
import os
import sys
import random
import socket
import select
import datetime
import threading

lock = threading.RLock(); os.system('cls' if os.name == 'nt' else 'clear')

def real_path(file_name):
    return os.path.dirname(os.path.abspath(__file__)) + file_name

def filter_array(array):
    for i in range(len(array)):
        array[i] = array[i].strip()
        if array[i].startswith('#'):
            array[i] = ''

    return [x for x in array if x]

def colors(value):
    patterns = {
        'R1' : '\033[31;1m', 'R2' : '\033[31;2m',
        'G1' : '\033[32;1m', 'Y1' : '\033[33;1m',
        'P1' : '\033[35;1m', 'CC' : '\033[0m'
    }

    for code in patterns:
        value = value.replace('[{}]'.format(code), patterns[code])

    return value

def log(value, status='P & P :' , color='[P1]'):
    value = colors('{color}''[P1]''[{time}] [G1]{color}{status} [R1]{color}{value}[Y1]'.format(
        time=datetime.datetime.now().strftime('[G1]Jaka [R1]Benang'),
        value=value,
        color=color,
        status=status
    ))
    with lock: print(value)

def log_replace(value, status='WARNING', color='[P1]'):
    value = colors('{}{} ({})        [CC]\r'.format(color, status, value))
    with lock:
        sys.stdout.write(value)
        sys.stdout.flush()

class inject(object):
    def __init__(self, inject_host, inject_port):
        super(inject, self).__init__()

        self.inject_host = str(inject_host)
        self.inject_port = int(inject_port)

    def log(self, value, color='[G1]'):
        log(value, color=color)

    def start(self):
        try:
            socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket_server.bind((self.inject_host, self.inject_port))
            socket_server.listen(1)
            frontend_domains = open(real_path('/config.ini')).readlines()
            frontend_domains = filter_array(frontend_domains)
            if len(frontend_domains) == 0:
                self.log('Frontend Domains not found. Please check config.ini', color='[Y1]')
                return
            self.log('{} Port {}'.format(self.inject_host, self.inject_port))
            while True:
                socket_client, _ = socket_server.accept()
                socket_client.recv(65535)
                domain_fronting(socket_client, frontend_domains).start()
        except Exception as exception:
            self.log('{} Port {}'.format(self.inject_host, self.inject_port), color='[P1]')

class domain_fronting(threading.Thread):
    def __init__(self, socket_client, frontend_domains):
        super(domain_fronting, self).__init__()

        self.frontend_domains = frontend_domains
        self.socket_tunnel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client = socket_client
        self.buffer_size = 65535
        self.daemon = True

    def log(self, value, status='*', color='[P1]'):
        log(value, status=status, color=color)
        
    def handler(self, socket_tunnel, socket_client, buffer_size):
        sockets = [socket_tunnel, socket_client]
        timeout = 0
        while True:
            timeout += 1
            socket_io, _, errors = select.select(sockets, [], sockets, 3)
            if errors: break
            if socket_io:
                for sock in socket_io:
                    try:
                        data = sock.recv(buffer_size)
                        if not data: break
                        # SENT -> RECEIVED
                        elif sock is socket_client:
                            socket_tunnel.sendall(data)
                        elif sock is socket_tunnel:
                            socket_client.sendall(data)
                        timeout = 0
                    except: break
            if timeout == 10: break

    def run(self):
        try:
            self.proxy_host_port = random.choice(self.frontend_domains).split(':')
            self.proxy_host = self.proxy_host_port[0]
            self.proxy_port = self.proxy_host_port[1] if len(self.proxy_host_port) >= 2 and self.proxy_host_port[1] else '443'
            self.log('[R1]B I S [G1]M I L L A H '.format(self.proxy_host, self.proxy_port))
            self.socket_tunnel.connect((str(self.proxy_host), int(self.proxy_port)))
            self.socket_client.sendall(b'HTTP/1.1 200 OK\r\n\r\n')
            self.handler(self.socket_tunnel, self.socket_client, self.buffer_size)
            self.socket_client.close()
            self.socket_tunnel.close()
            self.log('[G1]AL[R1]HAM[Y1]DUL[G1]ILL[Y1]AH  [P1]==> [G1]YA ALLAH','[R1]'.format(self.proxy_host, self.proxy_port), color='[G1]')
        except OSError:
            self.log('Connection Error', color='[G1]')
        except TimeoutError:
            self.log('{} Not Responding'.format(self.proxy_host), color='[R1]')

def main():
    print(colors('\n'.join([
    	      '         '
      '[G1]Nama       : [P1]MUHAMMAD AMIN','[R1]'
      '         '
          'Script     : TELKOMSEL OPOK 2020','[R1]'
                '         '
      '[G1]Limit      : 500 MB ','[Y1]'
            '         '
      '[P1]Facebook   : JAKA BENANG ','[Y1]'
          

          
          ])))
          
    inject('127.0.0.1', '8080 ').start()

if __name__ == '__main__':
    main()
#By Muhammad Amin
