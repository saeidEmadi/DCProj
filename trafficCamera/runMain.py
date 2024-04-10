import ipaddress
#from ultralytics import YOLO
#model = YOLO('yolov9e.pt')

class Camera:
    """ Camera Class : \
        track objects and detect Traffic """
    def __init__(self, serverIP : str, portNumber : int):
        """ initial variables """
        self.serverIP = serverIP
        self.portNumber = portNumber
        pass
    
    def netConfig(self, serverIP : str, portNumber : int):
        """ config ip and port """
        pass
    
    def connectionCheck():
        """ check connection socket """
        pass
    
    def reporter():
        """ send traffic report the C&C """
        pass
    
    def videoLoader(self, source):
        """ determine video source """
        pass
    
    def streamVideo(self):
        """ real-Time Camera """
        pass
    
    def detector(self, detect):
        """ for determine detect all labels or vehicles """
        pass
    
    def yVersion(self, version):
        """ detect yolo version and download """
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
        pass
    
    @portNumber.setter
    def portNumber(self, portNumber : int):
        """ set server Port Number """
        
        if not isinstance(portNumber, int):
            raise ValueError("port number only integer valid")
        
        if not 1 <= portNumber <= 65535 :
            raise ValueError("port number invalid")
        
        self.__portNumber = portNumber