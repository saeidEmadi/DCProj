#from ultralytics import YOLO
#model = YOLO('yolov9e.pt')

class Camera:
    """ Camera Class : \
        track objects and detect Traffic """
    def __init__(self, serverIP, serverPort):
        """ initial variables """
        pass
    
    def netConfig(self, serverIP, serverPort):
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
        pass
    
    @serverIP.setter
    def serverIP(self, serverIP):
        """ set server IP """
        pass
    
    @property
    def serverPort(self):
        """ return server Port """
        pass
    
    @serverPort.setter
    def serverPort(self, serverPort):
        """ set server Port """
        pass