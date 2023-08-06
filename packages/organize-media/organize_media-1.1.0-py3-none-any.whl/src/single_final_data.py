import os

from .initial_data import InitialData
from .original_file import OriginalFile
from .personal_logging import PersonalLogging
from .time_file import TimeFile

from tests.test_media import Media
from tests.test_month import Month
from tests.test_position import Position
from tests.test_year_month import YearMonth 
from tests.test_time import Time



class SingleFinalData:
    '''@ovewview this class represent the final data necessaryt ot run the copy of the original file'''

    def __init__(self, newroot, neworiginaltupla):
       self.log = PersonalLogging("SingleFinalData", False)
       self.root = newroot
       self.originaltupla = neworiginaltupla

    def tupla(self):
        '''@return  data of the original file as tupla'''
        self.log.print("tupla iniziale:\n" + str(self.originaltupla.tupla()[0]) )
        year = self.originaltupla.time.year()
        month = self.originaltupla.time.month()
        topic = self.originaltupla.position.topic() 
        filename = self.originaltupla.position.name()
        extension = self.originaltupla.position.extension()
        root = self.root
        media = Media(extension)

        day = self.originaltupla.time.day()
        return (root, year, month, topic, media, filename, extension, day)

    def physicalFile(self):
        '''@return the complete path as String'''
        data = self.tupla()
        listdata = [data[0], data[1], YearMonth(data[1], data[2]).show(), data[3],  data[4].directory() , data[5], data[6].name()]
        path = os.sep.join(listdata[0:6])
        self.log.print("path: {0}".format( path ) )
        return str(path + "." + data[6].name() )
    
    def physicalPath(self):
        '''@return the complete path as String, no filename and extension'''
        data = self.tupla()
        listdata = [data[0], data[1], data[2].name(), data[3], data[4].directory() , data[5] ]
        return os.sep.join(listdata[0:5])
        
    def __repr__(self):
        return "SingleFinalData[" + self.physicalFile() + "]\n>>>" + str(self.tupla())

    def __eq__(self, other):
        return self.physicalFile() == other.physicalFile()


