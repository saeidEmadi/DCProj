import ipaddress
import socket
import configparser
import threading
import cv2
from ultralytics import YOLO
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
    
    # ms-coco class list
    global className
    className = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
    
    def __init__(self, serverIP : str = config['Server']['server IP'], \
        portNumber : int = int(config['Server']['port']), \
        yoloVersion : str = 'yolov9e.pt',show : bool = False, \
        detectionLabels : list = ['vehicles'], yoloConf : float = 0.6, \
        DEBUG : bool = False):
        
        """ initial Thread initials """
        threading.Thread.__init__(self)
        """ initial variables """
        
        # define global _debug for validate Debug mode
        global _debug, _show
        self.__count = 0
        self.serverIP = serverIP
        self.portNumber = portNumber
        self.bondedBox = False
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.yoloVersion = yoloVersion
        _debug, _show = DEBUG , show
        self.__capture = 0
        self.detectionLabels = detectionLabels
        self.yoloConf = yoloConf
        
        if _debug :
            print("\n++[new Camera object]++\n")
            print(f"[server IP : {self.__serverIP}]")
            print(f"[Port Number : {self.__portNumber}]")
            print(f"[Bonded Box : {self.__bondedBox}]")
            print(f"[Stream Show  : {self._show}]")
            print(f"[yolo Version : {self.__yoloVersion}]")
            print(f"[detection Labels : {self.__detectionLabels}]")
            print(f"[detection : {self.__detection}]")       
            print(f"[yolo conf : {self.__yoloConf}]")
    
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
            self.__socket.send(f'camera connected NO. {threading.current_thread().ident}'.encode())
        except : 
            raise ConnectionError(f"can't connect to server, {self.__serverIP}:{self.__portNumber}")
        
        if _debug :
            print(f"\n**[connection started]**\n")
    
    def __closeConnection(self):
        self.__socket.close()
        
        if _debug :
            print(f"\n**[connection closed]**\n")
    
    def reporter(self):
        """ Threading Function """
        """ send traffic report the C&C """
        self.__socket.send(f'camera NO. {threading.current_thread().ident} | count : {self.__count}'.encode())
    
    def videoLoader(self, source):
        """ determine video source """
        pass
    
    def streamVideo(self):
        """ real-Time Camera """
        pass
    
    def __detector(self):
        # detection index from ClassName
        self.__detection = []
        for _ in range(len(self.__detectionLabels)):
            self.__detection.append(className.index(self.__detectionLabels[_]))
    
    def __modelGenerator(self):
        return YOLO(self.__yoloVersion)
    
    def __modelPredictor(self):
        pass
    
    def run(self):
        """ run camera and connect to server """
        self.__startConnection()
        self.reporter()
        # self.__closeConnection()
        
        if _debug :
            print(f"\n<< [app start running : Debug mode] >>\n")
            print(f"\n<< [ camera NO. {threading.current_thread().ident} ] >>\n")
        
    @property
    def yoloConf(self):
        return self.__yoloConf
    
    @yoloConf.setter
    def yoloConf(self, conf):
        if 0.01 <= conf <= 0.99 :
            self.__yoloConf = conf
        else:
            raise ValueError('minimum confidence threshold for detections between 0.01 to 0.99')
    
    @property
    def detectionLabels(self):
        return self.__detectionLabels
        
    @detectionLabels.setter
    def detectionLabels(self, detectionLabels : list):
        # detection Labels from ClassName
        self.__detectionLabels = []
        if 'all' in detectionLabels :
            self.__detectionLabels = className
        else :
            if 'vehicle' in detectionLabels:    
                self.__detectionLabels = ['bicycle','car','motorbike','aeroplane','bus','train','truck','boat']
            else :
                for _ in detectionLabels:
                    if _ in className:
                        self.__detectionLabels.append(_)
                    else :
                        print(f" class name : {_} != ms-coco list")
        # convert labels to arg index                
        self.__detector()

    @property
    def yoloVersion(self):
        return self.__yoloVersion
        
    @yoloVersion.setter
    def yoloVersion(self, ver):
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