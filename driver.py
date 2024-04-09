import argparse
import configparser

if __name__ == "__main__":
    
    # config parser
    config = configparser.ConfigParser()
    config.read('config.ini')

    # argument parser
    argparser = argparse.ArgumentParser(description = "Traffic detection and notify C&C (prototype)")
    #argparser.add_argument('host', metavar = 'host', type = str, nargs = 1, help = "Server Address for listening clients")
    #argparser.add_argument('port', metavar = 'port', type = int, nargs = 1, help = "port number")
    argparser.add_argument('-v','--yolov', metavar = 'yoloVersion', type = str, nargs = 1, help = "Yolo pre-Train Model version (default : "+config['Traffic Camera']['yoloVersion']+")",default = config['Traffic Camera']['yoloVersion'])
    #argparser.add_argument('--test', action = "store_true", help = "Enable defaults parameters run :: \n "+config['Server Address']['server']+" "+config['Server Address']['port']+" -v "+config['Traffic Camera']['yoloVersion']+", -c 5")
    args = argparser.parse_args()