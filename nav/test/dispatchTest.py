import unittest
import httplib
from urllib import urlencode
import json

import nav.dispatch as nav

class DispatchTest(unittest.TestCase):
    
    def setUp(self):
        self.inputDictionary = {}
        self.errorKey = "error"
        self.solutionKey = "probability"
        self.BX_PATH = '/nav?'
        self.BX_PORT = 5000
        self.BX_URL = 'localhost'
#         self.BX_PORT = 5000
#         self.BX_URL = 'www.ibmcloud.com'

    def tearDown(self):
        self.inputDictionary = {}

    def setParm(self, key, value):
        self.inputDictionary[key] = value
        
    def microservice(self):
        try:
            theParm = urlencode(self.inputDictionary)
            theConnection = httplib.HTTPConnection(self.BX_URL, self.BX_PORT)
            theConnection.request("GET", self.BX_PATH + theParm)
            theStringResponse = theConnection.getresponse().read()
            return theStringResponse
        except Exception as e:
            return "error encountered during transaction"
        
    def string2dict(self, httpResponse):
        '''Convert JSON string to dictionary'''
        result = {}
        try:
            jsonString = httpResponse.replace("'", "\"")
            unicodeDictionary = json.loads(jsonString)
            for element in unicodeDictionary:
                if(isinstance(unicodeDictionary[element],unicode)):
                    result[str(element)] = str(unicodeDictionary[element])
                else:
                    result[str(element)] = unicodeDictionary[element]
        except Exception as e:
            result['diagnostic'] = str(e)
        return result


    # -----------------------------------------------------------------------
    # ---- Acceptance Tests
    # 100 dispatch operation
    #   Happy path analysis:
    #        values:      mandatory
    #                     dictionary
    #                     Operations:   {'op':'adjust'}
    #                                   {'op':'predict'}
    #                                   {'op':'correct'}
    #                                   {'op':'locate'}
    #   Sad path analysis:
    #        values:
    #                     no op specified             values={}
    #                        -- return {'error':'no op  is specified'}
    #                     contain 'error' as a key      values={5d04.9', 'height': '6.0', 'pressure': '1010',
    #                                                           'horizon': 'artificial', 'temperature': '72'
    #                                                           'error':'no op is specified'}'
    #                        -- return values without error as a key and without its values
    #                     not-dictionary                values=42
    #                        -- return {'error':'parameter is not a dictionary'}
    #                     not legal operation           values={'op': 'unknown'}
    #                        -- return {'error':'op is not a legal operation'}
    #                     missing dictionary            dispatch()
    #                        -- return {'error':'dictionary is missing'}
    # Happy path

    def test100_010ShouldReturnUnchangedValuesWithOperationAdjust(self):
        self.setParm('op','adjust')
        self.setParm('error','mandatory information is missing')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertDictEqual(self.inputDictionary, resultDictionary)

    def test100_020ShouldReturnUnchangedValuesWithOperationPredict(self):
        self.setParm('op','predict')
        self.setParm('error','mandatory information is missing')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertDictEqual(self.inputDictionary, resultDictionary)
 
    def test100_030ShouldReturnUnchangedValuesWithOperationCorrect(self):
        self.setParm('op','correct')
        self.setParm('error','mandatory information is missing')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertDictEqual(self.inputDictionary, resultDictionary)
        
    def test100_040ShouldReturnUnchangedValuesWithOperationLocate(self):
        self.setParm('op','locate')
        self.setParm('error','assumedLat is missing')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertDictEqual(self.inputDictionary, resultDictionary)
        
    def test100_050ShouldReturnDefaultHeightAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '65d50.6', 'observation': '65d51.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        self.assertEqual(expectedResult, resultDictionary)
             
    def test100_060ShouldReturnDefaultTempAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('height', '15')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '65d50.6', 'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust'}
        self.assertEqual(expectedResult, resultDictionary)
                    
    def test100_070ShouldReturnDefaultPressureAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('height', '15')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '65d50.6', 'observation': '65d51.0', 'height': '15', 'horizon': 'artificial', 'op': 'adjust'}
        self.assertEqual(expectedResult, resultDictionary)

    def test100_070ShouldReturnDefaultHorizonAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('op', 'adjust')
        self.setParm('height', '15')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '65d46.8','observation': '65d51.0', 'height': '15', 'op': 'adjust'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test100_080ShouldReturnArtificialIgnoringCaseAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('op', 'adjust')
        self.setParm('horizon', 'ArTiFiCiAl')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '65d50.6', 'observation': '65d51.0', 'horizon': 'ArTiFiCiAl', 'op': 'adjust'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test100_090ShouldReturnLowAltitudeAdjust(self):
        self.setParm('observation', '13d51.6')
        self.setParm('pressure', '1010')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '72')
        self.setParm('height', '33')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '13d42.3', 'observation': '13d51.6', 'height': '33', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '72'}
        self.assertEqual(expectedResult, resultDictionary)

    def test100_100ShouldReturnNominalAltitudeAdjust(self):
        self.setParm('observation', '30d1.5')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '19.0')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude':'29d59.9', 'observation': '30d1.5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_110ShouldReturnHighAltitudeAdjust(self):
        self.setParm('observation', '45d15.2')
        self.setParm('pressure', '1010')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '71')
        self.setParm('height', '6')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude':'45d11.9', 'observation': '45d15.2', 'height': '6', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_120ShouldReturnAllDefaultsAdjust(self):
        self.setParm('observation', '42d0.0')
        self.setParm('op', 'adjust')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_130ShouldReturnHighHeightAdjust(self):
        self.setParm('observation', '30d1.5')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '9005')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '28d27.9', 'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '85'}
        self.assertEqual(expectedResult, resultDictionary)
    
    def test100_140ShouldReturnHighTempAdjust(self):
        self.setParm('observation', '30d1.5')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '115')
        self.setParm('height', '9005')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '28d28.0', 'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '115'}
        self.assertEqual(expectedResult, resultDictionary)
    
    def test100_150ShouldReturnLowTempAdjust(self):
        self.setParm('observation', '30d1.5')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '0')
        self.setParm('height', '9005')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '28d27.6', 'observation': '30d1.5', 'height': '9005', 'pressure': '1000', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_160ShouldReturnHighPressureAdjust(self):
        self.setParm('observation', '30d1.5')
        self.setParm('pressure', '1100')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '0')
        self.setParm('height', '9005')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '28d27.4', 'observation': '30d1.5', 'height': '9005', 'pressure': '1100', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        self.assertEqual(expectedResult, resultDictionary)
    
    def test100_170ShouldReturnLowPressureAdjust(self):
        self.setParm('observation', '30d1.5')
        self.setParm('pressure', '500')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '0')
        self.setParm('height', '9005')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude': '28d28.5', 'observation': '30d1.5', 'height': '9005', 'pressure': '500', 'horizon': 'natural', 'op': 'adjust', 'temperature': '0'}
        self.assertEqual(expectedResult, resultDictionary)

    def test100_180ShouldReturnStarLatAndLongAldebaranPredict(self):
        self.setParm('body', 'Aldebaran')
        self.setParm('op', 'predict')
        self.setParm('time', '03:15:42')
        self.setParm('date', '2016-01-17')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Aldebaran', 'time': '03:15:42', 'date': '2016-01-17', 'long': '95d41.6', 'lat': '16d32.3'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_190ShouldReturnStarLatAndLongBetelgeusePredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '03:15:42')
        self.setParm('date', '2016-01-17')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42', 'long': '75d53.6', 'lat': '7d24.3'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_200ShouldReturnStarLatAndLongDefaultTimePredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2016-01-17')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'long': '26d50.1', 'lat': '7d24.3'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_210ShouldReturnStarLatAndLongDefaultDatePredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '03:15:42')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '03:15:42', 'long': '60d45.2', 'lat': '7d24.3'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_220ShouldReturnStarLatAndLongSpaceInBodyAndNegDeclinationPredict(self):
        self.setParm('body', 'Kaus Australis')
        self.setParm('op', 'predict')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Kaus Australis', 'long': '184d24.4', 'lat': '-34d22.4'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_230ShouldReturnStarLatAndLongFebruaryLeapYearPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2004-02-29')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2004-02-29', 'long': '69d7.7', 'lat': '7d24.3'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_240ShouldReturnStarLatAndLongFebruaryNotLeapYearPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2003-02-28')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02-28', 'long': '68d22.9', 'lat': '7d24.3'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_250ShouldReturnResultProvidedExample1(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '16d32.3')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '53d38.4')
        self.setParm( 'assumedLong', '350d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'16d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'53d38.4', 'assumedLong': '350d35.3', 'correctedDistance':'104', 'correctedAzimuth':'262d55.6'}
        self.assertEqual(expectedResult, resultDictionary)
               
    def test100_260ShouldReturnResultProvidedExample2(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '89d20.1')
        self.setParm('long', '154d5.4')
        self.setParm('altitude', '37d15.6')
        self.setParm('assumedLat', '33d59.7')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'89d20.1', 'long':'154d5.4', 'altitude':'37d15.6',  'assumedLat':'33d59.7', 'assumedLong':'74d35.3', 'correctedDistance':'222', 'correctedAzimuth':'0d33.8'}
        self.assertEqual(expectedResult, resultDictionary)
                     
    def test100_270ShouldReturnResultNominalInputs(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '50d50.0')
        self.setParm('long', '50d50.0')
        self.setParm('altitude', '50d50.0')
        self.setParm('assumedLat', '50d50.0')
        self.setParm( 'assumedLong', '50d50.0')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'50d50.0', 'long':'50d50.0', 'altitude':'50d50.0',  'assumedLat':'50d50.0', 'assumedLong':'50d50.0', 'correctedDistance':'1168', 'correctedAzimuth':'46d25.0'}
        self.assertEqual(expectedResult, resultDictionary)
 
    def test100_280ShouldReturnResultProvidedExample3(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '16d32.3')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '350d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'16d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong': '350d35.3', 'correctedDistance':'1488', 'correctedAzimuth':'77d6.9'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test100_290ShouldReturnResultProvidedExample1(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '350d35.3')
        self.setParm('corrections', '[[100,1d0.0]]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate', 'assumedLat':'-53d38.4', 'assumedLong': '350d35.3', 'presentLat':'-51d58.4', 'corrections':'[[100,1d0.0]]','presentLong':'350d37.0','precision':'0','accuracy':'NA'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test100_300ShouldReturnResultProvidedExample2(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '32d36.5')
        self.setParm('assumedLong', '274d31.1')
        self.setParm('corrections', '[[50,45d0.0], [75, 60d42.0], [100, 300d11.2], [42, 42d12.3], [70, 60d45.0], [10, 280d0.0]]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate','assumedLat':'32d36.5', 'assumedLong': '274d31.1','corrections':'[[50,45d0.0], [75, 60d42.0], [100, 300d11.2], [42, 42d12.3], [70, 60d45.0], [10, 280d0.0]]',
                            'presentLat':'33d8.1', 'presentLong':'274d46.7','precision':'45','accuracy':'NA'}
        self.assertEqual(expectedResult, resultDictionary)
        
    # Sad path
    def test900_010_ShouldReturnValuesWithErrorKeyWhenNoOpSpecified(self):
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertTrue(resultDictionary.has_key("error"), True)
 
    def test900_020ShouldReturnValuesWithErrorWhenParameterIsNotALegalOperation(self):
        self.setParm('op','unknown')        
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertTrue(resultDictionary.has_key("error"), True)
 
    def test900_030ShouldReturnValuesWithErrorWhenOpIsBlank(self):
        self.setParm('op','')        
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertTrue(resultDictionary.has_key("error"), True)

    def test900_040ShouldReturnErrorNoObservationAdjust(self):
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '19')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'temperature': '85', 'error': 'mandatory information is missing', 'op': 'adjust'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_050ShouldReturnErrorEmptyObservationAdjust(self):
        self.setParm('observation', '')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '19')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'mandatory information is missing'}
        self.assertEqual(expectedResult, resultDictionary)
            
    def test900_060ShouldReturnErrorDegreeTooLargeAdjust(self):
        self.setParm('observation', '91d1.5')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '19')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '91d1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
      
    def test900_070ShouldReturnErrorDegreeNoSeparatorCharacterAdjust(self):
        self.setParm('observation', '76c1.5')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '19')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '76c1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_080ShouldReturnErrorDegreeTooSmallAdjust(self):
        self.setParm('observation', '-5d1.5')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '19')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '-5d1.5', 'height': '19', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_090ShouldReturnErrorMinuteTooLargeAdjust(self):
        self.setParm('observation', '65d61')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '19.0')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d61', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
           
    def test900_100ShouldReturnErrorHeightAsLetterAdjust(self):
        self.setParm('observation', '45d15.2')
        self.setParm('pressure', '1010')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '71')
        self.setParm('height', 'a')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '45d15.2', 'height': 'a', 'pressure': '1010', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'height is invalid'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_110ShouldReturnErrorPressureAsLetterAdjust(self):
        self.setParm('observation', '45d15.2')
        self.setParm('pressure', 'a')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '71')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '45d15.2', 'pressure': 'a', 'horizon': 'natural', 'op': 'adjust', 'temperature': '71', 'error':'pressure is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_120ShouldReturnErrorTempAsLetterAdjust(self):
        self.setParm('observation', '45d15.2')
        self.setParm('horizon', 'natural')
        self.setParm('op', 'adjust')
        self.setParm('temperature', 'a')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '45d15.2', 'horizon': 'natural', 'op': 'adjust', 'temperature': 'a', 'error':'temperature is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_130ShouldReturnErrorHorizonAsNumberAdjust(self):
        self.setParm('observation', '45d15.2')
        self.setParm('horizon', '3')
        self.setParm('op', 'adjust')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '45d15.2', 'horizon': '3', 'op': 'adjust', 'error':'horizon is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_140ShouldReturnErrorMinuteTooSmallAdjust(self):
        self.setParm('observation', '65d-5')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '85')
        self.setParm('height', '19.0')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d-5', 'height': '19.0', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_150ShouldReturnErrorPressureTooSmallAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('pressure', '50')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('height', '15')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d51.0', 'height': '15', 'pressure': '50', 'horizon': 'artificial', 'op': 'adjust', 'error': 'pressure is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_160ShouldReturnErrorTempTooSmallAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('temperature', '-21')
        self.setParm('height', '15')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '-21', 'error': 'temperature is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_170ShouldReturnExtraKeyIgnoreAdjust(self):
        self.setParm('observation', '42d0.0')
        self.setParm('op', 'adjust')
        self.setParm('extraKey', 'ignore')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'altitude':'41d59.0', 'observation': '42d0.0',  'op': 'adjust', 'extraKey':'ignore'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_180ShouldReturnInfoMissingAdjust(self):
        self.setParm('op', 'adjust')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'error':'mandatory information is missing', 'op': 'adjust'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_190ShouldReturnErrorInvalidHorizonAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('horizon', ' ')
        self.setParm('op', 'adjust')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d51.0', 'horizon': ' ', 'op': 'adjust', 'error': 'horizon is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_200ShouldReturnErrorPressureTooLargeAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('pressure', '1101')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('height', '15')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d51.0', 'height': '15', 'pressure': '1101', 'horizon': 'artificial', 'op': 'adjust', 'error': 'pressure is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_210ShouldReturnErrorTempTooLargeAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('height', '15')
        self.setParm('temperature', '250')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d51.0', 'height': '15', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '250', 'error': 'temperature is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_220ShouldReturnErrorHeightTooSmallAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('height', '-1')
        self.setParm('temperature', '85')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d51.0', 'height': '-1', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'height is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_230ShouldReturnErrorHeightBlankEntryAdjust(self):
        self.setParm('observation', '65d51.0')
        self.setParm('pressure', '1000')
        self.setParm('horizon', 'artificial')
        self.setParm('op', 'adjust')
        self.setParm('height', '')
        self.setParm('temperature', '85')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '65d51.0', 'height': '', 'pressure': '1000', 'horizon': 'artificial', 'op': 'adjust', 'temperature': '85', 'error': 'height is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_240ShouldReturnErrorObservationTotalTooSmallAdjust(self):
        self.setParm('observation', '0d0.0')
        self.setParm('op', 'adjust')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '0d0.0', 'op': 'adjust', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_250ShouldReturnErrorObservationMinutesNotFloat(self):
        self.setParm('observation', '2d6')
        self.setParm('op', 'adjust')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '2d6', 'op': 'adjust', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_260ShouldReturnErrorObservationMinutesInvalidFormatAdjust(self):
        self.setParm('observation', '2d6.55')
        self.setParm('op', 'adjust')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '2d6.55', 'op': 'adjust', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)  
        
    def test900_270ShouldReturnErrorObservationMinutesTrailingDecimalPredict(self):
        self.setParm('observation', '2d6.55.')
        self.setParm('op', 'adjust')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'observation': '2d6.55.', 'op': 'adjust', 'error': 'observation is invalid'}
        self.assertEqual(expectedResult, resultDictionary)  

    def test900_280ShouldReturnErrorNoBodyPredict(self):
        self.setParm('op', 'predict')
        expectedResult = {'op': 'predict', 'error': 'mandatory information is missing'}
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        self.assertEqual(expectedResult, resultDictionary)  
        
    def test900_290ShouldReturnErrorBodyNotInCatalogPredict(self):
        self.setParm('body', 'unknown')
        self.setParm('op', 'predict')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'error': 'star not in catalog', 'body': 'unknown'}
        self.assertEqual(expectedResult, resultDictionary)  
    
    def test900_300ShouldReturnErrorDateStringWrongLengthPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2001--01-01')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001--01-01',  'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_310ShouldReturnErrorYearTooLowPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2000-01-01')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2000-01-01', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
    
    def test900_320ShouldReturnErrorYearTooHighPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2101-01-01')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2101-01-01', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_330ShouldReturnErrorMonthTooLowPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2001-00-01')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-00-01', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_340ShouldReturnErrorMonthTooHighPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2001-13-01')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-13-01', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_350ShouldReturnErrorDayTooLowPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2001-01-00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-01-00', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_360ShouldReturnErrorDayTooHighOddMonthPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2001-01-32')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-01-32', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_370ShouldReturnErrorDayTooHighEvenMonthPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2001-04-31')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-04-31', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_380ShouldReturnErrorDayTooHighFebruaryLeapYearPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2004-02-30')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2004-02-30', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_390ShouldReturnErrorDayTooHighFebruaryNotLeapYearPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2003-02-29')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02-29', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_400ShouldReturnErrorFirstDayDelimiterIncorrectPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2003_02-25')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003_02-25', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_410ShouldReturnErrorSecondDayDelimiterIncorrectPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2003-02_25')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02_25', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_420ShouldReturnErrorEmptyTimePredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'error': 'invalid time', 'time': ''}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_430ShouldReturnErrorDecimalInHoursPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '.0:00:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '.0:00:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_440ShouldReturnErrorDecimalInMinutesPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:.0:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:.0:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_440ShouldReturnErrorDecimalInSecondsPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:00:.0')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:.0', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_450ShouldReturnErrorFirstTimeDelimiterIncorrectPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00-00:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00-00:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_460ShouldReturnErrorSecondTimeDelimiterIncorrectPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:00-00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00-00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_470ShouldReturnErrorHourTooLowPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '-1:00:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '-1:00:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_480ShouldReturnErrorHourTooHighPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '25:00:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '25:00:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)  
    
    def test900_490ShouldReturnErrorMinuteTooLowPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:-1:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:-1:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)  
        
    def test900_500ShouldReturnErrorMinuteTooHighPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:60:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:60:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary) 
        
    def test900_510ShouldReturnErrorSecondTooLowPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:00:-1')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:-1', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)  
    
    def test900_520ShouldReturnErrorSecondTooHighPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:00:60')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:60', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)  
        
    def test900_530ShouldReturnErrorHourNotNumberPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', 'aa:00:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': 'aa:00:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)  
        
    def test900_540ShouldReturnErrorMinuteNotNumberPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:aa:00')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:aa:00', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)  
            
    def test900_550ShouldReturnErrorSecondNotNumberPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('time', '00:00:aa')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:aa', 'error': 'invalid time'}
        self.assertEqual(expectedResult, resultDictionary)  
           
    def test900_560ShouldReturnErrorYearNotNumberPredict(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', 'aaaa-02-25')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': 'aaaa-02-25', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)  
            
    def test900_570ShouldReturnErrorMonthNotNumber(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2005-aa-25')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-aa-25', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)  
            
    def test900_580ShouldReturnErrorDayNotNumber(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2005-02-aa')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-02-aa', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)  
    
    def test900_590ShouldReturnErrorDayTooHigh(self):
        self.setParm('body', 'Betelgeuse')
        self.setParm('op', 'predict')
        self.setParm('date', '2005-09-31')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-09-31', 'error': 'invalid date'}
        self.assertEqual(expectedResult, resultDictionary)  
        
    def test900_600ShouldReturnErrorMissingLat(self):
        self.setParm('altitude', '13d42.3')
        self.setParm('op', 'correct')
        self.setParm('long', '95d41.6')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, resultDictionary)
            
    def test900_610ShouldReturnErrorMissingLong(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '55d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'55d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, resultDictionary)
              
    def test900_620ShouldReturnErrorMissingAltitude(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '55d41.6')
        self.setParm('long', '95d41.6')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'55d41.6',  'long':'95d41.6', 'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_630ShouldReturnErrorMissingAssumedLat(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '55d41.6')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct',  'lat':'55d41.6', 'long':'95d41.6', 'altitude':'13d42.3', 'assumedLong':'74d35.3', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, resultDictionary)
            
    def test900_640ShouldReturnErrorMissingAssumedLong(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '55d41.6')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct',  'lat':'55d41.6', 'long':'95d41.6', 'altitude':'13d42.3', 'assumedLat':'-53d38.4', 'error':'mandatory information is missing'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_650NoReturnErrorNoInputSeparator(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '16.0d32.3')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'16.0d32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
             
    def test900_660ShouldReturnErrorXXInInputNotInt(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '16.032.3')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'16.032.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
  
    def test900_670ShouldReturnErrorWrongSeparator(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '16c32.3')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'16c32.3', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)

          
    def test900_680ShouldReturnErrorLatBasedXXInputTooLow(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '-90d0.0')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'-90d0.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_690ShouldReturnErrorLatBasedXXInputTooHigh(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '90d0.0')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'90d0.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_700ShouldReturnErrorYYInputTooLow(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '80d-0.1')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'80d-0.1', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_710ShouldReturnErrorYYInputTooHigh(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '80d60.0')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'80d60.0', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_720ShouldReturnErrorYYInputNotFloat(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '80d50')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'80d50', 'long':'95d41.6', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_730ShouldReturnErrorLongBasedXXInputTooLow(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '80d0.0')
        self.setParm('long', '-0d0.1')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'80d0.0', 'long':'-0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid long'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_740ShouldReturnErrorLongBasedXXInputTooHigh(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '70d0.0')
        self.setParm('long', '360d0.0')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'70d0.0', 'long':'360d0.0', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid long'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_750ShouldReturnErrorAltitudeBasedXXInputTooLow(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '60d0.0')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '-0d0.1')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'60d0.0', 'long':'95d41.6', 'altitude':'-0d0.1',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid altitude'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_760ShouldReturnErrorAltitudeBasedXXInputTooHigh(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '60d0.0')
        self.setParm('long', '95d41.6')
        self.setParm('altitude', '90d0.0')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'60d0.0', 'long':'95d41.6', 'altitude':'90d0.0',  'assumedLat':'-53d38.4', 'assumedLong': '74d35.3', 'error':'invalid altitude'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_770ShouldReturnErrorFirstBelowXXRange(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '60d5.4')
        self.setParm('long', '-0d0.1')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'60d5.4', 'long':'-0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid long'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_780ShouldReturnErrorBlankChar(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '60 d5.4')
        self.setParm('long', '0d0.1')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm( 'assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'60 d5.4', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_790ShouldReturnErrorDecimalAtEnd(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '60d5.')
        self.setParm('long', '0d0.1')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'60d5.', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
    
    def test900_800ShouldReturnErrorNoValueToLeftOfDecimal(self):
        self.setParm('op', 'correct')
        self.setParm('lat', '60d.2')
        self.setParm('long', '0d0.1')
        self.setParm('altitude', '13d42.3')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '74d35.3')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'correct', 'lat':'60d.2', 'long':'0d0.1', 'altitude':'13d42.3',  'assumedLat':'-53d38.4', 'assumedLong':'74d35.3', 'error':'invalid lat'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_810ShouldReturnErrorNoCorrections(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '95d41.6')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate', 'assumedLong':'95d41.6',  'assumedLat':'-53d38.4', 'error':'corrections is missing'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_820ShouldReturnErrorNoAssumedLat(self):
        self.setParm('op', 'locate')
        self.setParm('corrections', '[100,130d5.6]')
        self.setParm('assumedLong', '95d41.6')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate', 'assumedLong':'95d41.6',  'corrections':'[100,130d5.6]', 'error':'assumedLat is missing'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_830test902ShouldReturnErrorNoAssumedLong(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate', 'assumedLat':'-53d38.4', 'corrections':'[100,130d5.6]', 'error':'assumedLong is missing'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_840ShouldReturnErrorDecimalInXOfAssumedLat(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '16.0d38.4')
        self.setParm('assumedLong', '95d41.6')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16.0d38.4', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_850ShouldReturnErrorNoDInAssumedLat(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '16032.3')
        self.setParm('assumedLong', '95d41.6')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16032.3', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_860ShouldReturnErrorCharacterBesidesDInAssumedLat(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '16.0c32.3')
        self.setParm('assumedLong', '95d41.6')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'16.0c32.3', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_870ShouldReturnErrorXInAssumedLatTooLow(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '-90d0.0')
        self.setParm('assumedLong', '95d41.6')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'-90d0.0', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_880ShouldReturnErrorXInAssumedLatTooHigh(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '90d0.0')
        self.setParm('assumedLong', '95d41.6')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'90d0.0', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_890ShouldReturnErrorYInAssumedLatTooHigh(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '80d60.0')
        self.setParm('assumedLong', '95d41.6')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'80d60.0', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_900ShouldReturnErrorNoDecimalInYOfAssumedLat(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '80d50')
        self.setParm('assumedLong', '95d41.6')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'95d41.6', 'assumedLat':'80d50', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_910ShouldReturnErrorXInAssumedLongTooLow(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d5.4')
        self.setParm('assumedLong', '-0d0.1')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'-0d0.1', 'assumedLat':'60d5.4', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLong'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_920ShouldReturnErrorXInAssumedLongTooHigh(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d5.4')
        self.setParm('assumedLong', '-0d0.1')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'-0d0.1', 'assumedLat':'60d5.4', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLong'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_930ShouldReturnErrorSpaceInAssumedLat(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60 d5.4')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60 d5.4', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_940ShouldReturnErrorNoDecimalInYOfAssumedLatOneCharacterY(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d5')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d5', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_950ShouldReturnErrorNoNumberBeforeDecimalInYOfAssumedLat(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d.2')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[100,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d.2', 'corrections':'[100,130d5.6]',  'error':'invalid assumedLat'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_960ShouldReturnErrorDistanceInCorrectionsTooLow(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d0.2')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[-1,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[-1,130d5.6]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_970ShouldReturnErrorDistanceInCorrectionsNotInteger(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d0.2')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[.3,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[.3,130d5.6]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, resultDictionary)
     
    def test900_980ShouldReturnErrorDistanceInCorrectionsTooHigh(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d0.2')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[2147483648,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[2147483648,130d5.6]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_990ShouldReturnErrorDistanceInCorrectionsMissing(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d0.2')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[130d5.6]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, resultDictionary)
         
    def test900_1000ShouldReturnErrorAzimuthInCorrectionsMissing(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d0.2')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[130]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[130]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, resultDictionary)

    def test900_1010ShouldReturnErrorEmptyCorrections(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '350d35.3')
        self.setParm('corrections', '[]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'error':'corrections can not be empty', 'op':'locate','assumedLat':'-53d38.4', 'assumedLong':'350d35.3','corrections':'[]'}
        self.assertEqual(expectedResult, resultDictionary)
        
    def test900_1020ShouldReturnErrorEmptyCorrectionsAndNoAssumedLat(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLong', '350d35.3')
        self.setParm('corrections', '[]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'error': 'assumedLat is missing', 'op':'locate', 'assumedLong':'350d35.3','corrections':'[]'}
        self.assertEqual(expectedResult, resultDictionary)
          
    def test900_1030ShouldReturnErrorMoreThanDistanceAndAzimuthInCorrections(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d0.2')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[[2,130d5.6, 3]]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[2,130d5.6, 3]]', 'error':'invalid corrections'}
        self.assertEqual(expectedResult, resultDictionary)      
        
    def test900_1040ShouldReturnErrorSpaceInDistance(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '-53d38.4')
        self.setParm('assumedLong', '350d35.3')
        self.setParm('corrections', '[[ 100,1d0.0]]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate','assumedLat':'-53d38.4', 'assumedLong': '350d35.3','corrections':'[[ 100,1d0.0]]', 'error':'invalid corrections'}
        self.assertEqual(expectedResult, resultDictionary)  
        
    def test900_1050ShouldReturnErrorStringNotListRepresentation(self):
        self.setParm('op', 'locate')
        self.setParm('assumedLat', '60d0.2')
        self.setParm('assumedLong', '60d0.0')
        self.setParm('corrections', '[[18,130d5.6]')
        result = self.microservice()
        resultDictionary = self.string2dict(result)
        expectedResult = {'op':'locate',  'assumedLong':'60d0.0', 'assumedLat':'60d0.2', 'corrections':'[[18,130d5.6]',  'error':'invalid corrections'}
        self.assertEqual(expectedResult, resultDictionary)      