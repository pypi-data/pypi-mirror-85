
from sys import setprofile
from Octopus.OctopusHTMLReport.OctopusTestResult import TestResult
from Octopus.OctopusHTMLReport.OctopusHTMLTestReport import HTMLTestReport
from Octopus.OctopusCore.globals import Globals
import datetime
import os
import sys
from enum import Enum


class Status(Enum):
    PASS = 'PASS'
    FAIL = 'FAIL'
    FATAL = 'FATAL'
    ERROR = 'ERROR'
    WARNING = 'WARNING'
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    SKIP = 'SKIP'


class Reporter (object):
    _testResult = None
    _htmlReport = None
    _reportFile = None

    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance        
        if Reporter._testResult is None:
            # Create and remember instance
            Reporter._testResult = TestResult()
            # Store instance reference as the only member in the handle
            self.__dict__['_Reporter__Result'] = Reporter._testResult
    
        if Reporter._htmlReport is None:
            # Create and remember instance
            Reporter._htmlReport = TestResult()
            # Store instance reference as the only member in the handle
            self.__dict__['_Reporter__htmlReport'] = Reporter._htmlReport


        if Reporter._reportFile is None:
            # Create and remember instance
            Reporter._reportFile = TestResult()
            # Store instance reference as the only member in the handle
            self.__dict__['_Reporter__reportFile'] = Reporter._reportFile
    

    @staticmethod
    def openReport( sReportPath, sProjectName):
        try:
            Reporter._testResult = TestResult()
            Reporter._reportFile = open(sReportPath, 'wb')
            Reporter._htmlReport = HTMLTestReport(stream=Reporter._reportFile,
                                              title=sProjectName,
                                              description='Octopus HTML Test Report : {0}'.format(sProjectName))
        except:
            print("\t\t[ERROR]  opening HTML Report File : {0}".format(
                sys.exc_info()[1]))

    @staticmethod
    def writeReport():
        try:
            Reporter._htmlReport.generateReport(Reporter._testResult)
        except:
            print("\t\t[ERROR]  Writing HTML Report File : {0}".format(
                sys.exc_info()[1]))
        finally:
            print('\n\n=============================================================')
            print('Total tests run: {0}, Failures: {1}, Errors: {2}, Passed: {3}'.format(Reporter._testResult.testsRun, \
                    Reporter._testResult.failure_count,Reporter._testResult.error_count,Reporter._testResult.success_count))
            print('\nTime Elapsed: {0}'.format( (Reporter._htmlReport.stopTime-Reporter._htmlReport.startTime) + datetime.timedelta(0, 1)))
            print('=============================================================\n') 
            Reporter._reportFile.close()

    @staticmethod
    def getBrowserImage(Browser,imgPath):
        _imgPath = ""
        try:
            if Browser != None:
                Browser.save_screenshot(imgPath)
                _imgPath = imgPath
        except:
            print("\t\t[Failed]  Take a screen shoot : {0}".format(
                sys.exc_info()[1]))
        finally:
            return _imgPath
    
    @staticmethod
    def saveScreenShot():
        imgPath=""
        try:
            if Globals.Test.Browser != None:
                Globals.Report.ScreenCaptureCount+=1
                imgPath=Globals.Report.ScreenShootFolder+"\\Img_"+str(Globals.Report.ScreenCaptureCount)+".png"
                Globals.Test.Browser.save_screenshot(imgPath)
                imgPath = Globals.Report.ScreenShootHTMLPath+"\\Img_"+str(Globals.Report.ScreenCaptureCount)+".png"
        except:
            print("\t\t[Failed]  Take a screen shoot : {0}".format(sys.exc_info()[1]))
        finally:
            return imgPath

    @staticmethod
    def log( status, details):
        try:

            if(None == details):
                details = ""

            if (("<html" in details or "<HTML" in details or "</" in details) and (details.strip().endswith(">"))):
                details = "<textarea readonly style=\"height:150px\">" + details + "</textarea>"

            if(status is Status.FAIL):
                print("\t\t[ {0} ]  {1} .".format(Status.FAIL.value, details))
                imgPath = Reporter.saveScreenShot()
                Reporter._testResult.addFailure(details, imgPath)
            elif(status is Status.ERROR):
                imgPath = Reporter.saveScreenShot()
                print("\t\t[ {0} ]  {1} .".format(Status.ERROR.value, details))
                Reporter._testResult.addError(details, imgPath)
            elif(status is Status.PASS):
                imgPath = Reporter.saveScreenShot()
                print("\t\t[ {0} ]  {1} .".format(Status.PASS.value, details))
                Reporter._testResult.addSuccess(details, imgPath)
            else:
                print("\t\t[ {0} ]  {1} .".format(Status.INFO.value, details))
                Reporter._testResult.addInfo(details)

        except Exception:
            print("Reporter Log Function Failed. {0}".format(
                sys.exc_info()[1]))
            Reporter._testResult.addError(sys.exc_info()[1], '')

    @staticmethod
    def startTest( sTestCaseName):
        try:
            print(
                "\n\n_________ Start Test Case [ " + sTestCaseName + " ] _________")
            Reporter._testResult.startTest(sTestCaseName)
        except:
            print("\t\t[Failed]  Starting New Test : {0}".format(
                sys.exc_info()[1]))

    @staticmethod
    def stopTest():
        try:
            print("\n_________ End Test Case _________")
            Reporter._testResult.stopTest()
        except:
            print("\t\t[Failed]  Ending Test : {0}".format(sys.exc_info()[1]))

    @staticmethod
    def info( details):
        Reporter.log(Status.INFO, details)

    @staticmethod
    def passed( details):
        Reporter.log(Status.PASS, details)

    @staticmethod
    def failed( details):
        Reporter.log(Status.FAIL, details)

    @staticmethod
    def error( details):
        Reporter.log(Status.ERROR, details)

