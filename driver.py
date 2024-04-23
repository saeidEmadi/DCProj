import argparse
import configparser
from server import Server
from trafficCamera.runMain import Camera
import threading
from videoController import VideoController
    
def __serverSide(args) :
    if args.test :
        """ server default mode : Config file params """
        server = Server(DEBUG = True)
    else :
        """ server run with args input """
        server = Server(serverIP = str(args.host[0]), portNumber = int(args.port[0]), DEBUG = args.debug)
    server.run()
    
def __clientSide(args):
    videoController = VideoController('.','.')
    videoController.videoAdder()
    """ initialing Client's and run"""
    if args.test :
        """ clients default mode : 5 client with Config file params """
        videos = videoController.getCameraOfflineVideos(5)
        for i in range(5):
            c = Camera(DEBUG = True)
            c.streamInput(".\\videos\\"+videos[i])      #set video input
            th = threading.Thread(target = c.run)
            th.start()
    else :
        """ clients create with args input """
        videos = videoController.getCameraOfflineVideos(args.client[0])
        for i in range(args.client[0]):
            c = Camera(serverIP = str(args.host[0]), portNumber = int(args.port[0]), \
                yoloVersion = args.yolov[0], yoloConf = args.yoloConf[0], trafficConf = args.trafficConf[0], \
                detectionLabels = args.detect, show = args.stream, DEBUG = args.debug, device = str(args.device[0]))
            c.streamInput(".\\videos\\"+videos[i])      #set video input
            th = threading.Thread(target = c.run)
            th.start()

if __name__ == "__main__":
    
    # config parser
    config = configparser.ConfigParser()
    try : 
        config.read('config.ini')
    except :
        raise FileExistsError("config.ini file is not exists.")

    # argument parser
    argparser = argparse.ArgumentParser(description = "Traffic detection and notify C&C (prototype)")
    argparser.add_argument('host', metavar = 'host', type = str, nargs = 1, help = "Server Address for listening clients")
    argparser.add_argument('port', metavar = 'port', type = int, nargs = 1, help = "port number")
    argparser.add_argument('-v', '--yolov', metavar = 'yoloVersion', type = str, nargs = 1, \
        help = "Yolo pre-Train Model version (default : yolov9e)", \
        default = ['yolov9e'])
    argparser.add_argument('-yc', '--yoloConf', metavar = 'yoloConf', type = float, nargs = 1, \
        help = "Yolo pre-Train Model confidence (default : 0.6)", \
        default = [0.6])
    argparser.add_argument('-tc', '--trafficConf', metavar = 'trafficConf', type = int, nargs = 1, \
        help = "traffic Max confidence (default : 8)", default = [8])
    argparser.add_argument('-d', '--detect', metavar = 'coco class name\'s', default = 'vehicles', nargs = '*', \
        help = "detect all objects in ms-COCO or only vehicles (example : vehicles person [etc.]], default = vehicles)")
    argparser.add_argument('-c', '--client', metavar = 'INT', type = int, default = '5', nargs = 1, \
        help = "number of clients ,[default = 5]")
    argparser.add_argument('--test', action = "store_true", \
        help = "flag for Enable defaults parameters run :: \n "+config['Server']['server IP'] \
            +" "+config['Server']['port']+" -v yolov9e, -c 5")
    argparser.add_argument('--stream', action = "store_true", help = "stream traffic camera real-Time")
    argparser.add_argument('--debug', action = "store_true", help = "flag for Enable Debug mode [show CLI logs]")
    argparser.add_argument('--device',metavar = "core" , nargs = 1, type = str, required = True, \
        help = "yolo gpu core  or CPU [ex. cpu , cuda:0]")
    args = argparser.parse_args()

    serverThread = threading.Thread(target = __serverSide, args = (args,))
    ClientThread = threading.Thread(target = __clientSide, args = (args,))
    serverThread.start()
    ClientThread.start()