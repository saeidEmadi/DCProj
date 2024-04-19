import threading
import configparser
import argparse
import ipaddress
import socket
from typing import Final

# config parser
# read config file and initial config variables
config = configparser.ConfigParser()
config.read('config.ini')
try : 
    config.read('config.ini')
except :
    raise FileExistsError("config.ini file is not exists.")

class Server(threading.Thread):
    """ Server Class use for receive report and data from cameras """        
    
    # default value for listen socket backLog    
    backlogListenVal : Final[int] = config['Server']["backlogListenVal"]
    
    def __init__(self, serverIP : str = config['Server']['server IP'], \
            portNumber : int = int(config['Server']['port']), \
            DEBUG : bool = False):
        """ initial class variables """
        global _debug , _stream
        self.serverIP = serverIP
        self.portNumber = portNumber
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__clientPool = []
        _debug = DEBUG
        
        if _debug :
            print("\n++[Server object]++\n")
            print(f"[server IP : {self.__serverIP}]")
            print(f"[Port Number : {self.__portNumber}]")
            
    def __startConnection(self):
        """ start connection socket """
        try:
            self.__socket.bind((self.__serverIP, self.__portNumber))
            self.__socket.listen(int(self.backlogListenVal))
        except : 
            raise ConnectionError(f"can't bind server listener, {self.__serverIP}:{self.__portNumber}")
        
        if _debug :
            print(f"\n**[connection started]**\n")
            print("socket binded to %s" %(self.__portNumber)) 
            print("socket is listening ....")
            
    def __closeConnection(self):
        """ socket close connection """
        self.__socket.close()
        
        if _debug :
            print(f"\n**[connection closed]**\n")
    
    def __shutDownConnection(self):
        """ socket shutdown mode (only receive) """
        self.__socket.shutdown()
        
        if _debug :
            print(f"\n**[connection shutdown]**\n")
    
    def stream(self, client):
        """ receive video from camera """
        pass
    
    def receiveReport(self, client):
        while True :
            msg = client.recv(1024).decode()
            if len(msg) > 0 :
                print(f"[ Camera :{threading.currentThread().name} {msg}]")
            else :
                print(f"[ Camera :{threading.currentThread().name} connection dead]")
                break
            
    def __getNewClient(self):
        """ Threading Function """
        """ receive and accept new clients """
        while True :
            client, address = self.__socket.accept()
            cameraName = client.recv(1024).decode()
            print(f'//// camera name : {cameraName} ////')
            print(f"[@@] Got connection from ",address)
            thReport = threading.Thread(target = self.receiveReport, args = (client,), name = cameraName)
            self.__clientPool.append((client, address),thReport)
            thReport.start()
    
    def run(self):
        """ run server """
        self.__startConnection()
        self.__getNewClient()
        # check Threads
        while True :
            (client, _), thread = self.__clientPool[0]
            if not thread.is_alive() :
                print(f"{thread.getName()} is disconnect")
                self.__clientPool[:] = self.__clientPool[1:]
                
        #self.__shutDownConnection()
        #self.__closeConnection()
    
    @property
    def serverIP(self):
        """ return server IP """
        return self.__serverIP
    
    @serverIP.setter
    def serverIP(self, serverIP : str):
        """ set server IP """
        try:
            ipaddress.ip_address(serverIP)
            self.__serverIP = serverIP
        except:
            raise ValueError("ip Address invalid, valid Types : [IPv4,IPv6]")
    
    @property
    def portNumber(self):
        """ return server Port Number """
        return self.__portNumber
    
    @portNumber.setter
    def portNumber(self, portNumber : int):
        """ set server Port Number """
        
        if not isinstance(portNumber, int):
            raise ValueError("port number only integer valid")
        
        if not 1 <= portNumber <= 65535 :
            raise ValueError("port number invalid")
        
        self.__portNumber = portNumber
        
if __name__ == "__main__":
    """ this class, you can use this \
        with import and create object \
        or CLI run Server"""
    print("[Server Running : CLI Mode]\n")
    
    # argument parser
    argparser = argparse.ArgumentParser(description = "Server runner Script | run script for receive Camera Packets")
    argparser.add_argument('host', metavar = 'host', type = str, nargs = 1, help = "Server Address for listening clients")
    argparser.add_argument('port', metavar = 'port', type = int, nargs = 1, help = "port number")
    argparser.add_argument('--test', action = "store_true", help = "flag for Enable defaults parameters run :: \n "+config['Server']['server IP']+" "+config['Server']['port'])
    argparser.add_argument('--debug', action = "store_true", help = "flag for Enable Debug mode [show CLI logs]")
    args = argparser.parse_args()
    
    if args.test : 
        server = Server(DEBUG = True)
    else :
        if args.debug :
            server = Server(str(args.host[0]),int(args.port[0]),True)
        else :
            server = Server(str(args.host[0]),int(args.port[0]))
    server.run()        