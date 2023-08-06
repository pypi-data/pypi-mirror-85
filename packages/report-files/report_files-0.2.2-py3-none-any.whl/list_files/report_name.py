import datetime

class ReportName:

    def __init__(self):
        self.extension = "csv"
        self.DATE_FORMAT="%Y-%m-%d"

    def unique(self):
        '''@return the name of final report file of the files (once written)'''
        return "report-unique-{0}.{1}".format( self.time(), self.extension )#TODO crete class decorator

    def duplicated(self):
        '''@return the name of final report file of the duplicated files'''
        return "report-duplicated-{0}.{1}".format( self.time(), self.extension )#TODO crete class decorator

    def all(self):
        '''@return the name of final report file'''
        return "report-all-{0}.{1}".format( self.time(), self.extension )#TODO crete class decorator

    def time(self):
        return  datetime.datetime.now().strftime(self.DATE_FORMAT)#TODO class ad hoc
        
    def __repr__(self):
        return "ReportName.repr:{0};{1}".format( self.extension , self.DATE_FORMAT )

    def __str__(self):
        return "ReportName:{0};{1}".format( self.extension , self.DATE_FORMAT )

