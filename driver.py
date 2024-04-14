import argparse
import configparser

if __name__ == "__main__":
    
    # config parser
    config = configparser.ConfigParser()
    config.read('config.ini')

    # argument parser
    argparser = argparse.ArgumentParser(description = "Traffic detection and notify C&C (prototype)")
    argparser.add_argument('host', metavar = 'host', type = str, nargs = 1, help = "Server Address for listening clients")
    argparser.add_argument('port', metavar = 'port', type = int, nargs = 1, help = "port number")
    argparser.add_argument('-v', '--yolov', metavar = 'yoloVersion', type = str, nargs = 1, help = "Yolo pre-Train Model version (default : "+config['Traffic Camera']['yoloVersion']+")",default = config['Traffic Camera']['yoloVersion'])
    argparser.add_argument('-BB', '--bb', action = "store_true", help = "Draw A Bounding Box for each object")
    argparser.add_argument('-d', '--detect', metavar = 'coco class name\'s', default = 'vehicles', nargs = '*', help = "detect all objects in ms-COCO or only vehicles (example : vehicles person [etc.]], default = vehicles)")
    argparser.add_argument('--test', action = "store_true", help = "flag for Enable defaults parameters run :: \n "+config['Server']['server IP']+" "+config['Server']['port']+" -v "+config['Traffic Camera']['yoloVersion']+", -c 5")
    argparser.add_argument('--stream', action = "store_true", help = "stream traffic camera real-Time")
    argparser.add_argument('--debug', action = "store_true", help = "flag for Enable Debug mode [show CLI logs]")
    args = argparser.parse_args()
    
    print(args)