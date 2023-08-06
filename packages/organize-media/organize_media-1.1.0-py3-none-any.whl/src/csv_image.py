from .csv_image_name import FailFirst 
from .csv_image_name import Name

from .personal_logging import PersonalLogging

from tests.test_day_month_year import DayMonthYear 
from tests.test_day_month_year import Space
from tests.test_day_month_year import Slash
from tests.test_quotation_mark import QuotationMark




class CSVImage:
    '''@overview: class that format the rows of the data'''
    def __init__(self, newini, newcsv):
        self.log = PersonalLogging("CSVImage")
        self.ini = newini
        self.manualcsv = newcsv
        self.staticcsv = CSVImageStatic()

    
    def data(self):
        '''@return list fo the row to be printed'''
        result = []
        result.append( self.manualcsv.fileName() )#filename 
        result.append( self.ini.copyright() )  #copyright
        result.append( self.ini.price() )#price
        created = DayMonthYear ( self.manualcsv.day(), self.manualcsv.month(), self.manualcsv.year())
        
        result.append( self.name(created) ) #name
        result.append( self.ini.city() ) #city
        result.append( self.ini.region() ) #Region
        result.append( self.ini.country() ) #Country

        result.append( Slash(created).show()  ) #Created
        
        result.append( self.ini.specifysource() ) #specififedsource
        result.append( self.manualcsv.keywords() )#keyword 
        result.append( self.staticcsv.keywordsCheckbox() )#keywordsCheckbox
        result.append( self.staticcsv.publicBin() )#publicbin

        result.append( QuotationMark(self.manualcsv.description()).string() ) #description
        
        result.append( self.ini.imagetype()  )#imagetype
        return ",".join(result)

    def name(self, created):
        '''@return name as concatenation fo Description, date creation , city, country'''
        return FailFirst ( Name ( self.ini, self.manualcsv, created) ) .string()

    def __str__(self):
        return "CSVImage:[{0}]".format(self.ini)

    def __repr__(self):
        return "[{0}]".format(self.data())


class CSVImageStatic:
    '''@overview: static value of a image in row CSV
    '''
    def __init__(self):
        pass #TODO put the value inside, as CSVVideoStatic

    def keywordsCheckbox(self):
        '''@return list of static values'''
        return " " #"keywordscheckbox-static" #TODO delete

    def publicBin(self):
        return " "# "publicBin-static" #TODO delete

