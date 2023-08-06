from .csv_image import CSVImage
from .file_to_write import FileToWrite
from tests.test_label import LabelImage
from .personal_logging import PersonalLogging
from .safe_file import SafeFile
from tests.test_label import LabelVideo
from tests.test_csv_video import CSVVideo


class FinalDataTag:
    '''@overview: class for the good tags'''
    
    def __init__(self, new_safe_file, new_list_tag):
        self.safefile = new_safe_file
        self.list_data = new_list_tag
        self.logging = PersonalLogging("FinalDataTag", False )

    def data(self):
        '''@return list of data file'''
        list_rows = []
        for tmp_value in self.list_data:
                list_rows.append ( "{0};".format ( tmp_value ) ) 
        self.logging.print ( "tmp: %s" % str ( list_rows ) )
        list_rows.sort()
        return self.safefile.safe ( list_rows )
        
