import threading

class Server(threading.Thread):
    """ Server Class use for receive report and data from cameras """
    def __init__(self, serverIp : str, serverPort : int, backlogListen : int, \
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