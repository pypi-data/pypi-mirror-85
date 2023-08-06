import os
from .original_file import OriginalFile
from .absolute_path import AbsolutePath
from .personal_logging import PersonalLogging
from tests.test_extension import Extension
from tests.test_position import Position

class GroupReadFiles:
    """
    @overview: classe che riceve i file letti e li trasforma in OriginalFiles
    """

    def __init__(self, new_list_readfiles):
        self.list_readfiles = new_list_readfiles
        self.logging = PersonalLogging("GroupReadFiles", False)

    def map(self):
        """
        @return la mappa tra percorso assoluto del file letto e la class originalFile
        """
        result = {}
        for filetmp in self.list_readfiles:
            self.logging.print("filetmp: " + str(filetmp))
            path = AbsolutePath(filetmp).absolute()
            tail, head = os.path.split(filetmp)
            if Position(tail, head).extension().media():
                result[filetmp]= OriginalFile(tail, head)
            else:
                self.logging.warn("Il file [" + head + "] non verra processato")
        return result


