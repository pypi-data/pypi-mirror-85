#!/usr/bin/env python3


"""Test result object"""



from Octopus.OctopusHTMLReport.OctopusTestCase import TestCase




class TestResult(object):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.

    def __init__(self):        
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0
        self.testsRun = 0
        self._TestCase = None
        

        # result is a list of result in 4 tuple
        # (
        #   result code (0: success; 1: fail; 2: error),
        #   TestCase object,
        # )
        self.result = []

    def startTest(self, testMethodName='testMethod'):
        self._TestCase = TestCase(testMethodName)
        self.testsRun += 1
        

    def stopTest(self):
        _status = 0        
        if self._TestCase.error_count > 0:
            self.error_count += 1
            _status = 2
        elif self._TestCase.failure_count > 0:
            self.failure_count += 1            
            _status = 1
        else:
            self.success_count += 1
            _status = 0
        self.result.append((_status,self._TestCase))
        self._TestCase = None
        
    def addSuccess(self, testDetails,screenShot):
        self._TestCase.addPassStep( testDetails,screenShot)        

    def addError(self, testDetails,screenShot):        
        self._TestCase.addErrorStep(testDetails,screenShot)
       
    def addFailure(self, testDetails,screenShot):        
        self._TestCase.addFailStep(testDetails,screenShot)
        

    def addInfo(self, testDetails):        
        self._TestCase.addInfoStep(testDetails)
       
