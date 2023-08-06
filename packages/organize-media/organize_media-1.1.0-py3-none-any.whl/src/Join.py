import os
import sys

from .copy import Copy
from .csv_image import CSVImage
from .file_to_write import FileToWrite
from .final_data_csv import FinalDataCSV
from .personal_logging import PersonalLogging
from .read_file_ini import ReadFileINI#TODO maybe . instead of organziemedia
from .read_file_ini import Video#TODO maybe . instead of organziemedia
from .safe_file import SafeFile
from .write import Write

from tests.test_name_file import Final
from tests.test_name_file import NameCSV
from tests.test_read_file_csv import Image
from tests.test_read_file_csv import ReadFileCSV
    #TODO mettere controllo che il path passato deve avere il sepratore os.sep corretto
    # altrimenti ci saranno problemi con i file


class Join:
    """@overview: class to join CSV and INI file"""
    def __init__(self, new_args ):
        self.directory = new_args[0]

    def __repr__(self):
        return 'Join(%s)' % (self.directory)

    def __str__(self):
        return "Join(%s)" % (self.directory)

    def __eq__(self, other):
        return self.directory == other.directory
    
    def run(self):
        """
        run the join between data of INI file and CSV file
        take the dir and put the ini inside an object
        """        
        #TODO centralize in an object
        properties_ini = ReadFileINI(self.directory).read()# has INI
        #TODO control that every property has a value, othrwise exception
        properties_file_csv = Image ( ReadFileCSV ( self.directory ) ).read() 
        """  
        every row-obejct is put inside another object with the optional data and the INI object  
        this object will be in another list
        the list is passed to a class that creates the file'
        this object is formatted as CSV
        """
        filecsv = FinalDataCSV ( 
                SafeFile ( 
                    FileToWrite ( 
                        NameCSV ( self.directory, 
                            Final() 
                            ).name() 
                        ) 
                    ), 
                properties_file_csv, 
                properties_ini ) 
        filecsv.data ( )
