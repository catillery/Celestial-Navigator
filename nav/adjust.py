"""
    Created on February 14, 2019
    adjust - Assignment6
    @author: Christopher Tillery (cat0050)
"""

from cmath import sqrt
from math import tan, radians
import decimal

# Calculates an adjusted altitude given an input dictionary called values.
def adjust(values):
    HORIZON_DEFAULT = 'natural'
    MINUTES_IN_HOUR = 60.0
    DIP_MULTIPLIER = -0.97
    REFRACTION_MULTIPLIER = -.00452
    ADD_TO_CELSIUS_TEMP = 273
    dip = 0
    
    observation = observationValidator(values)
    if 'error' in values.keys():
        return values   
    
    height = heightValidator(values)
    if 'error' in values.keys():
        return values   
    
    temperature = tempValidator(values)
    if 'error' in values.keys():
        return values   
    
    pressure = pressureValidator(values)
    if 'error' in values.keys():
        return values   
    
    horizon = horizonValidator(values)
    if 'error' in values.keys():
        return values   
         
    if horizon == HORIZON_DEFAULT:
        dip = (DIP_MULTIPLIER * sqrt(float(height))) / MINUTES_IN_HOUR
    
    observInDegrees = minutesToDecimal(observation)
    refraction = (REFRACTION_MULTIPLIER * float(pressure)) / (ADD_TO_CELSIUS_TEMP + convertToCelsius(temperature)) / tan(radians(observInDegrees))

    altitude = decimalToMinutes(observInDegrees + dip + refraction)
    altitudeValidator(values, altitude)
    
    return values

# Validates the value of the observation key in the dictionary values
def observationValidator(values):
    OBSERVATION_DEGREE_LOW_BOUND = 1
    OBSERVATION_DEGREE_UPPER_BOUND = 90
    OBSERVATION_MINUTE_LOW_BOUND = 0.0
    OBSERVATION_MINUTE_UPPER_BOUND = 60.0
    OBSERVATION_SEPARATOR = "d"
    OBSERVATION_ERROR = 'observation is invalid'
    EMPTY_INPUT_ERROR = 'mandatory information is missing'
    DECIMAL_POINT = "."
    
    if 'observation' in values.keys():
        observation = values['observation']
        observSeparatorLoc = observation.find(OBSERVATION_SEPARATOR)
        lastDecimalPointLoc = observation.find(DECIMAL_POINT)
        
        if len(observation) <= 0:
            values['error'] = EMPTY_INPUT_ERROR
            return
        
        if (observSeparatorLoc == -1 or lastDecimalPointLoc == -1):
            values['error'] = OBSERVATION_ERROR
            return
        
        # Check for valid "d" index
        if (observSeparatorLoc < 1 or observSeparatorLoc > 2) or (lastDecimalPointLoc >= 1 and len(observation) - lastDecimalPointLoc == 3):
            values['error'] = OBSERVATION_ERROR
            return
        
        # Find and attempt to assign the degree and minute values based on the "d" index; try-except ensures numerical values
        observDegreeRange = observSeparatorLoc
        observMinuteRange = observSeparatorLoc + 1
        try:
            observDegree = int(observation[:observDegreeRange])
            observMinute = float(observation[observMinuteRange:])
        except:
            values['error'] = OBSERVATION_ERROR
            return
        
        if (observDegree < OBSERVATION_DEGREE_LOW_BOUND or observDegree >= OBSERVATION_DEGREE_UPPER_BOUND) or (observMinute < OBSERVATION_MINUTE_LOW_BOUND or observMinute >= OBSERVATION_MINUTE_UPPER_BOUND):
            values['error'] = OBSERVATION_ERROR
        
        return observation
    
    else:
        values['error'] = EMPTY_INPUT_ERROR

# Validates the value of the height key in the dictionary values
def heightValidator(values):
    HEIGHT_DEFAULT = '0'
    HEIGHT_ERROR = 'height is invalid'
    HEIGHT_LOW_BOUND = 0
    
    if 'height' in values.keys():
        height = values['height']

        try:
            heightInt = float(height)
        except:
            values['error'] = HEIGHT_ERROR
            return
        
        if heightInt < HEIGHT_LOW_BOUND:
            values['error'] = HEIGHT_ERROR
        
    else:
        height = HEIGHT_DEFAULT
        
    return height

