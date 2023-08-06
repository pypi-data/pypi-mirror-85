from .personal_logging import PersonalLogging
import os
import platform


        
class FileToWrite:
    '''@overview: class or file to be written'''

    def __init__(self, new_path):
        self.path = new_path
        self.logging = PersonalLogging ("FileToWrite", False)

    def hard_disk(self, list_rows):
        '''@effects: create the physicalfile'''
        self.logging.print("<hard_disk:" + str(list_rows))
        with open(self.path, "w") as file_tmp:
            for tmp in list_rows:
                self.logging.print(tmp)
                file_tmp.write(tmp)


    def __repr__(self):
        return "FiletoWrite[%s]" %self.path 
