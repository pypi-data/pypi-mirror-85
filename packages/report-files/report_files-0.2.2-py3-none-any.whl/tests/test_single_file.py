import os
import unittest
from os.path import splitext

from list_files.physical_data import PhysicalData
from list_files.physical_data import PhysicalDataFake
from .test_filename import Filename

class SingleFile:

    def __init__(self, new_physical_data):
        self.physical = new_physical_data
        self.filename = Filename(new_physical_data)

    def directory(self):
        """
        @return the path of the file
        """
        dirs = self.physical.path().split(os.sep)
        #print(">SingleFile.directory")
        value =  str( os.sep.join(dirs[0:len(dirs) -1 ] ) )
        #print("<SingleFile.directory")
        return value

    def dimension(self):
        """
        @return the number of bytes of the file
        """
        return self.physical.data().st_size

    def timestamp(self):
        """
        @return the timestamp of the last modifiy or creation of the file
        """
        return self.physical.data().st_atime
    
    def name(self):
        """
        @return the name of the file
        """
        return self.filename
    
    def __iter__(self):
        return iter(self.name)

    def __lt__(self, other):
        return len(self.filename) > len(other.filename)

    def __eq__(self, other):
        return self.name().name() == other.name().name() and self.dimension() == other.dimension()

    def __hash__(self):
        return hash(self.filename)

    def __str__(self):
        return "SingleFile:{0};{1}-{2}".format ( self.name().name(), self.name().extension(), str(self.dimension()) )

    def __repr__(self):
        return "SingleFile:{0};{1}".format (self.physical, self.filename)


def test_eq():
    one = SingleFile ( PhysicalDataFake( "nome.txt", "C:\\path\\") )
    two = SingleFile ( PhysicalDataFake( "nome.txt", "C:\\path\\") )
    print (one) 
    print (two)
    assert(one.name() == two.name())

def test_not_eq():
    one = SingleFile ( PhysicalDataFake( "nome.txt", "C:\\path\\") )
    two = SingleFile ( PhysicalDataFake( "nome1.txt", "C:\\path\\") )
    assert(one != two)


