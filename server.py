import threading
import configparser
from typing import Final
class Server(threading.Thread):
    """ Server Class use for receive report and data from cameras """
    # read config file and initial config variables
    config = configparser.ConfigParser()
    try : 
        config.read('config.ini')
    except :
        raise FileExistsError("config.ini file is not exists.")
    
    # default value for listen socket backLog    
    backlogListenVal : Final[int] = config['Server']["backlogListenVal"]
    
    def __init__(self, serverIp : str = config['Server']['server IP'], \
            serverPort : int = int(config['Server']['port']), \
            DEBUG : bool = False):
        """ initial class variables """
        pass
    
    def stream(self):
        """ receive video from camera """
        pass
    
    def run(self):
        """ run server """
        pass
    
    
if __name__ == "__main__":
    """ this class, you can use this \
        with import and create object \
        or CLI run Server"""
    print("\n[Server Running : CLI Mode]\n")