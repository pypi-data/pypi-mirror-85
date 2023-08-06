import os
from .personal_logging import PersonalLogging
from tests.test_extension import Extension
from tests.test_quotation_mark import QuotationMark

class ReadFileINI:
    '''@overview: it contains the properties in file INI'''

    def __init__(self, new_dir):
        self.dir = new_dir
        self.log = PersonalLogging("ReadINI")

    def read(self):
        '''@return the object with the properties'''
        try:
            from configparser import ConfigParser
        except ImportError:
            from ConfigParser import ConfigParser  # ver. < 3.0
        config = ConfigParser()
        path =  self.dir + os.sep + "common.ini" #TODO concatenation of string to improve
        exists = os.path.exists(path)
        if exists : #TODO decorator
            config.read(path)
            #TODO centralize in an object
            path = self.dir.split ( os.sep )
            path.reverse()
            extension = Extension ( path[0] )#TODO put control if the path finish in \ or \\, if it raise exception
            
            file_ini = ReadFileINI(self.dir)
            if extension.image(): #TODO: create decorator and class
                self.log.print("I will writing a images file ")
                file_ini = Image ( ReadINI ( config ) ) 
            elif extension.video(): #TODO decorator
                self.log.print("I will writing a video file")
                file_ini = Video ( ReadINI ( config ) ) 
            else:
                raise Exception ("Unkown type of file:{0}".format(extension) ) 
        else:
            raise Exception ( "The file [{0}] is not present, I stop the elaboration".format(path) )
        return file_ini

    def __str__(self):
        return "ReadFileINI:{0}".format ( str ( self.dir) )

    def __repr__(self):
        return "ReadFileINI:{0}".format ( str ( self.dir) )


class Image:
    '''@overview: this class contains the configuration about the images'''
    def __init__(self, new_read_ini):
        self.name = 'Image'
        self.read = new_read_ini

    def copyright(self):
        return  QuotationMark( self.read.copyright(self.name) ).string()

    def city(self):
        return self.read.city(self.name)
    
    def price(self):
        return self.read.price(self.name)
    
    def specifysource(self):
        return QuotationMark ( self.read.specifysource(self.name) ).string()
    
    def region(self):
        return self.read.region(self.name)
    
    def imagetype(self):
        return 'photo'

    def country(self):
        return self.read.country(self.name)
   
    def __str__(self):
       return "Image:{0};{1}".format(self.name, self.read )
    
    def __repr__(self):
       return "Image:{0};{1}".format(self.name, self.read )

class Video:
    '''@overview: this class contains the configuration about the videos'''
    def __init__(self, new_read_ini):
        self.name = 'Video'
        self.read = new_read_ini

    def copyright(self):
        return QuotationMark( self.read.copyright(self.name) ).string()

    def city(self):
        return self.read.city(self.name)
    
    def price(self):
        return self.read.price(self.name)
    
    def specifysource(self):
        return QuotationMark ( self.read.specifysource(self.name) ).string()
    
    def region(self):
        return self.read.region(self.name)
    
    def imagetype(self):
        return 'video'

    def country(self):
        return self.read.country(self.name)


    def __str__(self):
       return "organizemedia.Video:[{0}]".format(self.name)
    
    def __repr__(self):
       return "organizemedia.Video:[{0}]".format(self.name)


class ReadINI:
    '''@overview: this class contains the configuration'''
    def __init__(self, new_config ):
        self.config = new_config

    def copyright(self, name):
        return self.config.get(name, 'Copyright' )
    
    def city(self, name):
        return self.config.get(name,'City')
    
    def price(self, name):
        return self.config.get(name, 'Price')
    
    def specifysource(self, name):
        return self.config.get(name,'SpecifySource')
    
    def region(self, name):
        return self.config.get(name,'Region')
    
    def imagetype(self, name):
        return self.config.get(name,'ImageType')

    def country(self, name ):
        return self.config.get(name,'Country')
   
    def __repr__(self):
       return "ReadINI:[{0}]".format(self.config)

    def __str__(self):
       return "ReadINI:[{0}]".format(self.config )
