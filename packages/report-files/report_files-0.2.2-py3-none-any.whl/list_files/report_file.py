import os
import datetime
import unittest

from tests.test_single_file import SingleFile

class RowCSV:
    '''@overview: class that manage the data as CSV row'''
    def __init__(self, new_single_file):
        self.single_file = new_single_file

    def data(self):#TODO what is annotation @property
        name_extension = FilenameExtension( self.single_file).filename()  
        filename = None
        try:
            filename = ";".join ( ( self.single_file.directory(), name_extension ) ) 
        except:
            print("Error1")
        return self.csv(filename)

    def time(self):
        return datetime.datetime.fromtimestamp ( float(self.single_file.timestamp () ) ).strftime( "%Y-%m-%d-%H-%M" ) #TODO class ad-hoc
        
    def csv(self, filename):
        data = None
        try:
            data  = (filename , str( self.single_file.dimension () ), self.time(), "\n")
        except:
            print("error2")
        return ";".join ( data ) #TODO move in a decorator

    def __repr__(self):
        return "RowCSV.repr:{0}".format( str ( self.single_file)  )

    def __str__(self):
        return "RowCSV:{0}}".format( str ( self.single_file)  )

        
class RowDuplicated:

    def __init__(self, new_origin):
        self.origin = new_origin

    def data(self):
        name_extension = FilenameExtension(  self.origin.single_file ).filename()  #TODO centralize
        filename = "{0}{1}{2}".format(self.origin.single_file.directory(), os.sep, name_extension ) 
        return self.origin.csv( filename )

    def __repr__(self):
        return "RowDuplicated.repr:{0}".format( str ( self.origin)  )

    def __str__(self):
        return "RowDuplicated:{0}}".format( str ( self.origin)  )

class FilenameExtension:

    def __init__(self, new_single_file):
        self.single_file = new_single_file

    def filename(self):
        name_extension = ".".join ( ( self.single_file.name().name() , self.single_file.name().extension() )  )
        return name_extension

