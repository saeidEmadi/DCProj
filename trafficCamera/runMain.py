import ipaddress
import socket
import configparser
import threading
import cv2
import pickle
import struct
from ultralytics import YOLO
import re
class Camera():
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
        yoloVersion : str = 'yolov9e',show : bool = False, device : str = 'cpu', \
        detectionLabels : list = ['vehicles'], yoloConf : float = 0.6, \
        trafficConf : int = 1, stream : bool = False, DEBUG : bool = False):
        
        """ initial Thread initials """
        threading.Thread.__init__(self)
        """ initial variables """
        
        # define global _debug for validate Debug mode
        global _debug, _show, _stream
        self.serverIP = serverIP
        self.portNumber = portNumber
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.yoloVersion = yoloVersion
        _debug, _show, _stream = DEBUG, show, stream
        # self.__capture = 0
        self.detectionLabels = detectionLabels
        self.yoloConf = yoloConf
        self.trafficConf = trafficConf
        self.device = device
        self.__cv2BufferSize = 100      # CV2 Video Capture Buffer Size

        if _debug :
            print("\n++[new Camera object]++\n")
            print(f" Camera : [server IP : {self.__serverIP}]")
            print(f"[ Camera Port Number : {self.__portNumber}]")
            # print(f" Camera : [Stream Show  : {self._show}]")
            print(f" Camera : [yolo Version : {self.__yoloVersion}]")
            print(f" Camera : [detection Labels : {self.__detectionLabels}]")
            print(f" Camera : [detection : {self.__detection}]")       
            print(f" Camera : [yolo conf : {self.__yoloConf}]")
            print(f" Camera : [traffic conf : {self.__trafficConf}]")
    
    def netConfig(self, serverIP : str, portNumber : int):
        """ config ip and port """
        self.serverIP = serverIP
        self.portNumber = portNumber
        
        if _debug :
            print(" Camera : \n++[new net Config]++\n")
            print(f" Camera : [new server IP : {self.__serverIP}]")
            print(f" Camera : [new Port Number : {self.__portNumber}]\n")
    
    def __startConnection(self):
        """ start connection socket """
        try:
            self.__socket.connect((self.__serverIP, self.__portNumber))
            self.__socket.send(f'camera connected NO. {threading.current_thread().ident}'.encode())
        except : 
            raise ConnectionError(f"can't connect to server, {self.__serverIP}:{self.__portNumber}")
        
        if _debug :
            print(f"\n Camera : **[connection started]**\n")
    
    def __closeConnection(self):
        self.__socket.close()
        
        if _debug :
            print(f"\n** Camera : [connection closed]**\n")
    
    def streamInput(self, inputCapt):
        """ this function only capture set """
        self.__capture = inputCapt
        
        if _debug :
            print(f" Camera : cv2 Capture set : {self.__capture}")
                
    def __detector(self):
        # detection index from ClassName
        self.__detection = []
        for _ in range(len(self.__detectionLabels)):
            self.__detection.append(className.index(self.__detectionLabels[_]))
            
        if _debug : 
            print(f" Camera : convert class Names : {self.__detectionLabels}")
            print(f" Camera : to ")
            print(f" Camera : {self.__detection}")
    
    def __modelPredictor(self):
        model = YOLO(self.__yoloVersion)
        cv2.VideoCapture().set(cv2.CAP_PROP_BUFFERSIZE, self.__cv2BufferSize)
        if _debug :
            print(f" Camera : <model Predictor start.>")
            
        if _show :
            while True :
                cap = cv2.VideoCapture(str(self.__capture))
                success, frame = cap.read()
                
                if not success:
                    raise FileNotFoundError('camera is off or video file ended.')
                
                results = model(frame, stream=True, show_labels = True, device = self.__device, \
                    conf = self.__yoloConf, classes = self.__detection, verbose = False)
                count =  0
                for r in results:
                    for box in r.boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                        count += 1
                        cv2.putText(frame, className[int(box.cls[0])], [x1, y1], cv2.FONT_HERSHEY_SIMPLEX,\
                            fontScale = 1, color = (255, 0, 0), thickness = 2)
                self.__checkTraffic(count)
                # video Streaming
                """ if _stream : 
                    piklFrema = pickle.dumps(frame)
                    msg = struct.pack("Q", len(piklFrema)) + piklFrema
                    try :
                        self.__socket.sendall(msg)
                    except ConnectionResetError :
                        raise ConnectionError("connection loss")
                    except :
                        print(" Camera : can't sent frame")
                """    
                cv2.imshow('Camera', frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        else :
            while True :
                cap = cv2.VideoCapture(str(self.__capture))
                success, frame = cap.read()
                
                if not success:
                    raise FileNotFoundError('camera is off or video file ended.')

                results = model(frame, show = False, conf = self.__yoloConf, classes = self.__detection, \
                    verbose = False, device = self.__device)
                count =  0
                for r in results:
                    for _ in r.boxes:
                        count += 1
                    self.__checkTraffic(count)
                # video Streaming
                """if _stream : 
                    piklFrema = pickle.dumps(frame)
                    msg = struct.pack("Q", len(piklFrema)) + piklFrema
                    try :
                        self.__socket.sendall(msg)
                    except ConnectionResetError :
                        raise ConnectionError("connection loss")
                    except :
                        print(" Camera : can't sent frame")
                """
                if cv2.waitKey(1) == ord('q'):
                    break      
                
        print(" Camera : camera off : this connection will disconnect")                  
        self.__closeConnection()
    
    """
    def reporter(self, msg):
        
        try : 
            reportThread = threading.Thread(target = , args = (msg.encode(),), \
                name = "count reporter Thread")
            reportThread.start()
        except :
            print(" Camera : can't send report to server")
        # self.__socket.send(msg.encode())
    """
    
    def __checkTraffic(self, count : int):
        if _debug :
            print(f" Camera : < Max Count : {self.__trafficConf} >")
            print(f" Camera : < count No. : {count} >")
            print(f" Camera : < thread NO : {threading.current_thread().ident} >")
            
        if count > self.__trafficConf :
            try :
                self.__socket.send((f'camera NO. {threading.current_thread().ident} | count : {count} | traffic : +').encode())
            except:
                print(" Camera : can't send report to server")
                self.__startConnection()
    
    def run(self):
        """ run camera and connect to server """
        if _debug :
            print(f"\n Camera : << [app start running : Debug mode] >>\n")
            print(f"\n Camera : << [ camera NO. {threading.current_thread().ident} ] >>\n")
            
        self.__startConnection()
        predictorThread = threading.Thread(target = self.__modelPredictor, name = "camera model predictor Thread")
        predictorThread.start()
        #self.__closeConnection()
        
    @property
    def trafficConf(self):
        return self.__trafficConf
    
    @trafficConf.setter
    def trafficConf(self, trafficConf):
        if trafficConf > 0 :
            self.__trafficConf = trafficConf
        else :
            raise ValueError('trafficConf must be positive number')
    
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
            if 'vehicle' or 'vehicles' in detectionLabels:    
                self.__detectionLabels = ['bicycle','car','motorbike','aeroplane','bus','train','truck','boat']
            else :
                for _ in detectionLabels:
                    if _ in className:
                        self.__detectionLabels.append(_)
                    else :
                        print(f" Camera :  class name : {_} != ms-coco list")
        # convert labels to arg index                
        self.__detector()

    @property
    def yoloVersion(self):
        return self.__yoloVersion
        
    @yoloVersion.setter
    def yoloVersion(self, ver):
        if not re.match('^\S{5}\d\S*$',ver):
            raise ValueError("Yolo Version is not vaild")
        self.__yoloVersion = ver+".pt"

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
    def device(self) :
        return self.__device

    @device.setter
    def device(self, deviceName) :
        """ select yolo model code devices 
            0 : => CPU
            cuda:n => n core in GPU """
        if deviceName in ['0','1','2','3','cuda:0','cuda:1','cuda:2','cuda:3','cpu'] :
            self.__device = deviceName
        else :
            raise ProcessLookupError("yolo model core invalid [0 for cpu and cuda:0 for GPU]")        

if __name__ == "__main__":
    """ this class, you can use this \
        only with import and create object """
    raise RuntimeError("this is Class, pls import and create new object")