import os
from .personal_logging import PersonalLogging

class AbsolutePath:
    '''@overview: leggo il path assoluto del file passato'''

    def __init__(self, newrelativepath):
        self.relativepath = newrelativepath
        self.logging = PersonalLogging("AbsolutePath", True)

    def absolute(self):
        return os.path.abspath(self.relativepath)


