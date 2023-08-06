import os
from os.path import splitext
import unittest


class PhysicalData:

    def __init__(self, new_current, new_directory):
        self.directory = new_directory
        self.currentfile = new_current 
    
    def data(self): 
        path = self.path()
        filetmp  = open( path, 'r' );
        statinfo = os.stat( path )
        filetmp.close()
        return statinfo

    def path(self):
        return "{0}{1}{2}".format( self.directory , os.sep ,self.currentfile )

    def __hash__(self):
        return hash(self.directory) * 10 + hash (self.currentfile)

    def __repr__(self):
        return "PhysicalData.repr:{0};{1}".format( self.directory , self.currentfile)

    def __str__(self):
        return "PhysicalData:{0};{1}".format( self.directory , self.currentfile)

class PhysicalDataFake:

    def __init__(self, new_current, new_directory):
        self.name = new_current
        self.directory = new_directory

    def data(self): 
        return DataFake() 

    def path(self):
        return "{0}_fake/{1}".format(self.directory, self.name )

    def __repr__(self):
        return "PhysicalDataFake:{0}-{1}".format(self.name, self.directory)
    
    def __str__(self):
        return "PhysicalDataFake:{0}-{1};{2}".format(self.directory, self.name, self.data())

    def __repr__(self):
        return "PhysicalDataFake.repr:{0};{1}".format( self.name , self.directory)

    def __str__(self):
        return "PhysicalDataFake:{0};{1}".format( self.name , self.directory)

class DataFake:

    def __init__(self):
        pass

    def st_mode(self):
        return 33206

    def st_ino(self):
        return 15199648742420042

    def st_dev(self):
        return 1658795973

    def st_nlink(self):
        return 1

    def st_uid(self):
        return 2

    def st_gid(self):
        return 3

    def st_size(self):
        return 4
    
    def st_atime(self):
        return 1599579491

    def st_mtime(self):
        return 1599579492

    def st_ctime(self):
        return 1599579493
    
    def __repr__(self):
        return "DataFake-static-data"

    def __str__(self):
        return "DataFake-static-data"


