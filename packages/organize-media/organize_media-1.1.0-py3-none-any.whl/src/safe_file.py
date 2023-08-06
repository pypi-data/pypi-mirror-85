import os
import platform
import errno

from .file_to_write import FileToWrite 
from .personal_logging import PersonalLogging

class SafeFile:
    '''@overview: this class creates the file if it does'nt exists, otherwise it does'nt modify the file''' 

    def __init__(self, new_file_to_write):
        self.file_to_write = new_file_to_write
        self.logging = PersonalLogging("SafeFile")

    def safe(self, list_rows):
        '''@return create the file INI for the photos'''
        exists = os.path.exists(self.file_to_write.path)
        #self.logging.print("safe:" + str(self.file_to_write.path))
        if(exists):
            self.logging.print("Existing file: %s" % self.file_to_write)
        else:
            try:
               self.file_to_write.hard_disk(list_rows)
               self.logging.print("Created file: %s" % self.file_to_write)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    self.logging.warn("Error in creating file: %s" % self.file_to_write)
                    raise

    def __repr__ (self):
        return "SafeFile:{0}".format ( str (self.file_to_write) )

    def __str__ (self):
        return "SafeFile:{0}".format ( str (self.file_to_write) )
