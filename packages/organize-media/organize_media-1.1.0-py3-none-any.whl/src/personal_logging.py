class PersonalLogging:
    '''@overview this class is a personal logging class'''
    def __init__( self, new_class, new_activation  = True):
        self.src = new_class
        self.activation = new_activation

   
    def print( self, data ):
        '''print the data in console'''
        msg = ""
        if( self.activation ):
            #TODO correct concatenation string
            msg = (self.src + ">" + data)
            print( msg )
        else:
            msg = ""
        return msg


    def warn( self, data ):
        '''print the warning data in console'''
        msg = ""
        if( self.activation ):
            #TODO correct concatenation string
            msg = (">WARN: " + data)
        else:
            msg = ""
        return self.print(msg)
