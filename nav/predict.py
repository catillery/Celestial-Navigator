"""
    Created on March 4, 2019
    predict - Assignment7
    @author: Christopher Tillery (cat0050)
"""
import decimal
from calendar import isleap
from datetime import date

# Computes the Greenwich Hour Angle (GHA) and declination of the specified body
def predict(values):
    LAT_INDEX = 2

    star = bodyValidator(values)
    if 'error' in values.keys():
        return values
    
    day = dateValidator(values)
    if 'error' in values.keys():
        return values
    
    time = timeValidator(values)
    if 'error' in values.keys():
        return values
    
    greenwichHourAngle = calculateGreenwichHourAngle(day, time)
    starGHA = calculateStarGHA(star, greenwichHourAngle)
    
    values['long'] = starGHA
    values['lat'] = star[LAT_INDEX]

    return values

# Calculates the Greenwich Hour Angle from the SHA of a star and the GHA of Aires
def calculateStarGHA(star, greenwichHourAngle):
    SHA_INDEX = 1
    MAX_DEGREES = 360
    
    return decimalToMinutes((minutesToDecimal(star[SHA_INDEX]) + greenwichHourAngle) % MAX_DEGREES)

# Calculates the Greenwich Hour Angle of Aires
def calculateGreenwichHourAngle(day, time):

    observationYear = getObservationYear(day)

    cumulativeProgression = determineAngularDifference(observationYear)
    leapProgression = accountForLeapYears(observationYear)
    
    primeMeridianRotation = calculatePrimeMeridianLocation(cumulativeProgression, leapProgression)
    angleOfRotation = calculateEarthRotationForYear(day, time)
    
    return primeMeridianRotation + angleOfRotation
    
# Calculates the rotation of the earth since the start of the year until the provided date and time    
def calculateEarthRotationForYear(day, time):
    EARTH_ROTATIONAL_PERIOD = 86164.1
    INITIAL_MONTH = 01
    INITIAL_DAY = 01
    SECONDS_IN_AN_HOUR = 3600
    SECONDS_IN_A_MINUTE = 60
    SECONDS_IN_A_DAY = 86400
    MAX_ROTATION = 360
    
    referenceDate = date(getObservationYear(day), INITIAL_MONTH, INITIAL_DAY)
    currentDate = date(getObservationYear(day), getObservationMonth(day), getObservationDay(day))
    numberOfDaysPassed = (currentDate - referenceDate).days
    
    numberOfSecondsPassedBeforeCurrentDate = (numberOfDaysPassed) * SECONDS_IN_A_DAY
    numberOfSecondsPassedDuringCurrentDate = (SECONDS_IN_AN_HOUR * getObservationHour(time)) + (SECONDS_IN_A_MINUTE * getObservationMinute(time)) + getObservationSecond(time)
    totalSeconds = numberOfSecondsPassedBeforeCurrentDate + numberOfSecondsPassedDuringCurrentDate
    
    return (totalSeconds / EARTH_ROTATIONAL_PERIOD * MAX_ROTATION) % MAX_ROTATION
    
# Calculates how far the prime meridian has rotated since the beginning of the provided year
def calculatePrimeMeridianLocation(cumulativeProgression, leapProgression):
    GHA_AIRES = '100d42.6'
    
    return minutesToDecimal(GHA_AIRES) + cumulativeProgression + leapProgression
    
# Accounts for rotation during leap years between the reference year and the provided year
def accountForLeapYears(observationYear):
    DAILY_ROTATION = '0d59.0'
    REFERENCE_YEAR = 2001
    BALANCE_DECIMAL = 0.001
    numberOfLeapYears = 0
    
    for currentYear in range(REFERENCE_YEAR, observationYear):
        if isleap(currentYear):
            numberOfLeapYears = numberOfLeapYears + 1
    
    return numberOfLeapYears * minutesToDecimal(DAILY_ROTATION) - BALANCE_DECIMAL
    
# Calculates the angular difference, or cumulative progression, for the provided year
def determineAngularDifference(observationYear):
    REFERENCE_YEAR = 2001
    YEARLY_RATE = '0d14.31667'
    
    return (int(observationYear) - REFERENCE_YEAR) * -(minutesToDecimal(YEARLY_RATE))

# Converts degrees + minutes to degrees + fraction
def minutesToDecimal(string):
    STRING_SEPARATOR = "d"
    MINUTES = 60
    
    separatorLoc = string.find(STRING_SEPARATOR)
    degreeRange = separatorLoc
    minuteRange = separatorLoc + 1
    degreeValue = float(string[:degreeRange])
    minuteValue = float(string[minuteRange:])
    if degreeValue < 0:
        return degreeValue - (minuteValue / MINUTES)
    return degreeValue + (minuteValue / MINUTES)

