from .csv_image import CSVImage
from .file_to_write import FileToWrite
from .personal_logging import PersonalLogging
from .safe_file import SafeFile

from tests.test_csv_video import CSVVideo
from tests.test_label import LabelVideo
from tests.test_label import LabelImage


class FinalDataCSV:
    """
    @overview: class for the partial csv file
    """
    
    def __init__(self, new_safe_file, new_list_manual_csv, new_properties_ini):
        self.safefile = new_safe_file
        self.list_data = new_list_manual_csv
        self.properties_ini = new_properties_ini
        self.logging = PersonalLogging("FinalDataCSV")

    def data(self):
        """
        @return list of data file
        """
        list_rows = []
        if self.image():#TODO creare decorator
            list_rows.append( "{0}\n".format ( LabelImage().csv() ) ) 
        else:
            list_rows.append( "{0}\n".format ( LabelVideo().csv() ) ) 
        for tmp_file in self.list_data:
            if self.image():
                tmp_value = CSVImage(self.properties_ini, tmp_file)
                list_rows.append( "{0}\n".format ( tmp_value.data())) #TODO centralize
            else:
                tmp_value = CSVVideo(self.properties_ini, tmp_file)
                list_rows.append( "{0}\n".format ( tmp_value.data())) #TODO centralize
        self.logging.print( "Elaborated: %s rows" % str ( len ( list_rows ) ) )
        return self.safefile.safe(list_rows)
        
    def image(self):
        """
        @return True if the row is about an image, False if it's abouta a video
        """
        return self.properties_ini.imagetype() == "photo" #TODO create decorator


