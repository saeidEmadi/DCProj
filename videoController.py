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
        self.__lastIndex = self.__getLastIndex()

        try : 
            if 'videos' not in os.listdir(dest):
                os.mkdir(os.path.dirname(dest)+"\\videos")
                print(f"video folder created in : {os.path.dirname(dest)}")
            else :
                # order video names
                self.__lastIndex = -1
                self.__ordering()
        except :
            raise FileNotFoundError('The directory name is invalid')
    
    def __fileMover(self, source : str, dest : str) -> bool :
        try :
            os.replace(source, dest)
            return True
        except : 
            return False
    
    def videoAdder(self) -> None :
        """ add video from source to destination Path """
        if os.path.isfile(self.__source) :
            file_name, extension = os.path.splitext(self.__source)
            if self.__fileMover(os.path.realpath(self.__source), \
                self.__dest+"\\videos\\"+self.__getNemName(extension)) :
                print(f"mv {os.path.realpath(self.__source)} to {self.__dest}\\videos\\")
            else :
                print(f"can\'t mov {os.path.realpath(self.__source)} to {self.__dest}\\videos\\")
        elif os.path.isdir(self.__source) :
            for video in self.__fetchVideos(self.source) :
                file_name, extension = os.path.splitext(os.path.realpath(video))
                if self.__fileMover(os.path.realpath(video), \
                    self.__dest+"\\videos\\"+self.__getNemName(extension)) :
                    print(f"mv {os.path.realpath(video)} to {self.__dest}\\videos\\")
                else :
                    print(f"can\'t mov {os.path.realpath(video)} to {self.__dest}\\videos\\")
                    
    def getCameraOfflineVideos(self, numOfClients : int) -> list :
        """ check pair camera's and Client's """
        j = self.__lastIndex
        lVideos = self.__fetchVideos(self.__source + "\\videos\\")
        videos = list()
        for _ in range(numOfClients):
            if j % self.__lastIndex == 0 :
                j -= self.__lastIndex
            videos.append(lVideos[j])
            j += 1
        return videos    

    def __getLastIndex(self) -> int :
        """ find last index for set new name indexing """
        
        videos = self.__fetchVideos(self.__dest+"\\videos")
        if len(videos) > 0 :
            file_name, _ = os.path.splitext(videos[-1])
            return int(''.join(_ for _ in file_name if _.isdigit()))
        
        return -1
        
    def __getNemName(self, videoFormat) -> str :
        """ create new video name
            pattern : video{index}[.format]"""
        self.__lastIndex += 1
        return f"video{self.__lastIndex}{videoFormat}"
    
    def __rename(self, old, new) -> bool :
        """ rename file """
        try :
            os.rename(old, new)
            return True
        except :
            return False
    
    def __ordering(self) -> None :
        """ ordering file's """
        videos = self.__fetchVideos(self.__dest+"\\videos")
        for video in videos :
            file_name, extension = os.path.splitext(video)
            if not self.__rename(self.__dest + "\\videos\\"+video, self.__dest +"\\videos\\"+self.__getNemName(extension)) :
                print("cant ordering files in videos folder")
    
    def __fetchVideos(self, addr : str) -> list :
        """ fetch vide files and directory """
        if os.path.isfile(addr) :
           addr = os.path.dirname(os.path.realpath(addr))
            
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
        required = True ,help = "find this formats in directory [.mp4|.mkv|etc]")
    
    args = argparser.parse_args()        
        
    c = VideoController(source = args.source_address[0], dest = args.dest[0])
    c.videoAdder()