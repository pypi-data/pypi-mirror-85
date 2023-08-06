import os
from .personal_logging import PersonalLogging
from .original_file import OriginalFile

class FileSystem:
    '''@overview: this class reads the files inside a directory'''

    def __init__(self, newInputDir):
        '''It read a directory and the subdirectory
        inputDIr: complete path of the root directory'''
        self.inputDir = newInputDir;
        self.log = PersonalLogging("FileSystem", False)

    def walk(self):
        '''@return the list of the read file
        It traverses root directory, and list directories as dirs and files as files
        in recursive way'''
        #TODO concatenation of string
        self.log.print("Filesystem.walk("+str(self.inputDir)+")");
        readfiles = [];
        return self.walksubdir(self.inputDir, readfiles);
       
    def walksubdir(self, partialRoot, readfiles):
        '''@return the partial list of the files'''
        for root, dirs, files in os.walk(partialRoot):
            for filetmp in files:
                readfiles.append (str(root) + os.sep + str(filetmp) ) ;
                self.log.print("Filesystem.walksubdir.filetmp(" + str(filetmp) + ")");
            for directory in dirs:
                self.walksubdir(directory, readfiles)
        self.log.print("Filesystem.walksubdir(" + str( readfiles ) + "): li trasformo in OriginalFile in una funzione a parte");
        return readfiles;

         

