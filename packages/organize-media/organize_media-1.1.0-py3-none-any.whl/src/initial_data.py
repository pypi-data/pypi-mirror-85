import os

from .personal_logging import PersonalLogging
from .time_file import TimeFile

from tests.test_extension import Extension
from tests.test_month import Month
from tests.test_position import Position
from tests.test_time import Time

class InitialData:
    '''@overview class about hthe data of the read files'''

    #TODO change form POJO to object, add some kind of logic
    def __init__(self, newposition , newtime):
        self.time = newtime
        self.position = newposition
        self.log = PersonalLogging("IntialData", False)

    def tupla(self):
        '''@return the elementary data of the original file in tupla'''
        self.log.print(">InitialData.tupla(" + str(self.position) + ")")
        day = self.time.day()
        year = self.time.year()
        month = self.time.month()
        topic = self.position.topic()
        name = self.position.name()
        extension = self.position.extension()#.name()
        root = self.position.root()
        res = (year, month, topic, name, extension, root, day)
        self.log.print( "<" + str(res ))
        return res


    def __str__(self):
        return "InitialData[{0}][{1}]".format(self.position, self.time)
    
    def __repr__(self):
       return "InitialData(" +str(self.time) + "," + str(self.position) + ")"
    
    def __eq__(self, other):
        return self.position == self.position




