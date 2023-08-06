import sys
import os

from .file_system import FileSystem
from .personal_logging import PersonalLogging
from .group_original_files import GroupOriginalFiles
from .group_read_files import GroupReadFiles
from .group_files import GroupFiles
from .group_directory import GroupDirectory
from .safe_file import SafeFile
from .file_to_write import FileToWrite

class Copy:
    '''@overview: class to copy file'''
    def __init__(self, args):
        self.source = args[0]
        self.dest = args[1]

    def __repr__(self):
        return 'Copy(source = %s, dest = %s )' % (self.source, self.dest)

    def __str__(self):
        return "Copy(%s,%s)" % (self.source, self.dest)

    def __eq__(self, other):
        return self.source == other.source and self.dest == other.dest

    def run(self):
        '''the copy of the files '''
        begin = FileSystem(self.source).walk()
        map_original_files = GroupReadFiles(begin).map()
        group_original_files = GroupOriginalFiles(map_original_files)
        group_final_files = group_original_files.map( self.dest )
        GroupDirectory(group_final_files.values()).write()
        group_files = GroupFiles(group_final_files)
        group_files.copy()