# Converts degrees + fraction to degrees + minutes with a "d" separating the degrees and minutes
def decimalToMinutes(number):
    MINUTES_IN_AN_HOUR = 60
    SIGNIFICANT_FIGURES = 1
    MINIMUM_MINUTE = 0
    stringFormat = '1e' + str(-SIGNIFICANT_FIGURES * SIGNIFICANT_FIGURES)
    
    # Convert the number, and then round the number to the nearest 0.1 arc-minute using 0.5+ rounds upwards
    minutes = MINUTES_IN_AN_HOUR * (number.real - int(number.real))
    minutes = decimal.Decimal(minutes.real)
    minuteForm = minutes.quantize(decimal.Decimal(stringFormat), rounding='ROUND_HALF_UP')
    if float(minuteForm) < MINIMUM_MINUTE:
        minuteForm = -(minuteForm)
        
    return str(int(number.real)) + "d" + str(minuteForm)

# Returns the star in the catalog that matching the body provided
def getStarInCatalog(values):
    STAR_NAME_INDEX = 0
    CATALOG_ERROR = 'star not in catalog'
    body = values['body'].upper()
    starCatalog = getStarCatalog()

    for currentCatalogIndex in range(len(starCatalog)):
        if body == starCatalog[currentCatalogIndex][STAR_NAME_INDEX]:
            catalogStar = starCatalog[currentCatalogIndex]
            return catalogStar

    values['error'] = CATALOG_ERROR

# Validator for the body input parm
def bodyValidator(values):
    BODY_ERROR = 'mandatory information is missing'
    
    if 'body' in values.keys():
        star = getStarInCatalog(values);
        return star
    else:  
        values['error'] = BODY_ERROR

# Validator for the date input parm
def dateValidator(values):
    DEFAULT_DATE = '2001-01-01'
    DATE_ERROR = 'invalid date'
    DATE_DELIMITER = '-'
    DATE_STRING_LENGTH = 10
    FIRST_DELIMITER_INDEX = 4
    SECOND_DELIMITER_INDEX = 7
    
    if 'date' in values.keys():
        day = values['date']
        
        if len(day) != DATE_STRING_LENGTH:
            values['error'] = DATE_ERROR
            return
        
        if day[FIRST_DELIMITER_INDEX] != DATE_DELIMITER or day[SECOND_DELIMITER_INDEX] != DATE_DELIMITER:
            values['error'] = DATE_ERROR
            return
                
        try:
            checkDateDetails(values)
            if 'error' in values.keys():
                return
        except:
            values['error'] = DATE_ERROR

    else:
        day = DEFAULT_DATE        
        
    return day

# Error checks individual components of the date value
def checkDateDetails(values):
    MINIMUM_YEAR = 2001
    MAXIMUM_YEAR = 2100
    MINIMUM_MONTH = 01
    MAXIMUM_MONTH = 12
    MINIMUM_DAY = 01
    DATE_ERROR = 'invalid date'
    date = values['date']
    
    year = getObservationYear(date)
    month = getObservationMonth(date)
    day = getObservationDay(date)
    
    maxDay = calculateMaxDay(year, month)
    if year < MINIMUM_YEAR or year > MAXIMUM_YEAR or month < MINIMUM_MONTH or month > MAXIMUM_MONTH or day < MINIMUM_DAY or day > maxDay:
        values['error'] = DATE_ERROR

# Returns the year of a given date
def getObservationYear(date):
    YEAR_INDEX_END = 4
    
    return int(date[:YEAR_INDEX_END])

# Returns the month of a given date
def getObservationMonth(date):
    MONTH_INDEX_START = 5
    MONTH_INDEX_END = 7
    
    return int(date[MONTH_INDEX_START:MONTH_INDEX_END])

# Returns the day of a given date
def getObservationDay(date):
    DAY_INDEX_START = 8
    DAY_INDEX_END = 10
    
    return int(date[DAY_INDEX_START:DAY_INDEX_END])
   
