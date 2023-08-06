import sys
import os

from tests.test_single_file import SingleFile
from .rootpath import Rootpath
from .report_file import RowCSV
from .report_file import RowDuplicated


class Report:
    """
    @overview: this class print the report of a list of files in CSV format 
    """

    def __init__(self, new_report_name):
        self.name = new_report_name

    def homonym(self):
        if os.path.exists( self.name ) :
            os.remove( self.name )
        else:
            pass

    def write(self, list_files):
        """
            It read a directory recursavely
            ----------
            Returns
            -------
            nil
        """
        try:
            self.homonym()
            report = open(self.name, "w")#TODO using decorator
            report.write(self.csvLabel())
            self.writerows( list_files, report)
            report.close()
        except:
            print (  sys.exc_info()  )
        print ("The file {0} is finally written".format ( self.name)  )


    def csvLabel(self):
        '''@return the summary of CSV file'''
        return "NAME;DIRECTORY;WEIGTH;TIMESTAMP\n"

    def writerows (self, readfiles, report):
        """
            It writes the elements of list of file in target file
            ----------
            readfiles: list    list of SingleFile in csv form
            report: file        final file of report
        """
        for fileToWrite in readfiles:
            report.write( RowCSV( fileToWrite ).data())
        self.end(readfiles)

    def end(self, readfiles):
        print("All the {0} rows have been written".format ( len(readfiles) ) )


    def __repr__(self):
        return "Report.repr:{0}".format( self.name )

    def __str__(self):
        return "Report:{0}:".format( self.name )

class MapReport:
    """@overview: this class print the report of a list of files in CSV format 
    """

    def __init__(self, new_origin):
        self.origin  = new_origin

    def homonym(self):
        self.origin.homonym()

    def write(self, map_files):
        """
            It read a directory recursavely
            ----------
            Returns nil
            -------    
        """
        try:
            self.homonym()
            report = open(self.origin.name, "w")
            self.writerows( map_files, report)
            report.close()
        except:
            print (  sys.exc_info()  )
        print ("The file {0} is finally written".format ( self.origin.name)  )


    def csvLabel(self):
        '''@return the summary of CSV file'''
        return "PATH;SIZE;TIMESTAMP\n"

    def writerows (self, readfiles, report):
        """
            It writes the elements of list of file in target file
            ----------
            readfiles: list    list of SingleFile in csv form
            report: file        final file of report
        """
        for fileToWrite in readfiles.keys():
            report.write ("\n******File {0}-REMEMBER TO LEAVE ONE OCCURRENCE\n".format( fileToWrite ))
            report.write(self.csvLabel())
            #if 1<len( readfiles[fileToWrite]) 
            for fileDuplicated in readfiles[fileToWrite]:
                report.write( RowDuplicated( RowCSV( fileDuplicated ) ).data())
        print("Written data")
        self.origin.end(readfiles.keys())

    def __repr__(self):
        return "MapReport.repr:{0}".format( str( self.origin) )

    def __str__(self):
        return "MapReport:{0}:".format( str( self.origin) )

