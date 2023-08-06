from .file_to_write import FileToWrite
from .personal_logging import PersonalLogging
from .safe_file import SafeFile

class DataINI:
    '''
    @class for the initial ini file of properties
    '''
    
    def __init__(self, new_safe_file):
        self.safefile = new_safe_file
        self.logging = PersonalLogging("DataINI")

    def data(self, list_rows):
        '''
        @return list of the field
        '''
        list_rows.append("Copyright=\n")
        list_rows.append("City=\n")#TODO in function of the topic
        list_rows.append("Price=\n")
        list_rows.append("SpecifySource=\n")
        list_rows.append("Region=\n")
        list_rows.append("Country=\n")
        return self.safefile.safe(list_rows)

    def __str__(self):
        return "DataINI:{0}".format( str ( self.safefile) )

    def __repr__(self):
        return "DataINI:{0}".format( str ( self.safefile) )

class Image:
    '''
    @overview: label about the image INI file
    '''
    def __init__(self, new_data_ini):
        self.data_ini = new_data_ini
        self.loggging = PersonalLogging("Image")

    def data(self):
        list_rows = []
        list_rows.append("[Image]\n")
        list_rows.append("ImageType=photo\n")
        return self.data_ini.data(list_rows)


    def __str__(self):
        return "Image:{0}".format( str ( self.data_ini) )

    def __repr__(self):
        return "Image:{0}".format( str ( self.data_ini) )


class Video:
    '''
    @overview: labels about the video INI file
    '''

    def __init__(self, new_data_ini):
        self.data_ini = new_data_ini
        self.loggging = PersonalLogging("Video")

    def data(self):
        list_rows = []
        list_rows.append("[Video]\n")
        list_rows.append("ImageType=video\n")
        return self.data_ini.data(list_rows)
    
    def __str__(self):
        return "Video:{0}".format( str ( self.data_ini) )

    def __repr__(self):
        return "Video:{0}".format( str ( self.data_ini) )

class DataDraft:
    '''
    @class for the initial draft file about the tags
    '''
    def __init__(self, new_safe_file):
        self.safefile = new_safe_file
        self.logging = PersonalLogging("DataDraft", True)

    def data(self, map_original_files):
        '''
        @return list of the files and the field s
        '''
        list_rows = []
        self.logging.print("data")
        list_rows.append("Filename, tags to put\n")
        for tmp_file in map_original_files.keys(): #TODO centralize in a class
            tmp_value = map_original_files[tmp_file]
            list_rows.append( "%s,\n" % ( tmp_value ) )

        return self.safefile.safe(list_rows)

    def __str__(self):
        return "DataDraft:{0}".format( str ( self.safefile ) )

    def __repr__(self):
        return "DataDraft:{0}".format( str ( self.safeilfile ) )

