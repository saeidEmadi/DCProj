import threading
import configparser
import argparse
import ipaddress
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
        global _debug
        self.serverIP = serverIP
        self.portNumber = portNumber
        _debug = DEBUG
        
        if _debug :
            print("\n++[Server object]++\n")
            print(f"[server IP : {self.__serverIP}]")
            print(f"[Port Number : {self.__portNumber}]")
    
    def netConfig(self, serverIP : str, portNumber : int):
        """ config ip and port """
        self.serverIP = serverIP
        self.portNumber = portNumber
        
        if _debug :
            print("\n++[new net Config]++\n")
            print(f"[new server IP : {self.__serverIP}]")
            print(f"[new Port Number : {self.__portNumber}]\n")
    
    def stream(self):
        """ receive video from camera """
        pass
    
    def run(self):
        """ run server """
        pass
    
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
    print("\n[Server Running : CLI Mode]\n")
    
    # argument parser
    argparser = argparse.ArgumentParser(description = "Server runner Script | run script for receive Camera Packets")
    argparser.add_argument('host', metavar = 'host', type = str, nargs = 1, help = "Server Address for listening clients")
    argparser.add_argument('port', metavar = 'port', type = int, nargs = 1, help = "port number")
    argparser.add_argument('--test', action = "store_true", help = "flag for Enable defaults parameters run :: \n "+config['Server']['server IP']+" "+config['Server']['port'])
    argparser.add_argument('--stream', action = "store_true", help = "stream traffic camera real-Time")
    argparser.add_argument('--debug', action = "store_true", help = "flag for Enable Debug mode [show CLI logs]")
    args = argparser.parse_args()
    