# Validates the value of the temperature key in the dictionary values
def tempValidator(values): 
    TEMP_LOWER_BOUND = -20
    TEMP_UPPER_BOUND = 120
    TEMPERATURE_DEFAULT = '72'
    TEMPERATURE_ERROR = 'temperature is invalid'
    
    if 'temperature' in values.keys():
        temperature = values['temperature']  

        try:
            tempInt = int(temperature)
        except:
            values['error'] = TEMPERATURE_ERROR
            return
        
        if tempInt < TEMP_LOWER_BOUND or tempInt > TEMP_UPPER_BOUND:
            values['error'] = TEMPERATURE_ERROR
    
    else:
        temperature = TEMPERATURE_DEFAULT

    return temperature
  
# Validates the value of the pressure key in the dictionary values   
def pressureValidator(values):
    PRESSURE_LOW_BOUND = 100
    PRESSURE_UPPER_BOUND = 1100
    PRESSURE_DEFAULT = '1010'
    PRESSURE_ERROR = 'pressure is invalid'

    if 'pressure' in values.keys():
        pressure = values['pressure']

        try:
            pressureInt = int(pressure)
        except:
            values['error'] = PRESSURE_ERROR
            return
        
        if pressureInt < PRESSURE_LOW_BOUND or pressureInt > PRESSURE_UPPER_BOUND:
            values['error'] = PRESSURE_ERROR
        
    else:
        pressure = PRESSURE_DEFAULT 
        
    return pressure 

# Validates the value of the horizon key in the dictionary values    
def horizonValidator(values):
    HORIZON_DEFAULT = 'natural'
    HORIZON_ARTIFICIAL = 'artificial'
        
    if ('horizon' in values.keys()):
        horizon = values['horizon']
        
        if horizon.lower() == HORIZON_DEFAULT:
            horizon = HORIZON_DEFAULT
        elif horizon.lower() == HORIZON_ARTIFICIAL:
            horizon = HORIZON_ARTIFICIAL
        else:
            values['error'] = 'horizon is invalid'         
            
    else:
        horizon = HORIZON_DEFAULT
        
    return horizon
   
# Validates the value of the altitude to be pushes the value to the dictionary with the key altitude
def altitudeValidator(values, altitude):
    ALTITUDE_DEGREE_LOW_BOUND = -90
    ALTITUDE_DEGREE_UPPER_BOUND = 90
    ALTITUDE_MINUTE_LOW_BOUND = 0.0
    ALTITUDE_MINUTE_UPPER_BOUND = 60.0
    ALTITUDE_SEPARATOR = "d"
    
    # Find and attempt to assign the degree and minute values based on the "d" index
    altitudeSeparatorLoc = altitude.find(ALTITUDE_SEPARATOR)
    altitudeDegreeRange = altitudeSeparatorLoc
    altitudeMinuteRange = altitudeSeparatorLoc + 1
    altitudeDegree = float(altitude[:altitudeDegreeRange])
    altitudeMinute = float(altitude[altitudeMinuteRange:])
    
    if (altitudeDegree <= ALTITUDE_DEGREE_LOW_BOUND or altitudeDegree >= ALTITUDE_DEGREE_UPPER_BOUND) or (altitudeMinute < ALTITUDE_MINUTE_LOW_BOUND or altitudeMinute >= ALTITUDE_MINUTE_UPPER_BOUND):
        values['error'] = 'altitude is invalid'
    
    values['altitude'] = altitude 
   
# Converts a Fahrenheit temperature to Celsius
def convertToCelsius(temperature):
    FAHRENHEIT_SUBTRACTION = 32
    FAHRENHEIT_FACTOR = 5.0 / 9.0
    
    return (float(temperature) - FAHRENHEIT_SUBTRACTION) * FAHRENHEIT_FACTOR

# Converts degrees + minutes to degrees + fraction
def minutesToDecimal(observation):
    OBSERVATION_SEPARATOR = "d"
    MINUTES = 60
    
    separatorLoc = observation.find(OBSERVATION_SEPARATOR)
    degreeRange = separatorLoc
    minuteRange = separatorLoc + 1
    
    observDegree = float(observation[:degreeRange])
    observMinute = float(observation[minuteRange:])
    
    return observDegree + (observMinute / MINUTES)

# Converts degrees + fraction to degrees + minutes with a "d" separating the degrees and minutes
def decimalToMinutes(altitude):
    MINUTES_IN_AN_HOUR = 60
    SIGNIFICANT_FIGURES = 1
    stringFormat = '1e' + str(-SIGNIFICANT_FIGURES * SIGNIFICANT_FIGURES)
    
    # Convert the number, and then round the number to the nearest 0.1 arc-minute using 0.5+ rounds upwards
    minutes = MINUTES_IN_AN_HOUR * (altitude.real - int(altitude.real))
    minutes = decimal.Decimal(minutes.real)
    minuteForm = minutes.quantize(decimal.Decimal(stringFormat), rounding='ROUND_HALF_UP')
    return str(int(altitude.real)) + "d" + str(minuteForm)