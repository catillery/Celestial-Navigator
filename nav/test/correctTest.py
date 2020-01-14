"""
    Created on March 27, 2019
    correctTest - Test file for the correct function.
    @author: Christopher Tillery (cat0050)
"""

import unittest
import nav.correct as nav

class correctTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
# Analysis
#    correct(values)
#    Level: BVA
#
#    input:
#        values:     a dictionary of inputs with the possibility of containing a lat, long,
#                    altitude, assumedLat, and assumedLong; arrives unvalidated
#                                   lat    xx(>-90 and <90) + 'd' + y.y(>=0 and <60). Paired min -89d59.9, paired max 89d59.9
#                                  long    xx(>=0 and <360) + 'd' + y.y(>=0 and <60). Paired min 0d0.0, paired max 359d59.9
#                              altitude    xx(>=0 and <90) + 'd' + y.y(>=0 and <60). Paired min 0d0.1, paired max 89d59.9
#                            assumedLat    xx(>-90 and <90) + 'd' + y.y(>=0 and <60). Paired min -89d59.9, paired max 89d59.9
#                           assumedLong    xx(>=0 and <360) + 'd' + y.y(>=0 and <60). Paired min 0d0.0, paired max 359d59.9
#                                    op    correct (validated)
#    output:
#        returns:    an updated dictionary according to the calculations within correct with the possibility
#                    of containing an error key
#                    Dictionary element    Range xx = integer, yy = float, d = char, . = char
#                                   lat    xx(>-90 and <90) + 'd' + y.y(>=0 and <60). Paired min -89d59.9, paired max 89d59.9. x or y may have leading zeroes.
#                                  long    xx(>=0 and <360) + 'd' + y.y(>=0 and <60). Paired min 0d0.0, paired max 359d59.9. x or y may have leading zeroes.
#                              altitude    xx(>=0 and <90) + 'd' + y.y(>=0 and <60). Paired min 0d0.1, paired max 89d59.9. x or y may have leading zeroes.
#                            assumedLat    xx(>-90 and <90) + 'd' + y.y(>=0 and <60). Paired min -89d59.9, paired max 89d59.9. x or y may have leading zeroes.
#                           assumedLong    xx(>=0 and <360) + 'd' + y.y(>=0 and <60). Paired min 0d0.0, paired max 359d59.9. x or y may have leading zeroes.
#                     correctedDistance    string representing a positive integer
#                      correctedAzimuth    xx(>=0 and <360) + 'd' + y.y(>=0 and <60). Paired min 0d0.0, paired max 359d59.9. Rounded to nearest 1 arc-minute. No leading zeroes on x or y.
#                                    op    correct
#
#    Happy path.
#        test 001:    provided example 1
#        test 002:    provided example 2
#        test 003:    nominal inputs
#        test 004:    provided example 3
#
#    Sad path.
#        test 900:    missing lat
#        test 901:    missing long
#        test 902:    missing altitude
#        test 903:    missing assumedLat
#        test 904:    missing assumedLong
#        test 905:    no 'd' in input
#        test 906:    xx in input is not int
#        test 907:    'd' character is wrong char
#        test 908:    lat based xx input too low
#        test 909:    lat based xx input too high
#        test 910:    yy too low
#        test 911:    yy too high
#        test 912:    yy in input is not float
#        test 913:    long based xx input too low
#        test 914:    long based xx input too high
#        test 915:    altitude based xx input too low
#        test 916:    altitude based xx input too high
#        test 917:    first value below xx range (-0d0.1)
#        test 918:    space char in input
#        test 919:    no digit to right of decimal in input
#        test 920:    no digit to left of decimal in input
#
# Happy path tests
     
    def test001ShouldReturnResultProvidedExample1(self):
        values = {'op':'correct', 'lat':'16d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong': '350d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'16d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong': '350d35.3', 'correctedDistance':'1488', 'correctedAzimuth':'77d6.9'}
        self.assertEqual(expectedResult, actualResult)
               
    def test002ShouldReturnResultProvidedExample2(self):
        values = {'op':'correct', 'lat':'89d20.1', 'long':'154d5.4', 'altitude':'37d15.6',  'assumedLat':'33d59.7', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'89d20.1', 'long':'154d5.4', 'altitude':'37d15.6',  'assumedLat':'33d59.7', 'assumedLong':'74d35.3', 'correctedDistance':'222', 'correctedAzimuth':'0d33.8'}
        self.assertEqual(expectedResult, actualResult)
                     
    def test003ShouldReturnResultNominalInputs(self):
        values = {'op':'correct', 'lat':'50d50.0', 'long':'50d50.0', 'altitude':'50d50.0',  'assumedLat':'50d50.0', 'assumedLong':'50d50.0'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'50d50.0', 'long':'50d50.0', 'altitude':'50d50.0',  'assumedLat':'50d50.0', 'assumedLong':'50d50.0', 'correctedDistance':'1168', 'correctedAzimuth':'46d25.0'}
        self.assertEqual(expectedResult, actualResult)
 
    def test004ShouldReturnResultProvidedExample3(self):
        values = {'op':'correct', 'lat':'16d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'53d38.4', 'assumedLong': '350d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'16d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'53d38.4', 'assumedLong': '350d35.3', 'correctedDistance':'104', 'correctedAzimuth':'262d55.6'}
        self.assertEqual(expectedResult, actualResult)

# Sad path tests
         
    def test900ShouldReturnErrorMissingLat(self):
        values = {'op':'correct', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, actualResult)
            
    def test901ShouldReturnErrorMissingLong(self):
        values = {'op':'correct', 'lat':'55d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'55d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, actualResult)
              
    def test902ShouldReturnErrorMissingAltitude(self):
        values = {'op':'correct', 'lat':'55d41.6', 'long':'95d41.6',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'55d41.6',  'long':'95d41.6', 'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, actualResult)
          
    def test903ShouldReturnErrorMissingAssumedLat(self):
        values = {'op':'correct', 'lat':'55d41.6',  'long':'95d41.6', 'altitude':'13d42.3', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct',  'lat':'55d41.6', 'long':'95d41.6', 'altitude':'13d42.3', 'assumedLong':'74d35.3', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, actualResult)
            
    def test904ShouldReturnErrorMissingAssumedLong(self):
        values = {'op':'correct', 'lat':'55d41.6',  'long':'95d41.6', 'altitude':'13d42.3', 'assumedLat':'-53d38.4'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct',  'lat':'55d41.6', 'long':'95d41.6', 'altitude':'13d42.3', 'assumedLat':'-53d38.4', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, actualResult)
            
    def test905NoReturnErrorNoInputSeparator(self):
        values = {'op':'correct', 'lat':'16.0d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'16.0d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
             
    def test906ShouldReturnErrorXXInInputNotInt(self):
        values = {'op':'correct', 'lat':'16.032.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'16.032.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
  
    def test907ShouldReturnErrorWrongSeparator(self):
        values = {'op':'correct', 'lat':'16c32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':' 74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'16c32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':' 74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
          
    def test908ShouldReturnErrorLatBasedXXInputTooLow(self):
        values = {'op':'correct', 'lat':'-90d0.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'-90d0.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
          
    def test909ShouldReturnErrorLatBasedXXInputTooHigh(self):
        values = {'op':'correct', 'lat':'90d0.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'90d0.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
          
    def test910ShouldReturnErrorYYInputTooLow(self):
        values = {'op':'correct', 'lat':'80d-0.1', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'80d-0.1', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
          
    def test911ShouldReturnErrorYYInputTooHigh(self):
        values = {'op':'correct', 'lat':'80d60.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':' 74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'80d60.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':' 74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
          
    def test912ShouldReturnErrorYYInputNotFloat(self):
        values = {'op':'correct', 'lat':'80d50', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'80d50', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
          
    def test913ShouldReturnErrorLongBasedXXInputTooLow(self):
        values = {'op':'correct', 'lat':'80d0.0', 'long':'-0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'80d0.0', 'long':'-0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid long'}
        self.assertEqual(expectedResult, actualResult)
          
    def test914ShouldReturnErrorLongBasedXXInputTooHigh(self):
        values = {'op':'correct', 'lat':'70d0.0', 'long':'360d0.0', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'70d0.0', 'long':'360d0.0', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid long'}
        self.assertEqual(expectedResult, actualResult)
          
    def test915ShouldReturnErrorAltitudeBasedXXInputTooLow(self):
        values = {'op':'correct', 'lat':'60d0.0', 'long':'95d41.6', 'altitude':'-0d0.0',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'60d0.0', 'long':'95d41.6', 'altitude':'-0d0.0',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid altitude'}
        self.assertEqual(expectedResult, actualResult)
          
    def test916ShouldReturnErrorAltitudeBasedXXInputTooHigh(self):
        values = {'op':'correct', 'lat':'60d0.0', 'long':'95d41.6', 'altitude':'90d0.0',  'assumedLat':'-53d38.4', 'assumedLong': '74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'60d0.0', 'long':'95d41.6', 'altitude':'90d0.0',  'assumedLat':'-53d38.4', 'assumedLong': '74d35.3', 'error':'invalid altitude'}
        self.assertEqual(expectedResult, actualResult)
          
    def test917ShouldReturnErrorFirstBelowXXRange(self):
        values = {'op':'correct', 'lat':'60d5.4', 'long':'-0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'60d5.4', 'long':'-0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid long'}
        self.assertEqual(expectedResult, actualResult)
         
    def test918ShouldReturnErrorBlankChar(self):
        values = {'op':'correct', 'lat':'60 d5.4', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d3.2', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'60 d5.4', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d3.2', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
        
    def test919ShouldReturnErrorDecimalAtEnd(self):
        values = {'op':'correct', 'lat':'60d5.', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d3.2', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'60d5.', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d3.2', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)
    
    def test920ShouldReturnErrorNoValueToLeftOfDecimal(self):
        values = {'op':'correct', 'lat':'60d.2', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d3.2', 'assumedLong':'74d35.3'}
        actualResult = nav.correct(values)
        expectedResult = {'op':'correct', 'lat':'60d.2', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d3.2', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, actualResult)