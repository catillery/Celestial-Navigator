"""
    Created on April 24, 2019
    locate - Assignment10
    @author: Christopher Tillery (cat0050)
"""

from nav.predict import minutesToDecimal, decimalToMinutes
from math import radians, cos, sin, sqrt
from dis import dis

# Determines geoposition based on trilateration of multiple sightings  
def locate(values):
    
    assumedLat = inputValidator(values, 'assumedLat')
    if 'error' in values.keys():
        return values
    
    assumedLong = inputValidator(values, 'assumedLong')
    if 'error' in values.keys():
        return values
    
    corrections = inputValidator(values, 'corrections')
    if 'error' in values.keys():
        return values
    
    nsCorrection = determineAdjustment(corrections, 'NS')
    ewCorrection = determineAdjustment(corrections, 'EW')
    presentLat = calculatePresentLat(assumedLat, nsCorrection)
    presentLong = calculatePresentLong(assumedLong, ewCorrection)
    precision = estimatePrecision(corrections, nsCorrection, ewCorrection)

    updateValues(values, presentLat, presentLong, precision)

    return values

# Validates and confirms proper inputs for the locate function
def inputValidator(values, typeName):
    EMPTY_INPUT_ERROR = typeName + ' is missing'
    invalidInputError = 'invalid ' + typeName
    NEGATIVE = '-'
    BLANK_CHAR = ' '
    SEPARATE_CHAR = "d"
    DECIMAL_POINT = "."
    LONG_LOW_BOUND = 0
    LONG_HIGH_BOUND = 360
    LAT_LOW_BOUND = -90
    LAT_HIGH_BOUND = 90
    MINUTE_LOW_BOUND = 0.0
    MINUTE_HIGH_BOUND = 60.0
    
    if typeName in values.keys():
        
        if typeName is 'corrections':
            valueList = correctionsValidator(values);
            return valueList
        
        else:
            value = values[typeName]
            separatorLoc = value.find(SEPARATE_CHAR)
            decimalPointLoc = value.find(DECIMAL_POINT)
            blankCharLoc = value.find(BLANK_CHAR)
            negativeLoc = value.find(NEGATIVE)
            
            if len(value) <= 0:
                values['error'] = EMPTY_INPUT_ERROR
                return
        
            # Check for valid "d" and "." index
            if separatorLoc < 1 or decimalPointLoc < 3 or blankCharLoc != -1 or negativeLoc > separatorLoc or decimalPointLoc - separatorLoc == 1 or decimalPointLoc == len(value) - 1:
                values['error'] = invalidInputError
                return
            
            # Find and attempt to assign the degree and minute values based on the "d" index; try-except ensures numerical values
            degreeRange = separatorLoc
            minuteRange = separatorLoc + 1
            try:
                degree = int(value[:degreeRange])
                minute = float(value[minuteRange:])
                # Input yy bounds checking
                if minute >= MINUTE_HIGH_BOUND or minute < MINUTE_LOW_BOUND:
                    raise Exception()
            except:
                values['error'] = invalidInputError
                return
            
            # Input xx bounds checking
            if typeName == 'lat' or typeName == 'assumedLat':
                if degree <= LAT_LOW_BOUND or degree >= LAT_HIGH_BOUND:
                    values['error'] = invalidInputError
            elif typeName == 'long' or typeName == 'assumedLong':
                if degree < LONG_LOW_BOUND or degree >= LONG_HIGH_BOUND or (degree == LONG_LOW_BOUND and minute > MINUTE_LOW_BOUND and negativeLoc != -1):
                    values['error'] = invalidInputError
        
            return value

    else:
        values['error'] = EMPTY_INPUT_ERROR 

