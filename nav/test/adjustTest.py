"""
    Created on February 14, 2019
    adjustTest - Test file for the adjust function.
    @author: Christopher Tillery (cat0050)
"""

import unittest
import nav.adjust as nav

class adjustTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
# Analysis
#    adjust(values)
#    Level: BVA
#
#    input:
#        values:     a dictionary of inputs with the possibility of containing an observation, height,
#                    pressure, horizon, and temperature; arrives unvalidated
#    output:
#        returns:    an updated dictionary according to the calculations within adjust with the possibility
#                    of containing an error key
#                    Dictionary element    Range
#                           observation    xx(>=0 and <90) + 'd' + yy(>=0 and <60)
#                                height    >=0
#                              pressure    >=100 and <=1100
#                               horizon    artificial or natural (not case sensitive)
#                           temperature    >=-20 and <=120
#                                    op    adjust (validated)
#
#    Happy path.
#        test 001:    Default height
#        test 002:    Default temperature
#        test 003:    Default pressure
#        test 004:    Default horizon
#        test 005:    Horizon ignore case
#        test 006:    Low observation and nominal values
#        test 007:    Nominal observation and nominal values
#        test 008:    High observation and nominal values
#        test 009:    All default values
#        test 010:    High height
#        test 011:    High temperature
#        test 012:    Low temperature
#        test 013:    High pressure
#        test 014:    Low pressure
#
#    Sad path.
#        test 900:    No observation
#        test 901:    Empty observation
#        test 902:    Observation degree too large
#        test 903:    Observation without "d" character
#        test 904:    Observation degree too small
#        test 905:    Observation minute too large
#        test 906:    Height as letter
#        test 907:    Pressure as letter
#        test 908:    Temperature as letter
#        test 909:    Horizon as number
#        test 910:    Observation minute too small
#        test 911:    Pressure too small
#        test 912:    Temperature too small
#        test 913:    Extra key in values
#        test 914:    Empty values
#        test 915:    Empty horizon
#        test 916:    Pressure too large
#        test 917:    Temperature too large
#        test 918:    Height too small
#        test 919:    Empty height
#        test 920:    Observation too small
#        test 921:    Observation minutes not a float
#        test 922:    Observation minutes invalid decimal format
#        test 923:    Observation minutes not a valid floating point number
#
# Happy path tests
          
    def test001ShouldReturnDefaultHeight(self):
        values = {'observation': '65d51.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '65d50.6', 'observation': '65d51.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        self.assertEqual(expectedResult, actualResult)
             
    def test002ShouldReturnDefaultTemp(self):
        values = {'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '65d50.6', 'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust'}
        self.assertEqual(expectedResult, actualResult)
                    
    def test003ShouldReturnDefaultPressure(self):
        values = {'observation': '65d51.0', 'height': '15', 'horizon': 'artificial', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '65d50.6', 'observation': '65d51.0', 'height': '15', 'horizon': 'artificial', 'op': 'adjust'}
        self.assertEqual(expectedResult, actualResult)

    def test004ShouldReturnDefaultHorizon(self):
        values = {'observation': '65d51.0', 'height': '15', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '65d46.8','observation': '65d51.0', 'height': '15', 'op': 'adjust'}
        self.assertEqual(expectedResult, actualResult)
         
    def test005ShouldReturnArtificialIgnoringCase(self):
        values = {'observation': '65d51.0', 'horizon': 'ArTiFiCiAl', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '65d50.6', 'observation': '65d51.0', 'horizon': 'ArTiFiCiAl', 'op': 'adjust'}
        self.assertEqual(expectedResult, actualResult)
         
    def test006ShouldReturnLowAltitude(self):
        values = {'observation': '13d51.6', 'height': '33', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '72'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '13d42.3', 'observation': '13d51.6', 'height': '33', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '72'}
        self.assertEqual(expectedResult, actualResult)

    def test007ShouldReturnNominalAltitude(self):
        values = {'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude':'29d59.9', 'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        self.assertEqual(expectedResult, actualResult)
        
    def test008ShouldReturnHighAltitude(self):
        values = {'observation': '45d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude':'45d11.9', 'observation': '45d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        self.assertEqual(expectedResult, actualResult)
        
    def test009ShouldReturnAllDefaults(self):
        values = {'observation': '42d0.0',  'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust'}
        self.assertEqual(expectedResult, actualResult)
        
    def test010ShouldReturnHighHeight(self):
        values = {'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '28d27.9', 'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '85'}
        self.assertEqual(expectedResult, actualResult)
    
    def test011ShouldReturnHighTemp(self):
        values = {'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '115'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '28d28.0', 'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '115'}
        self.assertEqual(expectedResult, actualResult)
    
    def test012ShouldReturnLowTemp(self):
        values = {'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '28d27.6', 'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        self.assertEqual(expectedResult, actualResult)
        
    def test013ShouldReturnHighPressure(self):
        values = {'observation': '30d1.5', 'height': '9005', 'pressure': '1100', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '28d27.4', 'observation': '30d1.5', 'height': '9005', 'pressure': '1100', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        self.assertEqual(expectedResult, actualResult)
    
    def test014ShouldReturnLowPressure(self):
        values = {'observation': '30d1.5', 'height': '9005', 'pressure': '500', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude': '28d28.5', 'observation': '30d1.5', 'height': '9005', 'pressure': '500', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        self.assertEqual(expectedResult, actualResult)

    
# Sad path tests
        
    def test900ShouldReturnErrorNoObservation(self):
        values = {'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'temperature': '85', 'error': 'mandatory information is missing', 'op': 'adjust'}
        self.assertEqual(expectedResult, actualResult)
          
    def test901ShouldReturnErrorEmptyObservation(self):
        values = {'observation': '', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'mandatory information is missing'}
        self.assertEqual(expectedResult, actualResult)
            
    def test902ShouldReturnErrorDegreeTooLarge(self):
        values = {'observation': '91d1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '91d1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)
      
    def test903ShouldReturnErrorDegreeNoSeparatorCharacter(self):
        values = {'observation': '76c1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '76c1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)
          
    def test904ShouldReturnErrorDegreeTooSmall(self):
        values = {'observation': '-5d1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '-5d1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)
          
    def test905ShouldReturnErrorMinuteTooLarge(self):
        values = {'observation': '65d61', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d61', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)
           
    def test906ShouldReturnErrorHeightAsLetter(self):
        values = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'height is invalid'}
        self.assertEqual(expectedResult, actualResult)

    def test907ShouldReturnErrorPressureAsLetter(self):
        values = {'observation': '45d15.2', 'pressure': 'a', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '45d15.2', 'pressure': 'a', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'pressure is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test908ShouldReturnErrorTempAsLetter(self):
        values = {'observation': '45d15.2', 'horizon': 'natural', 'op': 'adjust', 'temperature': 'a'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '45d15.2', 'horizon': 'natural', 'op': 'adjust', 'temperature': 'a', 'error':'temperature is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test909ShouldReturnErrorHorizonAsNumber(self):
        values = {'observation': '45d15.2', 'horizon': '3', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '45d15.2', 'horizon': '3', 'op': 'adjust', 'error':'horizon is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test910ShouldReturnErrorMinuteTooSmall(self):
        values = {'observation': '65d-5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d-5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test911ShouldReturnErrorPressureTooSmall(self):
        values = {'observation': '65d51.0', 'height': '15', 'pressure': '50', 'horizon': 'artificial', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d51.0', 'height': '15', 'pressure': '50', 'horizon': 'artificial', 'op': 'adjust', 'error': 'pressure is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test912ShouldReturnErrorTempTooSmall(self):
        values = {'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '-21'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '-21', 'error': 'temperature is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test913ShouldReturnExtraKeyIgnore(self):
        values = {'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        actualResult = nav.adjust(values)
        expectedResult = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        self.assertEqual(expectedResult, actualResult)
        
    def test914ShouldReturnInfoMissing(self):
        values = {'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'error':'mandatory information is missing', 'op': 'adjust'}
        self.assertEqual(expectedResult, actualResult)
        
    def test915ShouldReturnErrorInvalidHorizon(self):
        values = {'observation': '65d51.0', 'horizon': ' ', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d51.0', 'horizon': ' ', 'op': 'adjust', 'error': 'horizon is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test916ShouldReturnErrorPressureTooLarge(self):
        values = {'observation': '65d51.0', 'height': '15', 'pressure': '1101', 'horizon': 'artificial', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d51.0', 'height': '15', 'pressure': '1101', 'horizon': 'artificial', 'op': 'adjust', 'error': 'pressure is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test917ShouldReturnErrorTempTooLarge(self):
        values = {'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '250'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '250', 'error': 'temperature is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test918ShouldReturnErrorHeightTooSmall(self):
        values = {'observation': '65d51.0', 'height': '-1', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d51.0', 'height': '-1', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'height is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test919ShouldReturnErrorHeightBlankEntry(self):
        values = {'observation': '65d51.0', 'height': '', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '65d51.0', 'height': '', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'height is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test920ShouldReturnErrorObservationTotalTooSmall(self):
        values = {'observation': '0d0.0', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '0d0.0', 'op': 'adjust', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)
        
    def test921ShouldReturnErrorObservationMinutesNotFloat(self):
        values = {'observation': '2d6', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '2d6', 'op': 'adjust', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)   
        
    def test922ShouldReturnErrorObservationMinutesInvalidFormat(self):
        values = {'observation': '2d6.55', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '2d6.55', 'op': 'adjust', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)   
        
    def test923ShouldReturnErrorObservationMinutesTrailingDecimal(self):
        values = {'observation': '2d6.55.', 'op': 'adjust'}
        actualResult = nav.adjust(values)
        expectedResult = {'observation': '2d6.55.', 'op': 'adjust', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, actualResult)   