# Returns the last day of the month for a given month in a given year 
def calculateMaxDay(year, month):
    MAXIMUM_DAY_ODD_MONTH_FIRST_HALF = 31
    MAXIMUM_DAY_ODD_MONTH_SECOND_HALF = 30
    MAXIMUM_DAY_EVEN_MONTH_FIRST_HALF = 30
    MAXIMUM_DAY_EVEN_MONTH_SECOND_HALF = 31
    MAXIMUM_DAY_FEBRUARY_NO_LY = 28
    MAXIMUM_DAY_FEBRUARY__LY = 29
    TURNING_MONTH = 7
    FEBRUARY = 2
    
    if isEvenMonth(month) and month <= TURNING_MONTH:
        if month == FEBRUARY:
            if isleap(year):
                maxDay = MAXIMUM_DAY_FEBRUARY__LY
            else:
                maxDay = MAXIMUM_DAY_FEBRUARY_NO_LY
        else:
            maxDay = MAXIMUM_DAY_EVEN_MONTH_FIRST_HALF
    elif isEvenMonth(month):
        maxDay = MAXIMUM_DAY_EVEN_MONTH_SECOND_HALF
    elif month <= TURNING_MONTH:
        maxDay = MAXIMUM_DAY_ODD_MONTH_FIRST_HALF
    else:
        maxDay = MAXIMUM_DAY_ODD_MONTH_SECOND_HALF
        
    return maxDay
        
# Returns a boolean stating whether a provided month is even or not
def isEvenMonth(month):
    return month % 2 == 0

# Validator for the time input parm
def timeValidator(values):
    DEFAULT_TIME = '00:00:00'
    TIME_ERROR = 'invalid time'
    TIME_DELIMITER = ':'
    TIME_STRING_LENGTH = 8
    FIRST_DELIMITER_INDEX = 2
    SECOND_DELIMITER_INDEX = 5
    
    if 'time' in values.keys():
        time = values['time']
        
        if len(time) != TIME_STRING_LENGTH:
            values['error'] = TIME_ERROR
            return
        
        if time[FIRST_DELIMITER_INDEX] != TIME_DELIMITER or time[SECOND_DELIMITER_INDEX] != TIME_DELIMITER:
            values['error'] = TIME_ERROR
            return
        
        try:
            checkTimeDetails(values)
            if 'error' in values.keys():
                return time
        except:
            values['error'] = TIME_ERROR
            return
        
    else:
        time = DEFAULT_TIME

    return time
  
# Error checks individual components of the time value 
def checkTimeDetails(values):
    MINIMUM_TIME = 00
    MAXIMUM_HOURS = 24
    MAXIMUM_MINUTES = 59
    MAXIMUM_SECONDS = 59
    TIME_ERROR = 'invalid time'
    time = values['time']
    
    hour = getObservationHour(time)
    minute = getObservationMinute(time)
    second = getObservationSecond(time)
    
    if hour < MINIMUM_TIME or hour > MAXIMUM_HOURS or minute < MINIMUM_TIME or minute > MAXIMUM_MINUTES or second < MINIMUM_TIME or second > MAXIMUM_SECONDS:
        values['error'] = TIME_ERROR
 
# Returns the hour of a given time       
def getObservationHour(time):
    HOUR_INDEX_END = 2
    
    return int(time[:HOUR_INDEX_END])

# Returns the minute of a given time
def getObservationMinute(time):
    MINUTE_INDEX_START = 3
    MINUTE_INDEX_END = 5
    
    return int(time[MINUTE_INDEX_START:MINUTE_INDEX_END])

# Returns the second of a given time
def getObservationSecond(time):
    SECOND_INDEX_START = 6
    SECOND_INDEX_END = 8
    
    return int(time[SECOND_INDEX_START:SECOND_INDEX_END])