# Validates and confirms proper inputs for the corrections value
def correctionsValidator(values):
    EMPTY_INPUT_ERROR = 'corrections can not be empty'
    INVALID_INPUT_ERROR = 'invalid corrections'
    NEGATIVE = '-'
    BLANK_CHAR = ' '
    SEPARATE_CHAR = "d"
    DECIMAL_POINT = "."
    Y_LOW_BOUND = 0
    Y_HIGH_BOUND = 360
    MINUTE_LOW_BOUND = 0.0
    MINUTE_HIGH_BOUND = 60.0
    INDEX_START = 0
    
    corrections = correctionsToListOfLists(values)
    
    if len(corrections) > INDEX_START:
        for index in range(INDEX_START, len(corrections)):
                azimuth = extractAzimuth(corrections[index])
                distance = extractDistance(corrections[index])
                separatorLoc = azimuth.find(SEPARATE_CHAR)
                decimalPointLoc = azimuth.find(DECIMAL_POINT)
                blankCharLoc = azimuth.find(BLANK_CHAR)
                negativeLoc = azimuth.find(NEGATIVE)
                
                if distance.find(DECIMAL_POINT) >= INDEX_START or distance.find(BLANK_CHAR) >= INDEX_START:
                    values['error'] = INVALID_INPUT_ERROR
                    return
                
                if len(azimuth) <= 0 or len(distance) <= 0:
                    values['error'] = EMPTY_INPUT_ERROR
                    return
            
                # Check for valid "d"and "." index
                if separatorLoc < 1 or decimalPointLoc < 3 or blankCharLoc != -1 or negativeLoc > separatorLoc or decimalPointLoc - separatorLoc == 1 or decimalPointLoc == len(azimuth) - 1:
                    values['error'] = INVALID_INPUT_ERROR
                    return
                
                # Find and attempt to assign the degree and minute values based on the "d" index; try-except ensures numerical values
                degreeRange = separatorLoc
                minuteRange = separatorLoc + 1
                try:
                    degree = int(azimuth[:degreeRange])
                    minute = float(azimuth[minuteRange:])
                    distance = int(distance)
                    # Input yy bounds checking
                    if minute >= MINUTE_HIGH_BOUND or minute < MINUTE_LOW_BOUND:
                        raise Exception()
                except:
                    values['error'] = INVALID_INPUT_ERROR
                    return
                
                # Input xx bounds checking
                if degree < Y_LOW_BOUND or degree >= Y_HIGH_BOUND or (degree == Y_LOW_BOUND and minute > MINUTE_LOW_BOUND and negativeLoc != -1):
                    values['error'] = INVALID_INPUT_ERROR
                if int(distance) < 0 or int(distance) > 2147483647:
                    values['error'] = INVALID_INPUT_ERROR
                    
    return corrections

# Updates the dictionary values
def updateValues(values, presentLat, presentLong, precision):
    values['presentLat'] = str(presentLat)
    values['presentLong'] = str(presentLong)
    values['precision'] = str(precision)
    values['accuracy'] = 'NA'
    
# Estimates the precision of the present position by measuring the uniformity of the input corrected distance/corrected azimuth pairs
def estimatePrecision(corrections, nsCorrection, ewCorrection):
    CORRECTIONS_INDEX_START = 0
    POWER_OF_2 = 2
    SIG_FIGS = 2
    nsPair = 0
    ewPair = 0
    summation = 0
    
    for index in range(CORRECTIONS_INDEX_START, len(corrections)):
        correctedAzimuth = radians(minutesToDecimal(extractAzimuth(corrections[index])))
        nsPair = pow((float(extractDistance(corrections[index])) * round(cos(correctedAzimuth), SIG_FIGS) - nsCorrection), POWER_OF_2)
        ewPair = pow((float(extractDistance(corrections[index])) * round(sin(correctedAzimuth), SIG_FIGS) - ewCorrection), POWER_OF_2)
        summation = summation + sqrt(nsPair + ewPair)
    
    return int(summation / len(corrections))

# Determines the present latitude by applying NS Adjustments
def calculatePresentLat(assumedLat, nsCorrection):
    MINUTES = 60 
    presentLat = minutesToDecimal(assumedLat) + nsCorrection / MINUTES
    return decimalToMinutes(presentLat)
   
