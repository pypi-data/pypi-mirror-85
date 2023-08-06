#!/usr/bin/env python3


"""Test case implementation"""


import datetime




class TestCase(object):
    """A class whose instances are single test cases.
    that hold all information about a test case like name, description
    and steps count, details 
    and statistics like totla pass, fail and error steps
    """

    def __init__(self, testMmethodName='runTest',testCaseDescription='desc'):        
        self.methodName = testMmethodName
        self.description = testCaseDescription        
        self.success_count = 0
        self.failure_count = 0
        self.error_count = 0        
        # steps is a list of result in 4 tuple
        # (
        #   step type code (0: success; 1: fail; 2: error, 3: info),
        #   timestamp time,
        #   step details string,
        #   sceenchoot string path,
        # )
        self.steps = []
        self.steps_count = 0

    def addInfoStep(self, details):
        self.success_count += 1
        self.steps_count += 1
        tiemStamp = str(datetime.datetime.now().time()).split('.')[0]  
        self.steps.append((3,tiemStamp,details,''))

    def addPassStep(self, details,screenshot=''):
        self.success_count += 1
        self.steps_count += 1
        tiemStamp = str(datetime.datetime.now().time()).split('.')[0]
        self.steps.append((0,tiemStamp,details,screenshot))

    def addFailStep(self, details, screenshot=''):
        self.failure_count += 1
        self.steps_count += 1
        tiemStamp = str(datetime.datetime.now().time()).split('.')[0]
        self.steps.append((1,tiemStamp,details,screenshot))

    def addErrorStep(self, details,screenshot=''):
        self.error_count += 1
        self.steps_count += 1        
        tiemStamp = str(datetime.datetime.now().time()).split('.')[0]
        self.steps.append((2,tiemStamp,details,screenshot))

    def shortDescription(self):
        doc = self.description
        return doc and doc.split("\n")[0].strip() or None


    def id(self):
        return  self.methodName

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented

        return self.methodName == other.methodName

    def __hash__(self):
        return hash((type(self), self.methodName))

    def __str__(self):
        return "(%s)" % (self.methodName)

    def __repr__(self):
        return "<testMethod=%s>" % \
               (self.methodName)

    
    

   