# Populates a list of lists with the support info for each star
def getStarCatalog():
    ACHERNAR = ['ACHERNAR', '335d25.5', '-57d09.7']
    ACRUX = ['ACRUX', '173d07.2', '-63d10.9']
    ADARA = ['ADARA', '255d10.8', '-28d59.9']
    ALCAID = ['ALCAID', '152d57.8', '49d13.8']
    ALDEBARAN = ['ALDEBARAN', '290d47.1', '16d32.3']
    ALIOTH = ['ALIOTH', '166d19.4', '55d52.1']
    ALNAIR = ['ALNAIR', '27d42.0', '-46d53.1']
    ALNILAM = ['ALNILAM', '275d44.3', '-1d11.8']
    ALPHARD = ['ALPHARD', '217d54.1', '-8d43.8']
    ALPHECCA = ['ALPHECCA', '126d09.9', '26d39.7']
    ALPHERATZ = ['ALPHERATZ', '357d41.7', '29d10.9']
    ALTAIR = ['ALTAIR', '62d06.9', '8d54.8']
    ANKAA = ['ANKAA', '353d14.1', '-42d13.4']
    ANTARES = ['ANTARES', '112d24.4', '-26d27.8']
    ARCTURUS = ['ARCTURUS', '145d54.2', '19d06.2']
    ATRIA = ['ATRIA', '107d25.2', '-69d03.0']
    AVIOR = ['AVIOR', '234d16.6', '-59d33.7']
    BELLATRIX = ['BELLATRIX', '278d29.8', '6d21.6']
    BETELGEUSE = ['BETELGEUSE', '270d59.1', '7d24.3']
    CANOPUS = ['CANOPUS', '263d54.8', '-52d42.5']
    CAPELLA = ['CAPELLA', '280d31.4', '46d00.7']
    DENEB = ['DENEB', '49d30.7', '45d20.5']
    DENEBOLA = ['DENEBOLA', '182d31.8', '14d28.9']
    DIPHDA = ['DIPHDA', '348d54.1', '-17d54.1']
    DUBHE = ['DUBHE', '193d49.4', '61d39.5']
    ELNATH = ['ELNATH', '278d10.1', '28d37.1']
    ENIF = ['ENIF', '33d45.7', '9d57.0']
    ETAMIN = ['ETAMIN', '90d45.9', ' 51d29.3']
    FOMALHAUT = ['FOMALHAUT', '15d22.4', '-29d32.3']
    GACRUX = ['GACRUX', '171d58.8', '-57d11.9']
    GIENAH = ['GIENAH', '175d50.4', '-17d37.7']
    HADAR = ['HADAR', '148d45.5', '-60d26.6']
    HAMAL = ['HAMAL', '327d58.7', '23d32.3']
    KAUS_AUSTRALIS = ['KAUS AUSTRALIS', '83d41.9', '-34d22.4']
    KOCHAB = ['KOCHAB', '137d21.0', '74d05.2']
    MARKAB = ['MARKAB', '13d36.7', '15d17.6']
    MENKAR = ['MENKAR', '314d13.0', '4d09.0']
    MENKENT = ['MENKENT', '148d05.6', '-36d26.6']
    MIAPLACIDUS = ['MIAPLACIDUS', '221d38.4', '-69d46.9']
    MIRFAK = ['MIRFAK', '308d37.4', '49d55.1']
    NUNKI = ['NUNKI', '75d56.6', '-26d16.4']
    PEACOCK = ['PEACOCK', '53d17.2', '-56d41.0']
    POLARIS = ['POLARIS', '316d41.3', '89d20.1']
    POLLUX = ['POLLUX', '243d25.2', '27d59.0']
    PROCYON = ['PROCYON', '244d57.5', '5d10.9']
    RASALHAGUE = ['RASALHAGUE', '96d05.2', '12d33.1']
    REGULUS = ['REGULUS', '207d41.4', '11d53.2']
    RIGEL = ['RIGEL', '281d10.1', '-8d11.3']
    RIGIL_KENTAURUS = ['RIGIL KENTAURUS', '139d49.6', '-60d53.6']
    SABIK = ['SABIK', '102d10.9', '-15d44.4']
    SCHEDAR = ['SCHEDAR', '349d38.4', '56d37.7']
    SHAULA = ['SHAULA', '96d20.0', '-37d06.6']
    SPICA = ['SPICA', '158d29.5', '-11d14.5']
    SIRIUS = ['SIRIUS', '258d31.7', '-16d44.3']
    SUHAIL = ['SUHAIL', '222d50.7', '-43d29.8']
    VEGA = ['VEGA', '80d38.2', '38d48.1']
    ZUBENELGENUBI = ['ZUBENELGENUBI', '137d03.7', '-16d06.3']
    
    CATALOG = [ACHERNAR, ACRUX, ADARA, ALCAID, ALDEBARAN, ALIOTH, ALNAIR, ALNILAM, ALPHARD, ALPHECCA, ALPHERATZ, ALTAIR, ANKAA, ANTARES, ARCTURUS, ATRIA, AVIOR, BELLATRIX,
               BETELGEUSE, CANOPUS, CAPELLA, DENEB, DENEBOLA, DIPHDA, DUBHE, ELNATH, ENIF, ETAMIN, FOMALHAUT, GACRUX, GIENAH, HADAR, HAMAL, KAUS_AUSTRALIS, KOCHAB, MARKAB,
               MENKAR, MENKENT, MIAPLACIDUS, MIRFAK, NUNKI, PEACOCK, POLARIS, POLLUX, PROCYON, RASALHAGUE, REGULUS, RIGEL, RIGIL_KENTAURUS, SABIK, SCHEDAR, SHAULA, SPICA,
               SIRIUS, SUHAIL, VEGA, ZUBENELGENUBI]
    
    return CATALOG