# Determines the present longitude by applying by applying EW adjustments
def calculatePresentLong(assumedLong, ewCorrection):   
    MINUTES = 60
    presentLong = minutesToDecimal(assumedLong) + ewCorrection / MINUTES
    return decimalToMinutes(presentLong) 

# Extracts the azimuth in a given corrections sub-list
def extractAzimuth(value):
    AZIMUTH_INDEX = 1
    return value[AZIMUTH_INDEX]

# Extracts the distance in a given corrections sub-list
def extractDistance(value):
    DISTANCE_INDEX = 0
    return value[DISTANCE_INDEX]

#  Determine north-south or east-west adjustments to make the the assumed position based on the collection of direction and azimuth corrections
def determineAdjustment(corrections, directions):
    CORRECTIONS_INDEX_START = 0
    SIG_FIGS = 2
    
    correctedDistanceList = [''] * len(corrections)
    correctedAzimuthList = [''] * len(corrections)
    multipliedList = [''] * len(corrections)
    summation = 0
    
    for index in range(CORRECTIONS_INDEX_START, len(corrections)):
                correctedDistanceList[index] = extractDistance(corrections[index])
                correctedAzimuthList[index] = extractAzimuth(corrections[index])
                if directions is 'NS':
                    multipliedList[index] = float(correctedDistanceList[index]) * cos(radians(minutesToDecimal(correctedAzimuthList[index])))
                else:
                    multipliedList[index] = float(correctedDistanceList[index]) * sin(radians(minutesToDecimal(correctedAzimuthList[index])))
                summation = summation + multipliedList[index]
                
    return round(summation / len(corrections), SIG_FIGS)

# Converts corrections from a string of strings representing lists to a list of string lists
def correctionsToListOfLists(values):
    EMPTY_INPUT_ERROR = 'corrections can not be empty'
    INVALID_INPUT_ERROR = 'invalid corrections'
    CORRECTIONS_INDEX_START = 0
    COUNT_DISTANCE_AND_AZIMUTH = 2
    DISTANCE_INDEX = 0
    AZIMUTH_INDEX = 1
    
    value = values['corrections']
    
    if value == '[]':
        values['error'] = EMPTY_INPUT_ERROR
        return []

    # The magic happens here - string representing list of lists to list of string lists
    strs = value.replace('[', '').split('],')
    valueList = [map(str, s.replace(']', '').split(',')) for s in strs]
    
    for index_values in range(CORRECTIONS_INDEX_START, len(valueList)):
        for index_inner_values in range(CORRECTIONS_INDEX_START, 1):
            if valueList[index_values][index_inner_values] == '':
                values['error'] = EMPTY_INPUT_ERROR
                return []
    
    if value.count('[') != len(valueList) + 1 or value.count(']') != len(valueList) + 1 or value.count(',') != len(valueList) + len(valueList) - 1:
        values['error'] = INVALID_INPUT_ERROR
        return []
        
    for index in range(CORRECTIONS_INDEX_START, len(valueList)):
        if len(valueList[index]) != COUNT_DISTANCE_AND_AZIMUTH:
            values['error'] = INVALID_INPUT_ERROR
            return []
        
        # Due to the nature of the conversion method, an extra space is added before the distance value when the index in the corrections
        # list is > 0 - we strip that leading space off but leave any leading spaces that were present in the dictionary
        if index > CORRECTIONS_INDEX_START:
            valueList[index][DISTANCE_INDEX] = extractDistance(valueList[index])[1:]
            valueList[index][AZIMUTH_INDEX] = extractAzimuth(valueList[index])[1:]
        else:
            valueList[index][DISTANCE_INDEX] = extractDistance(valueList[index])
            valueList[index][AZIMUTH_INDEX] = extractAzimuth(valueList[index])
            
    return valueList
    