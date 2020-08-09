import pickle
import socket
import time


class Network:

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None
        self.port = None

        self.made_connection = None
        self.ping = 0

    def find_servers(self):

        with open("servers.txt") as f:
            content = [self.find_ip(x.rstrip()) for x in f.readlines()]
        return content

    def find_ip(self, ip):
        '''
        Takes a string, and returns (if found)
        the ip and port
        '''

        if ":" not in ip:
            return None
        else:
            server, port = ip.split(":")
            return (server, int(port))

    def connect(self):
        '''
        Makes the initial connection to the
        host/server
        '''

        for addr in self.find_servers():
            try:
                self.addr = addr
                self.server, self.port = addr
                self.client.connect(self.addr)
                time.sleep(0.00001)
                self.made_connection = True
                return pickle.loads(self.client.recv(2048*4))
            except:
                pass
        self.addr = None
        self.server = None
        self.port = None
        self.made_connection = False
        print("could not make connection")
    
    def request(self, data):

        packet = {"action" : "request", "data" : data}
        try:
            self.client.send(pickle.dumps(packet))
            r_data = pickle.loads(self.client.recv(2048*4))
                
            return r_data
        except socket.error as e:
            print(e)
            return None
    
    def push(self, data):

        packet = {"action" : "push", "data" : data}
        try:
            self.client.send(pickle.dumps(packet))
            # Set to receive low # of bits as its not excepting
            # to receive any important data
            r_data = pickle.loads(self.client.recv(2048*2))
                
            return r_data
        except socket.error as e:
            print(e)
            return None

    def send(self, data):
        '''
        Sends and immediately receives data with the host/server.
        Data is sent as bytes through object serialization
        '''

        try:
            self.client.send(pickle.dumps(data))
            r_data = pickle.loads(self.client.recv(2048*4))
                
            return r_data
        except socket.error as e:
            print(e)
