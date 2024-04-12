import ipaddress
import socket
import configparser
import threading
#from ultralytics import YOLO
import re
class Camera(threading.Thread):
    """ Camera Class : \
        track objects and detect Traffic """
        
    # read config file and initial config variables
    config = configparser.ConfigParser()
    try : 
        config.read('config.ini')
    except :
        raise FileExistsError("config.ini file is not exists.")
    
    def __init__(self, serverIP : str = config['Server Address']['server'], \
        portNumber : int = int(config['Server Address']['port']), \
        yoloVersion : str = 'yolov9e.pt', DEBUG : bool = False):
        
        """ initial Thread initials """
        threading.Thread.__init__(self)
        """ initial variables """
        
        # define global _debug for validate Debug mode
        global _debug
        self.serverIP = serverIP
        self.portNumber = portNumber
        self.bondedBox = False
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.yoloVersion = yoloVersion
        _debug = DEBUG
        self
        
        if _debug :
            print("\n++[new Camera object]++\n")
            print(f"[server IP : {self.__serverIP}]")
            print(f"[Port Number : {self.__portNumber}]")
            print(f"[Bonded Box : {self.__bondedBox}]")
            print(f"[Bonded Box : {self.__yoloVersion}]\n")
            
    
    def netConfig(self, serverIP : str, portNumber : int):
        """ config ip and port """
        self.serverIP = serverIP
        self.portNumber = portNumber
        
        if _debug :
            print("\n++[new net Config]++\n")
            print(f"[new server IP : {self.__serverIP}]")
            print(f"[new Port Number : {self.__portNumber}]\n")
    
    def __startConnection(self):
        """ start connection socket """
        try:
            self.__socket.connect((self.__serverIP, self.__portNumber))
            self.__socket.send(f'camera connected NO. {threading.get_ident()}'.encode())
        except : 
            raise ConnectionError(f"can't connect to server, {self.__serverIP}:{self.__portNumber}")
        
        if _debug :
            print(f"\n**[connection started]**\n")
    
    def reporter(self):
        """ send traffic report the C&C """
        pass
    
    def videoLoader(self, source):
        """ determine video source """
        pass
    
    def streamVideo(self):
        """ real-Time Camera """
        pass
    
    def detector(self, detect = 'vehicles'):
        """ for determine detect all labels or vehicles """
        pass
    
    def run(self):
        """ run camera and connect to server """
        self.__startConnection()
        print(f"\n<camera NO. {threading.get_ident()} available>\n")
        
        if _debug :
            print(f"\n<< [app start running : Debug mode] >>\n")
            print(f"\n<< [ camera NO. {threading.get_ident()} ] >>\n")
        
    @property
    def yoloVersion(self):
        return self.__yoloVersion
        
    @yoloVersion.setter
    def yoloVersion(self,ver):
        if not re.match('^\S{5}\d\S*\.pt$',ver):
            raise ValueError("Yolo Version is not vaild")
        
        self.__yoloVersion = ver
        
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
        
    @property
    def bondedBox(self):
        return "Bonded box : " + str(self.__bondedBox)
    
    @bondedBox.setter
    def bondedBox(self,val):
        if val not in list((True,False)):
            raise ValueError('boded box value invalid')
        
        self.__bondedBox = val
        
if __name__ == "__main__":
    """ this class, you can use this \
        only with import and create object """
    raise RuntimeError("this is Class, pls import and create new object")