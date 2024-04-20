import argparse
import configparser
from server import Server
from trafficCamera.runMain import Camera
import threading
    
def __serverSide(args) :
    if args.test :
        """ server default mode : Config file params """
        server = Server(DEBUG = True)
    else :
        """ server run with args input """
        server = Server(serverIP = str(args.host[0]), portNumber = int(args.port[0]), DEBUG = args.debug)
    server.run()
    
def __clientSide(args):
    """ initialing Client's and run"""
    if args.test :
        """ clients default mode : 5 client with Config file params """
        for i in range(5):
            c = Camera(DEBUG = True)
            c.streamInput(f'video{i}.mp4')      #set video input
            th = threading.Thread(target = c.run)
            th.start()
    else :
        """ clients create with args input """
        for i in range(args.client):
            c = Camera(serverIP = str(args.host[0]), portNumber = int(args.port[0]), \
                yoloVersion = str(args.yolov), yoloConf = args.yoloConf, trafficConf = args.trafficConf, \
                detectionLabels = args.detect, show = args.stream, DEBUG = args.debug)
            c.streamInput(f'video{i}.mp4')      #set video input
            th = threading.Thread(target = c.run)
            th.start()

if __name__ == "__main__":
    
    # config parser
    config = configparser.ConfigParser()
    config.read('config.ini')

    # argument parser
    argparser = argparse.ArgumentParser(description = "Traffic detection and notify C&C (prototype)")
    argparser.add_argument('host', metavar = 'host', type = str, nargs = 1, help = "Server Address for listening clients")
    argparser.add_argument('port', metavar = 'port', type = int, nargs = 1, help = "port number")
    argparser.add_argument('-v', '--yolov', metavar = 'yoloVersion', type = str, nargs = 1, \
        help = "Yolo pre-Train Model version (default : "+config['Traffic Camera']['yoloVersion']+")", \
        default = config['Traffic Camera']['yoloVersion'])
    argparser.add_argument('-yc', '--yoloConf', metavar = 'yoloConf', type = float, nargs = 1, \
        help = "Yolo pre-Train Model confidence (default : "+config['Traffic Camera']['confidence']+")", \
        default = config['Traffic Camera']['confidence'])
    argparser.add_argument('-tc', '--trafficConf', metavar = 'trafficConf', type = int, nargs = 1, \
        help = "traffic Max confidence (default : 8)", default = 8)
    argparser.add_argument('-d', '--detect', metavar = 'coco class name\'s', default = 'vehicles', nargs = '*', \
        help = "detect all objects in ms-COCO or only vehicles (example : vehicles person [etc.]], default = vehicles)")
    argparser.add_argument('-c', '--client', metavar = 'INT', type = int, default = '5', nargs = 1, \
        help = "number of clients ,[default = 5]")
    argparser.add_argument('--test', action = "store_true", \
        help = "flag for Enable defaults parameters run :: \n "+config['Server']['server IP'] \
            +" "+config['Server']['port']+" -v "+config['Traffic Camera']['yoloVersion']+", -c 5")
    argparser.add_argument('--stream', action = "store_true", help = "stream traffic camera real-Time")
    argparser.add_argument('--debug', action = "store_true", help = "flag for Enable Debug mode [show CLI logs]")
    args = argparser.parse_args()

    serverThread = threading.Thread(target = __serverSide, args = (args,))
    ClientThread = threading.Thread(target = __clientSide, args = (args,))
    serverThread.start()
    ClientThread.start()