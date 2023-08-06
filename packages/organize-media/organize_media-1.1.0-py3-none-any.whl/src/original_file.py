from .personal_logging import PersonalLogging
import os
from tests.test_extension import Extension
from tests.test_month import Month
from .time_file import TimeFile
from tests.test_time import Time
from tests.test_position import Position
from .initial_data import InitialData

class OriginalFile:
    """@overview this class represent the logical representation of a file to copy"""
    def __init__(self, newabsolutepath, newfilename):
       self.log = PersonalLogging("OriginalFile", False)
       self.absolutepath = newabsolutepath
       self.filename = newfilename

    def tupla(self):
        """@return the elementary data of the original file in tupla"""
        self.log.print(">OriginalFIle.tupla(" + self.physicalFileAsString() + ")")
        completeDateTime = Time(TimeFile(self.physicalFileAsString()).complete())
        position = Position(self.absolutepath, self.filename)        
        res = InitialData(position, completeDateTime)
        self.log.print("<" + str(res.tupla()))
        return res
    
    def physicalFile(self):
        """@return the complete path """
        return self.absolutepath + os.sep + self.filename

    def physicalFileAsString(self):
        """@return the complete path as String"""
        return str(self.physicalFile())

    def __str__(self):
        return self.physicalFileAsString()
    
    def __repr__(self):
       return "OriginalFile(" +str(self.absolutepath) + "," + str(self.filename) + ")"
    
    def __eq__(self, other):
        return self.physicalFile() == self.physicalFile()

