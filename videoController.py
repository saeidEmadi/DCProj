import os
import argparse

class VideoController():
    """ this class use for control video versions 
        if videos folder is exists : 
            True : change video names and move in to
            else : make video directory """
    def __init__(self, source : str, dest : str = '.', formats : list = ['mp4','mkv']):
        """ initial class constructor """
        # check video path folder
        self.source = source
        self.dest = dest
        self.formats = formats
        
        try : 
            if 'videos' not in os.listdir(dest):
                #os.mkdir(os.path.dirname(__file__)+"\\videos")
                print(f"video folder created in : {os.path.dirname(dest)}")
        except :
            raise FileNotFoundError('The directory name is invalid')
    
    def videoAdder(self) -> bool :
        """ add video from source to driver Path """
        pass
    
    def __driverChecker(self) -> bool :
        """ check driver.py for running | 
            True : run app and add video, etc
            False : add this script to driver path 
                    or add path """
        pass
    
    def __nameChanger(self, nameStr) -> str :
        """ change video name """
        pass
    
    def checkPairVideoAndClient(self) -> list :
        """ check pair camera's and Client's """
        pass
    
    @property
    def source(self) -> str :
        return self.__source
    
    @source.setter
    def source(self, sourceAddress) -> None :
        """ check source address valid """
        if self.__pathIsFileOrDir(sourceAddress) :
            self.__source = sourceAddress
        else : 
            raise FileExistsError('source Path is not exists.')
    
    @property
    def dest(self) -> str : 
        return self.__dest
    
    @dest.setter
    def dest(self, destAddress) -> None :
        """ check destination address valid """
        if self.__pathIsFileOrDir(destAddress) :
            self.__dest = destAddress
        else : 
            raise FileExistsError('destination Path is not exists.') 
    
    @property
    def formats(self) -> list :
        return self.__formats
    
    @formats.setter
    def formats(self, formats) -> None :
        self.__formats = formats
    
    def __pathIsFileOrDir(self, address) -> bool :
        """ check Address Path """
        if os.path.isdir(address) :   # directory address check
            return True
        elif os.path.isfile(address) :  # file address check
            return True
        return False
    
if __name__ == "__main__" :
    
    """ Script mode runner """
    
    print("[ video controller Running : CLI Mode]")
    
    # argument parser
    argparser = argparse.ArgumentParser(
        description = "video controller runner Script | run script for input controlling video for camera's",\
            prog = 'videoController')
    argparser.add_argument('source_address', metavar = 'source address', type = str, nargs = 1, \
        help = "video source address (folder or video name)")
    argparser.add_argument('--dest', '-d', metavar = 'destination address', type = str, nargs = 1, \
        help = "video destination address folder (video folder)", default = list(['.'],))
    argparser.add_argument('--format', '-f', metavar = 'format', type = str, nargs = '+', \
        required = True ,help = "find this formats in directory")
    
    args = argparser.parse_args()
    print(args)
    
    c = VideoController(source = args.source_address[0], dest = args.dest[0])