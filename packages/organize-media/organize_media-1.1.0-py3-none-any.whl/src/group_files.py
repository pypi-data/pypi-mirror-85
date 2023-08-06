import shutil
import os
from .personal_logging import PersonalLogging

class GroupFiles:
    '''
    @overview:  class that copies the file from original path to final path
    '''

    def __init__(self, new_map_files):
        self.logging = PersonalLogging("GroupFiles", False)
        self.map_files = new_map_files


    def copy(self):
        '''
        copy all the files
        '''
        for originalfile in self.map_files.keys():
            self.logging.print("copy(" +str(originalfile)  + ")" )
            destinationfile = self.map_files[originalfile]
            Transfert(originalfile, destinationfile.physicalFile()).copy()


class Transfert:
    '''
    @overview: this class copy one file from one source to another
    '''

    def __init__(self, new_source, new_destination):
        self.source = new_source
        self.destination = new_destination
        self.logging = PersonalLogging("Transfert", False)

    def copy(self):
        '''
        copy one file
        '''
        msg_source = "" + str(self.source) + ""
        msg_destination = "" + str(self.destination) + ""
        if self.alreadyCopied() :#TODO decorator
            self.logging.print("Already existing file: %s" % self.destination)
        else:
            self.logging.print("copy(" + str(self.source) + "," + str(self.destination) + ")")
            shutil.copy(self.source, self.destination)
                
        
    def alreadyCopied(self):
        '''
        @return true if the file already exists
        ''' 
        return os.path.exists(self.destination)

