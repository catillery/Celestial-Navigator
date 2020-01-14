"""
    Created on March 4, 2019
    predictTest - Test file for the predict function.
    @author: Christopher Tillery (cat0050)
"""
import unittest
import nav.predict as nav

class predictTest(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass
    
# Analysis
#    predict(values)
#    Level: BVA
#
#    input:
#        values:     a dictionary of inputs with the body, date, and time
#                        body    case independent string matching a name of a navigable star (mandatory)
#                        date    string of length 10 representing a date in yyyy-mm-dd format (optional - defaults to 2001-01-01)
#                                    yyyy: integer .GE. 2001 and .LE. 2100
#                                          may be a leap year or a non-leap year, to determine if leap year:
#                                                1. if the year is evenly divisible by 4, go to step 2. Otherwise, go to step 5.
#                                                2. if the year is evenly divisible by 100, go to step 3. Otherwise, go to step 4.
#                                                3. if the year is evenly divisible by 400, go to step 4. Otherwise, go to step 5.
#                                                4. the year is a leap year (it has 366 days).
#                                                5. the year is not a leap year (it has 365 days).
#                                      mm: two digit integer .GE. 01 and .LE. 12 
#                                      dd: two digit integer .GE. 01 and .LE. LAST_DAY_IN_MONTH
#                                       -: character that denotes separation between yyyy, mm, and dd. must be in indices 4 & 7 - no others
#                                          LAST_DAY_IN_MONTH: 31 if mm = 01, 03, 05, 06, 08, 10, 12
#                                                             30 if mm = 04, 05, 07, 09, 11
#                                                             28 if mm = 02 & yyyy is not leap year
#                                                             29 if mm = 02 & yyyy is leap year
#                        time    string of length 8 representing a time in the hh:mm:ss format (optional - defaults to 00:00:00)
#                                      hh: two digit integer .GE. 00 & .LE. 23
#                                      mm: two digit integer .GE. 00 & .LE. 59
#                                      ss: two digit integer .GE. 00 & .LE. 59
#                                       :: character that denotes separation between hh, mm, and ss. must be in indices 2 & 5 - no others
#    output:
#        returns:    an updated dictionary according to the calculations within predict in order to provide the
#                    geographical location at which a celestial body is directly overhead
#                    Dictionary element    Range
#                                 error    diagnostic string (only on errors)
#                                              Ex: star not in catalog, mandatory information missing, invalid date, invalid time
#                                    op    predict
#                                  body    body provided as input with proper case formatting
#                                  time    provided time in hh:mm:ss format
#                                  date    provided date in yyyy-mm-dd format
#                                  long    calculated longitude of the body of the form xdy
#                                              x: .GE. 0 & .LT. 90
#                                              d: character d as a delimiter
#                                              y: .GE. 0.0 & .LT. 60.0
#                                   lat    calculated latitude of the body of the form xdy
#                                              x: .GE. 0 & .LT. 90
#                                              d: character d as a delimiter
#                                              y: .GE. 0.0 & .LT. 60.0
#
#    Happy path.
#        test 000: example passing test with Aldebaran
#        test 001: example passing test with Betelgeuse
#        test 002: passing with default time
#        test 003: passing with default date
#        test 004: passing with body containing spaces and declination negative
#        
#
#    Sad path.
#        test 900: no body in input dictionary
#        test 901: body not in star catalog
#        test 902: date string wrong length
#        test 903: year in date too low
#        test 904: year in date too high
#        test 905: month in date too low
#        test 906: month in date too high
#        test 907: day too low
#        test 908: day too high in odd month
#        test 909: day too high in even month
#        test 910: day too high in Feb on leap year
#        test 911: day too high in Feb not on leap year
#        test 912: first day delimiter not correct
#        test 913: second day delimiter not correct
#        test 914: empty time input
#        test 915: decimal point in hour portion of time input
#        test 916: decimal point in minute portion of time input
#        test 917: decimal point in seconds portion of time input
#        test 918: first time delimiter is incorrect
#        test 919: second time delimiter is incorrect
#        test 920: hour too low in time
#        test 921: hour too high in time
#        test 922: minute too low in time
#        test 923: minute too high in time
#        test 924: second too low in time
#        test 925: second too high in time
#
# Happy path tests

    def test000ShouldReturnStarLatAndLongAldebaran(self):
        values = {'op': 'predict', 'body': 'Aldebaran', 'time': '03:15:42', 'date': '2016-01-17'}
        expectedResult = {'op': 'predict', 'body': 'Aldebaran', 'time': '03:15:42', 'date': '2016-01-17', 'long': '95d41.6', 'lat': '16d32.3'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test001ShouldReturnStarLatAndLongBetelgeuse(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'time': '03:15:42', 'long': '75d53.6', 'lat': '7d24.3'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test002ShouldReturnStarLatAndLongDefaultTime(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2016-01-17', 'long': '26d50.1', 'lat': '7d24.3'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test003ShouldReturnStarLatAndLongDefaultDate(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '03:15:42'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '03:15:42', 'long': '60d45.2', 'lat': '7d24.3'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test004ShouldReturnStarLatAndLongSpaceInBodyAndNegDeclination(self):
        values = {'op': 'predict', 'body': 'Kaus Australis'}
        expectedResult = {'op': 'predict', 'body': 'Kaus Australis', 'long': '184d24.4', 'lat': '-34d22.4'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test005ShouldReturnStarLatAndLongFebruaryLeapYear(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2004-02-29'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2004-02-29', 'long': '69d7.7', 'lat': '7d24.3'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 
        
    def test006ShouldReturnStarLatAndLongFebruaryNotLeapYear(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02-28'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02-28', 'long': '68d22.9', 'lat': '7d24.3'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 
        

# Sad path tests

    def test900ShouldReturnErrorNoBody(self):
        values = {'op': 'predict'}
        expectedResult = {'op': 'predict', 'error': 'mandatory information is missing'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test901ShouldReturnErrorBodyNotInCatalog(self):
        values = {'op': 'predict', 'body': 'unknown'}
        expectedResult = {'op': 'predict', 'error': 'star not in catalog', 'body': 'unknown'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
    
    def test902ShouldReturnErrorDateStringWrongLength(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001--01-01'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001--01-01',  'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test903ShouldReturnErrorYearTooLow(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2000-01-01'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2000-01-01', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
    
    def test904ShouldReturnErrorYearTooHigh(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2101-01-01'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2101-01-01', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 

    def test905ShouldReturnErrorMonthTooLow(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-00-01'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-00-01', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 
        
    def test906ShouldReturnErrorMonthTooHigh(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-13-01'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-13-01', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 

    def test907ShouldReturnErrorDayTooLow(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-01-00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-01-00', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 

    def test908ShouldReturnErrorDayTooHighOddMonth(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-01-32'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-01-32', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 
        
    def test909ShouldReturnErrorDayTooHighEvenMonth(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-04-31'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2001-04-31', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 
        
    def test910ShouldReturnErrorDayTooHighFebruaryLeapYear(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2004-02-30'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2004-02-30', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 
        
    def test911ShouldReturnErrorDayTooHighFebruaryNotLeapYear(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02-29'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02-29', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 
        
    def test912ShouldReturnErrorFirstDayDelimiterIncorrect(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003_02-25'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003_02-25', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result) 
        
    def test913ShouldReturnErrorSecondDayDelimiterIncorrect(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02_25'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2003-02_25', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test914ShouldReturnErrorEmptyTime(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': ''}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'error': 'invalid time', 'time': ''}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test915ShouldReturnErrorDecimalInHours(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '.0:00:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '.0:00:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test916ShouldReturnErrorDecimalInMinutes(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:.0:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:.0:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test917ShouldReturnErrorDecimalInSeconds(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:.0'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:.0', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test918ShouldReturnErrorFirstTimeDelimiterIncorrect(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00-00:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00-00:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test919ShouldReturnErrorSecondTimeDelimiterIncorrect(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00-00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00-00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test920ShouldReturnErrorHourTooLow(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '-1:00:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '-1:00:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)    
        
    def test921ShouldReturnErrorHourTooHigh(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '25:00:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '25:00:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)    
    
    def test922ShouldReturnErrorMinuteTooLow(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:-1:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:-1:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)    
        
    def test923ShouldReturnErrorMinuteTooHigh(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:60:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:60:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)    
        
    def test924ShouldReturnErrorSecondTooLow(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:-1'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:-1', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)    
    
    def test925ShouldReturnErrorSecondTooHigh(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:60'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:60', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test926ShouldReturnErrorHourNotNumber(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': 'aa:00:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': 'aa:00:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test927ShouldReturnErrorMinuteNotNumber(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:aa:00'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:aa:00', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
            
    def test928ShouldReturnErrorSecondNotNumber(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:aa'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'time': '00:00:aa', 'error': 'invalid time'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
           
    def test929ShouldReturnErrorYearNotNumber(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': 'aaaa-02-25'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': 'aaaa-02-25', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
            
    def test930ShouldReturnErrorMonthNotNumber(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-aa-25'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-aa-25', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
            
    def test931ShouldReturnErrorDayNotNumber(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-02-aa'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-02-aa', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)
        
    def test931ShouldReturnErrorDayTooHigh(self):
        values = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-09-31'}
        expectedResult = {'op': 'predict', 'body': 'Betelgeuse', 'date': '2005-09-31', 'error': 'invalid date'}
        result = nav.predict(values);
        self.assertEqual(expectedResult, result)