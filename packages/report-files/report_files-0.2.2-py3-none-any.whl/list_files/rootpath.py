import sys
import os
from tests.test_single_file import PhysicalData
from tests.test_single_file import SingleFile
import pytest

class Rootpath:
    """
    @overvieww: class of the absolute path of root directory
    """
    def __init__(self, opts):
        self.rootpath = opts[1] #TODO study how to resolve the constants in Python

    def data(self):
        return str(self.rootpath )

    def exists(self):
        return os.path.exists(self.data())

    def files ( self ): #TODO move in class Rootpath
        """
        It read a directory recursavely
        """
        readfiles = []
        try:
            self.subdir(self.data(), readfiles)
        except:
            print ( sys.exc_info() )
        print ( "The total number of the read files is {0}".format ( str( len ( readfiles )  ) ) )
        return readfiles;


    def subdir(self, root_path,  readfiles ):
        """
            It traverses root directory, and list directories as dirs and files as files
            ----------
            root_path: string    root of the path
            readfiles: list            list of read files inside path
        """
        for root, dirs, files in os.walk(root_path) :
            path = root.split(os.sep)
            for fileTmp in files:
                readfiles.append ( SingleFile (  PhysicalData ( fileTmp, os.sep.join ( path ) ) ) ) 
            for directory in dirs:
                self.subdir(directory, readfiles)

    def __repr__(self):
        return "Rootpath.repr:{0}".format( str ( self.rootpath) )

    def __str__(self):
        #return "{0}".format( str ( self.rootpath) )
        return "Rootpath:{0}".format( str ( self.rootpath) )


class OnlyVisible(Rootpath):
    """
    It reads only visible directory
    """
    def __init__(self, new_rootpath):
        self.rootpath = new_rootpath

    def data(self):
        return self.rootpath.data()

    def exists(self):
        return super().exists()

    def files ( self ): #TODO move in class Rootpath
        readfiles = []
        try:
            if ( self.exists() ):
                readfiles = self.rootpath.files()
            else:
                print ( "The directory [{0}] doesn'nt exists".format ( self.data() ) )  
        except:
            print ( sys.exc_info() )
        return readfiles;


    def subdir(self, root_path,  readfiles ):
        if "\\." in root_path :
            print ("Directory with dot (.), then it's hidden: {0}".format  ( directory )) 
        else:
            return self.rootpath.subdir(root_path, readfiles)
            
    def __repr__(self):
        return "OnlyVisible.repr:{0}".format( str ( self.rootpath) )

    def __str__(self):
        return "OnlyVisible:{0}".format( str ( self.rootpath) )


def test_dot_in_path():
    path = "C:\\Users\\apuzielli\\Documents\\personale\\mio-github\\.metadata\\.plugins\\org.jboss.tools.central\\proxyWizards\\1596464026525\\.rcache\\.orphans"
    result = ( "."  in path)
    assert True == result
