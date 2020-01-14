"""
    Created on March 27, 2019
    predict - Assignment8
    @author: Christopher Tillery (cat0050)
"""
from nav.predict import minutesToDecimal, decimalToMinutes
from math import degrees, radians, sin, cos, asin, acos

# Determines how far and in what direction one must move to match an observed sighting to a predicted sighting
def correct(values):
    NORMALIZE_VALUE = 0
    
    latValue = inputValidator(values, 'lat')
    if 'error' in values.keys():
        return values
    longValue = inputValidator(values, 'long')
    if 'error' in values.keys():
        return values
    altitudeValue = inputValidator(values, 'altitude')
    if 'error' in values.keys():
        return values
    assumedLatValue = inputValidator(values, 'assumedLat')
    if 'error' in values.keys():
        return values
    assumedLongValue = inputValidator(values, 'assumedLong')
    if 'error' in values.keys():
        return values

    localHourAngle = calculateLocalHourAngle(longValue, assumedLongValue)
    intermediateDistance = calculateIntermediateDistance(latValue, assumedLatValue, localHourAngle)
    correctedAltitude = calculateCorrectedAltitude(intermediateDistance)
    correctedDistance = calculateCorrectedDistance(altitudeValue, correctedAltitude)
    correctedAzimuth = calculateCorrectedAzimuth(latValue, assumedLatValue, intermediateDistance, correctedAltitude)

    if correctedDistance < NORMALIZE_VALUE:
        correctedDistance = normalizeCorrectedDistance(correctedDistance)
        correctedAzimuth = normalizeCorrectedAzimuth(correctedAzimuth)

    updateValues(values, correctedDistance, correctedAzimuth)
    
    return values

# Updates the dictionary values
def updateValues(values, correctedDistance, correctedAzimuth):
    values['correctedAzimuth'] = decimalToMinutes(correctedAzimuth)
    values['correctedDistance'] = str(correctedDistance)

# Validates and confirms proper inputs for the correct function
def inputValidator(values, typeName):
    EMPTY_INPUT_ERROR = 'mandatory information is missing'
    LAT_LOW_BOUND = -90
    LAT_HIGH_BOUND = 90
    ALTITUDE_LOW_BOUND = 0
    ALTITUDE_HIGH_BOUND = 90
    LONG_LOW_BOUND = 0
    LONG_HIGH_BOUND = 360
    MINUTE_LOW_BOUND = 0.0
    MINUTE_HIGH_BOUND = 60.0
    NEGATIVE = '-'
    BLANK_CHAR = ' '
    SEPARATE_CHAR = "d"
    DECIMAL_POINT = "."
    invalidInputError = 'invalid ' + typeName
    
    if typeName in values.keys():
        value = values[typeName]
        separatorLoc = value.find(SEPARATE_CHAR)
        decimalPointLoc = value.find(DECIMAL_POINT)
        blankCharLoc = value.find(BLANK_CHAR)
        negativeLoc = value.find(NEGATIVE)
        
        if len(value) <= 0:
            values['error'] = EMPTY_INPUT_ERROR
            return
        
        # Check for valid "d"and "." index
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
        elif typeName == 'altitude':
            if degree < ALTITUDE_LOW_BOUND or degree >= ALTITUDE_HIGH_BOUND or (degree == ALTITUDE_LOW_BOUND and minute == MINUTE_LOW_BOUND) or (negativeLoc != -1):
                values['error'] = invalidInputError
        
        return value
    else:
        values['error'] = EMPTY_INPUT_ERROR  

# Normalizes the distance (make positive)
def normalizeCorrectedDistance(correctedDistance):
    return abs(correctedDistance)
    
# Normalizes the azimuth (adjust by 180 and make it fall within 360 degrees)
def normalizeCorrectedAzimuth(correctedAzimuth):
    NORMALIZING_DEGREE = 180
    MOD_VALUE = 360
    
    return (correctedAzimuth + NORMALIZING_DEGREE) % MOD_VALUE

# Determines the compass direction in which to make a distance adjustment
def calculateCorrectedAzimuth(latValue, assumedLatValue, intermediateDistance, correctedAltitude):
    latDecimal = radians(minutesToDecimal(latValue))
    assumedLatDecimal = radians(minutesToDecimal(assumedLatValue))    
    correctedAltitudeDecimal = radians(minutesToDecimal(correctedAltitude))
    return degrees(acos((sin(latDecimal) - (sin(assumedLatDecimal) * intermediateDistance)) / (cos(assumedLatDecimal) * cos(correctedAltitudeDecimal))))

# Calculates the distance in arc-minutes the navigator must move to make the observed and calculated star positions match
def calculateCorrectedDistance(altitudeValue, correctedAltitude):
    ARC_MINUTE_CONVERSION_FACTOR = 60
    
    return int(round((minutesToDecimal(altitudeValue) - minutesToDecimal(correctedAltitude)) * ARC_MINUTE_CONVERSION_FACTOR))

# Calculate the angle by which to adjust the observed altitude in order to match the star
def calculateCorrectedAltitude(intermediateDistance):
    return decimalToMinutes(degrees((asin(intermediateDistance))))

# Calculates the local hour angle of the navigator
def calculateLocalHourAngle(longValue, assumedLongValue):
    localHourAngle = (minutesToDecimal(longValue) + minutesToDecimal(assumedLongValue))
    return decimalToMinutes(localHourAngle)

# Calculates the intermediate distance necessary to correcting the altitude
def calculateIntermediateDistance(latValue, assumedLatValue, localHourAngle):
    latDecimal = radians(minutesToDecimal(latValue))
    assumedLatDecimal = radians(minutesToDecimal(assumedLatValue))
    lhaDecimal = radians(minutesToDecimal(localHourAngle)) 
    return (sin(latDecimal) * sin(assumedLatDecimal)) + (cos(latDecimal) * cos(assumedLatDecimal) * cos(lhaDecimal))