import os
import argparse

class VideoController():
    """ this class use for control video versions 
        if videos folder is exists : 
            True : change video names and move in to
            else : make video directory """
    def __init__(self, source : str, dest : str = '.', formats : list = ['.mp4','.mkv']):
        """ initial class constructor """
        # check video path folder
        self.source = source
        self.dest = dest
        self.formats = formats
        self.__videos = self.__fetchVideos(source)
        self.__lastIndex = self.__getLastIndex()
        
        try : 
            if 'videos' not in os.listdir(dest):
                #os.mkdir(os.path.dirname(__file__)+"\\videos")
                print(f"video folder created in : {os.path.dirname(dest)}")
        except :
            raise FileNotFoundError('The directory name is invalid')
    
    def videoAdder(self) -> bool :
        """ add video from source to driver Path """
        if os.path.isdir(self.__source) :
            pass
        elif os.path.isfile(self.__source) :
            pass
    
    def __driverChecker(self) -> bool :
        """ check driver.py for running | 
            True : run app and add video, etc
            False : add this script to driver path 
                    or add path """
        pass
    
    def __getLastIndex(self) -> int :
        """ find last index for set new name indexing """
        
        videos = self.__fetchVideos(self.__dest+"\\videos")
        if len(videos) > 0 :
            file_name, _ = os.path.splitext(videos[-1])
            return int(''.join(_ for _ in file_name if _.isdigit()))
        
        return 0
        
    def __getNemName(self, videoFormat) -> str :
        """ create new video name
            pattern : video{index}[.format]"""
        self.__lastIndex += 1
        return f"video{self.__lastIndex - 1}{videoFormat}"
    
    def checkPairVideoAndClient(self, numOfClients : int) -> list :
        """ check pair camera's and Client's """
        
        pass
    
    def __fetchVideos(self, addr : str) -> list :
        """ fetch vide files and directory """
        if os.path.isfile(addr) :
            addr = os.path.realpath(addr)
            
        direList = os.listdir(addr)
        videos = list()
        for _ in direList :
            file_name, extension = os.path.splitext(_)
            if extension in self.__formats :
                videos.append(_)
        return videos
    
    @property
    def source(self) -> str :
        return self.__source
    
    @source.setter
    def source(self, sourceAddress) -> None :
        """ check source address valid """
        if os.path.isdir(sourceAddress) \
            or os.path.isfile(sourceAddress) :
            self.__source = sourceAddress
        else : 
            raise FileExistsError('source Path is not exists.')
    
    @property
    def dest(self) -> str : 
        return self.__dest
    
    @dest.setter
    def dest(self, destAddress) -> None :
        """ check destination address valid """
        if os.path.isdir(destAddress) :
            self.__dest = destAddress
        else : 
            raise FileExistsError('source Path is not exists.')
    
    @property
    def formats(self) -> list :
        return self.__formats
    
    @formats.setter
    def formats(self, formats) -> None :
        self.__formats = formats
    
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