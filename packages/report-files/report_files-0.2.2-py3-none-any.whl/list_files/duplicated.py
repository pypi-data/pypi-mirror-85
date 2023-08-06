from tests.test_single_file import SingleFile
from tests.test_duplicated_files import Occurrence

class Duplicated:
    """
    @overview: class with the list of files and the occurrences of the homonym files
    """

    def __init__(self, newListFiles):
        self.listFiles = newListFiles

    def files(self):
        """
        @return the map<SingleFile, list_of_files_duplicated_with_same_filename>
        """
        mapFiles =  {}
        for fileTmp in self.listFiles:
            mapFiles[fileTmp] = fileTmp.name().name() 
        duplicated = {}
        for filenameTmp in set(mapFiles.values()) : #TODO translate in functional programming with lambda syntax
            numberOccurrences = Occurrence (mapFiles, filenameTmp ) 
            if numberOccurrences.excessive(): 
                duplicated [filenameTmp] = numberOccurrences.list_files()
        #at the end of the cycle
        return duplicated

    def __repr__(self):
        return "Duplicated.repr:{0}".format( str ( self.listFiles) )

    def __str__(self):
        return "Duplicated:{0}:{0}".format( str ( self.listFiles) )
