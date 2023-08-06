import os
import unittest
from os.path import splitext

from list_files.physical_data import PhysicalData
from list_files.physical_data import PhysicalDataFake


class Filename:
    """
    class about the filename of a file
    """
    def __init__(self, new_physical):
        self.physical = new_physical
    
    def name(self): 
        """
        @return the name of a file, with extension
        """
        #print("Filename.name")
        list_subdirectory = self.prepare()
        return list_subdirectory[0]

    def __hash__(self):
        return hash(self.physical)    

    def extension(self):
        """
        @return the extension of a file
        """
        return self.prepare()[1]

    def prepare(self):
        """
        @return the couple <name, extension> of a file
        """
        list_subdirectory = self.physical.path().split(os.sep)
        list_subdirectory.reverse()
        #print("Filename.prepare len:{0}".format ( len ( str ( list_subdirectory )  ) ) )
        #print("Filename.prepare:{0}".format ( str ( list_subdirectory )  ) )
        #if not "." in list_subdirectory[0]:#TODO move in a defensive decorator
            #raise Exception ("The first element of the list {0} lacks of the dot, please control".format( str(list_subdirectory[0] ) ) )
            #print ("The first element of the list {0} lacks of the dot, please control".format( str(list_subdirectory[0] ) ) )
        result = SeparationDirectory ( list_subdirectory).split()
        if "" == result:
            resul="EMPTY-FILE-#TODO-DONT-PUT-IN-LIST"
        return result 

    def __lt__(self, other):
        return self.name() < other.name()

    def __eq__(self, other):
        return self.name() == self.name() and self.extension() == self.extension()

    def __repr__(self):
        return "Filename.repr:{0}.{1}".format(self.name(), self.extension())

    def __str__(self):
        return "Filename:{0}.{1}".format(self.name(), self.extension())

class SeparationDirectory:
    """
    clsss about the separation of a directory in subdirectory
    """

    def __init__(self, new_list_subdirectory):
        self.list_subdirectory = new_list_subdirectory

    def split(self):
        result = None
        try:
            result = self.subdir().split(".")
        except IndexError:
            print ("SeparationDirectory.split() split dot: {0}".format( str ( self.subdir() ) ))
            raise
        return result

    def subdir(self):
        directory = None
        try:
            directory = self.list_subdirectory[0]
        except IndexError:
            print ("SeparationDirectory.split() access first element: {0}".format( str ( self.list_subdirectory) ) )
            raise
        return directory

    def __repr__(self):
        return "SeparationDirectory.repr:{0}".format(str ( self.list_subdirectory))

    def __str__(self):
        return "SeparationDirectory:{0}".format( str ( self.list_subdirectory))  
        
"""
Test area
"""
def test_eq():
    one = Filename ( PhysicalDataFake( "nome1.txt", "C:\\path\\") )
    two = Filename ( PhysicalDataFake( "nome1.txt", "C:\\path\\") )
    assert one == two

def test_not_eq():
    one = Filename ( PhysicalDataFake( "nome3.txt", "C:\\path\\") )
    two = Filename ( PhysicalDataFake( "nome4.txt", "C:\\path\\") )
    assert (one ==  two)

def test_separationDirectory_split():
    list_dir = ['.travis.yml', 'jcabi-dynamo', 'mio-java', 'personale', 'Documents', 'apuzielli', 'Users', 'C:']
    result = SeparationDirectory(list_dir).split()
    assert result == ['','travis','yml']

def test_separationDirectory_subdir():
    list_dir = ['.travis.yml', 'jcabi-dynamo', 'mio-java', 'personale', 'Documents', 'apuzielli', 'Users', 'C:']
    result = SeparationDirectory(list_dir).subdir()
    assert result == ".travis.yml"
        

