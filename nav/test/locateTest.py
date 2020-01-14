"""
    Created on April 24, 2019
    adjustTest - Test file for the locate function.
    @author: Christopher Tillery (cat0050)
"""

import unittest
import nav.locate as nav

class locateTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
# Analysis
#    adjust(values)
#    Level: BVA
#
#    input:
#        values:     a dictionary of inputs with the assumedLat, assumedLong,
#                    and corrections containing n distances and n azimuths
#                           corrections     distance = integer(>= 0) and azimuth xx(>=0 and <360) + 'd' + y.y(>=0 and <60). Paired min 0d0.0, paired max 359d59.9. [[distance, azimuth], ...]
#                             assumedLat    xx(>-90 and <90) + 'd' + y.y(>=0 and <60). Paired min -89d59.9, paired max 89d59.9
#                            assumedLong    xx(>=0 and <360) + 'd' + y.y(>=0 and <60). Paired min 0d0.0, paired max 359d59.9
#                                    op    correct (validated)
#    output:
#        returns:    an updated dictionary according to the calculations within locate with the possibility
#                    of containing an error key
#                    
#
#    Happy path.
#        test 001:   provided example 1
#        test 002:   provided example 2   
#
#    Sad path.
#        test 900:   no corrections
#        test 901:   no assumedLat
#        test 902:   no assumedLong
#        test 903:   decimal in x of assumedLat
#        test 904:   no 'd' in assumedLat
#        test 905:   non-integer character besides 'd' in assumedLat
#        test 906:   x in assumedLat too low
#        test 907:   x in assumedLat too high
#        test 908:   y in assumedLat too high
#        test 909:   no decimal in y of assumedLat
#        test 910:   x in assumedLong too low
#        test 911:   x in assumedLong too high
#        test 912:   space in assumedLat
#        test 913:   no decimal in one character y of assumedLat
#        test 914:   no number before decimal in y of assumedLat
#        test 915:   distance in corrections too low
#        test 916:   distance in corrections not integer
#        test 917:   distance in corrections too high
#        test 918:   distance in corrections missing
#        test 919:   azimuth in corrections missing
#        test 920:   empty corrections
#        test 921:   empty corrections and no assumedLat
#        test 922:   more than distance and azimuth in corrections
#        test 923:   space in distance in corrections
#        test 924:   string in corrections not list representation
#
# Happy path tests
             
    def test001ShouldReturnResultOneCorrectionsValue(self):
        values = {'op':'locate','assumedLat':'-53d38.4', 'assumedLong': '350d35.3','corrections':'[[100,1d0.0]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate', 'assumedLat':'-53d38.4', 'assumedLong': '350d35.3', 'presentLat':'-51d58.4', 'corrections':'[[100,1d0.0]]','presentLong':'350d37.0','precision':'0','accuracy':'NA'}
        self.assertEqual(expectedResult, actualResult)
         
    def test002ShouldReturnResultMultipleCorrectionsValues(self):
        self.maxDiff = None
        values = {'op':'locate','assumedLat':'32d36.5', 'assumedLong': '274d31.1','corrections':'[[50,45d0.0], [75, 60d42.0], [100, 300d11.2], [42, 42d12.3], [70, 60d45.0], [10, 280d0.0]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate','assumedLat':'32d36.5', 'assumedLong': '274d31.1','corrections':'[[50,45d0.0], [75, 60d42.0], [100, 300d11.2], [42, 42d12.3], [70, 60d45.0], [10, 280d0.0]]',
                            'presentLat':'33d8.1', 'presentLong':'274d46.7','precision':'45','accuracy':'NA'}
        self.assertEqual(expectedResult, actualResult)
              
# Sad path tests
         
    def test900ShouldReturnErrorNoCorrections(self):
        values = {'op':'locate', 'assumedLong':'95d41.6',  'assumedLat':'-53d38.4'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate', 'assumedLong':'95d41.6',  'assumedLat':'-53d38.4', 'error':'corrections is missing'}
        self.assertEqual(expectedResult, actualResult)
         
    def test901ShouldReturnErrorNoAssumedLat(self):
        values = {'op':'locate', 'assumedLong':'95d41.6',  'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate', 'assumedLong':'95d41.6',  'corrections':'[[100,130d5.6]]', 'error':'assumedLat is missing'}
        self.assertEqual(expectedResult, actualResult)
         
    def test902ShouldReturnErrorNoAssumedLong(self):
        values = {'op':'locate', 'assumedLat':'-53d38.4', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate', 'assumedLat':'-53d38.4', 'corrections':'[[100,130d5.6]]', 'error':'assumedLong is missing'}
        self.assertEqual(expectedResult, actualResult)
         
    def test903ShouldReturnErrorDecimalInXOfAssumedLat(self):
        values = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16.0d38.4', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16.0d38.4', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)
         
    def test904ShouldReturnErrorNoDInAssumedLat(self):
        values = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16032.3', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16032.3', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)
         
    def test905ShouldReturnErrorCharacterBesidesDInAssumedLat(self):
        values = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16.0c32.3', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16.0c32.3', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)
         
    def test906ShouldReturnErrorXInAssumedLatTooLow(self):
        values = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'-90d0.0', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'-90d0.0', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)
         
    def test907ShouldReturnErrorXInAssumedLatTooHigh(self):
        values = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'90d0.0', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'90d0.0', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)
         
    def test908ShouldReturnErrorYInAssumedLatTooHigh(self):
        values = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'80d60.0', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'80d60.0', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)
         
    def test909ShouldReturnErrorNoDecimalInYOfAssumedLat(self):
        values = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'80d50', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'80d50', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)
         
    def test910ShouldReturnErrorXInAssumedLongTooLow(self):
        values = {'op':'locate',  'assumedLong':'-0d0.1', 'assumedLat':'60d5.4', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'-0d0.1', 'assumedLat':'60d5.4', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLong'}
        self.assertEqual(expectedResult, actualResult)
             
    def test911ShouldReturnErrorXInAssumedLongTooHigh(self):
        values = {'op':'locate',  'assumedLong':'360d0.0', 'assumedLat':'60d5.4', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'360d0.0', 'assumedLat':'60d5.4', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLong'}
        self.assertEqual(expectedResult, actualResult)
         
    def test912ShouldReturnErrorSpaceInAssumedLat(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60 d5.4', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60 d5.4', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)
         
    def test913ShouldReturnErrorNoDecimalInYOfAssumedLatOneCharacterY(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d5', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d5', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)   
         
    def test914ShouldReturnErrorNoNumberBeforeDecimalInYOfAssumedLat(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d.2', 'corrections':'[[100,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d.2', 'corrections':'[[100,130d5.6]]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, actualResult)   
         
    def test915ShouldReturnErrorDistanceInCorrectionsTooLow(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[-1,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[-1,130d5.6]]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, actualResult) 
         
    def test916ShouldReturnErrorDistanceInCorrectionsNotInteger(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[.3,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[.3,130d5.6]]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, actualResult)     
     
    def test917ShouldReturnErrorDistanceInCorrectionsTooHigh(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[2147483648,130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[2147483648,130d5.6]]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, actualResult)     
         
    def test918ShouldReturnErrorDistanceInCorrectionsMissing(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[130d5.6]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[130d5.6]]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, actualResult)     
         
    def test919ShouldReturnErrorAzimuthInCorrectionsMissing(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[130]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[130]]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, actualResult)    
    
    def test920ShouldReturnErrorEmptyCorrections(self):
        values = {'op':'locate','assumedLat':'-53d38.4', 'assumedLong':'350d35.3','corrections':'[[]]'}
        actualResult = nav.locate(values)
        expectedResult = {'error':'corrections can not be empty', 'op':'locate','assumedLat':'-53d38.4', 'assumedLong':'350d35.3','corrections':'[[]]'}
        self.assertEqual(expectedResult, actualResult)   
         
    def test921ShouldReturnErrorEmptyCorrectionsAndNoAssumedLat(self):
        values = {'op':'locate', 'assumedLong':'350d35.3','corrections':'[[]]'}
        actualResult = nav.locate(values)
        expectedResult = {'error': 'assumedLat is missing', 'op':'locate', 'assumedLong':'350d35.3','corrections':'[[]]'}
        self.assertEqual(expectedResult, actualResult)   
           
    def test922ShouldReturnErrorMoreThanDistanceAndAzimuthInCorrections(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[2,130d5.6, 3]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[2,130d5.6, 3]]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, actualResult)            
         
    def test923ShouldReturnErrorSpaceInDistance(self):
        values = {'op':'locate','assumedLat':'-53d38.4', 'assumedLong': '350d35.3','corrections':'[[ 100,1d0.0]]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate','assumedLat':'-53d38.4', 'assumedLong': '350d35.3','corrections':'[[ 100,1d0.0]]', 'error':'invalid corrections'}
        self.assertEqual(expectedResult, actualResult)  
         
    def test924ShouldReturnErrorStringNotList(self):
        values = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[18,130d5.6]'}
        actualResult = nav.locate(values)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[18,130d5.6]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, actualResult)             