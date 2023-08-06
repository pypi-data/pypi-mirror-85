
import re
import datetime

# For immutable types we started out using a variation on namedtuple, inspired
# by the code at:
# http://blog.thomnichols.org/2010/12/lightweight-data-types-in-python
# and also the source code for namedtuple:
# http://svn.python.org/view/python/branches/release26-maint/Lib/collections.py?revision=72955&view=markup
# Downside was that namedtuple required Python 2.6+, it wasn't so great for
# documentation (parameters specified as strings), it prohibited or at least
# made it difficult for us to have our own inheritance hierarchy, we couldn't
# have private fields in our immutable subclasses, we didn't have complete
# control over all methods, type-checking of constructor args involved
# implementing __new__ which was messy, and we had to override __slots__ in
# subclasses to prevent the overhead of a dict (we need to do that with a
# superclass too, but the point is that using this namedtuple thing didn't
# eliminate unnecessary code).
# So we shifted over to subclassing the following Immutable class instead. In
# commit 62 we got rid of all use of the original namedtuple approach, and
# removed that code from this module. 
#
# Good idea for subclasses to override __repr__ and possibly __str__ if they 
# want a shorter friendly string (by default __str__ will just use __repr__).
# Don't worry too much about making __repr__ return something that can be used
# to re-create the object using eval, but since it seems that is the ideal case,
# you might as well use that kind of object-creation format when possible.
# See notes at:
# http://stackoverflow.com/questions/1436703/
class Immutable(object):
    __slots__ = ()
    # If there's one field this can just return it; otherwise it should return
    # a tuple of all fields.
    def _equalityFields(self):
        raise NotImplementedError()
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self._equalityFields() == other._equalityFields()
    def __ne__(self, other):
        return not (self == other)
    def __hash__(self):
        # For many of our subclasses we get less hash collisions if we include
        # the class type in the hash.  Otherwise, say,
        # DatedBreakdown.daily(Period.latestValues(1)) and
        # DatedBreakdown.monthly(Period.latestValues(1))
        # would have the same hash.
        # We include the class in the hash always for now.  We could of course
        # make it optional later if we wanted to.
        fields = self._equalityFields()
        if type(fields) is tuple:
            return hash((self.__class__,) + fields)
        else: # fields is just one field, not in a tuple
            return hash((self.__class__, fields))

# Wraps the exception that is currently being handled (in an except block) and
# raises the wrapped version with a proper stack trace.
# Python 3 has "raise WrapperException from cause" but that won't work in 2.
# This basically has the same effect though, and works in 2.
def raiseWrapped(wrapperExceptionClass, message=None):
    import sys
    info = sys.exc_info() # get info on current exception
    newException = wrapperExceptionClass(message)
    # __cause__ is a python 3 property that gets added automatically with
    # raise WrapperException from cause
    # info[1] lets us access it from the last exception.
    newException.__cause__ = info[1]
    try:
        # Try the python 3 way of setting the stack trace first
        newException.with_traceback(info[2])
    except:
        # Need to put below in exec otherwise it won't compile in Python 3.
        # See https://docs.python.org/2.0/ref/raise.html for the syntax
        exec('raise newException, None, info[2]')
    # If it's got here, with_traceback worked so we just raise that.
    raise newException

# Work out once whether we have viewkeys and viewvalues, as although they say
# exceptions are cheap, they mean the try/except blocks are cheap...  If an
# exception is thrown, it's expensive:
# http://stackoverflow.com/questions/8107695/
def _runHasDictViews():
    testDict = {'key': 5}
    try:
        testDict.viewkeys()
        testDict.viewvalues()
        # It's Python 2, 2.7 or later
        return True
    except:
        # It's either Python 2 before 2.7, or python 3
        return False
_hasDictViews = _runHasDictViews()

def _runHasDictIterMethods():
    testDict = {'key': 5}
    try:
        testDict.iterkeys()
        testDict.itervalues()
        testDict.iteritems()
        # It's Python 2, 2.2 or later.
        return True
    except:
        # It's Python 2 before 2.2 or Python 3
        return False
_hasDictIterMethods = _runHasDictIterMethods()

# This will only work as expected if dictObject won't change.  Otherwise the
# view (python 2.7+ only) will change with it.  Note that viewkeys and
# viewvalues are gone in Python 3, where keys() and values() simply return a
# view instead.
def getSafeDictKeys(dictObject):
    if _hasDictViews:
        return dictObject.viewkeys()
    else:
        return dictObject.keys()
    
def getSafeDictValues(dictObject):
    if _hasDictViews:
        return dictObject.viewvalues()
    else:
        return dictObject.values()
    
def getDictValuesIterable(dictObject):
    if _hasDictIterMethods:
        # Python 2 (2.2 or later) for fast iterating over the values.
        return dictObject.itervalues()
    else:
        # Python 3 by default values returns an iterator.
        return dictObject.values()
    
def getDictItemsIterable(dictObject):
    if _hasDictIterMethods:
        return dictObject.iteritems()
    else:
        # In Python 3, items returns the same as iteritems used to.
        return dictObject.items()
 
# This must calculate the hash of the values in an order-independent way.   
def getDictValuesHash(dictObject, startingHashCode=0):
    hashCode = startingHashCode
    for v in getDictValuesIterable(dictObject):
        # This must be order-independent
        hashCode += hash(v)
    # Before python 2.2 (earlier than this library covers), Python int
    # operations used to result in an error if they got big or small enough
    # to overflow.  They never overflowed automatically like Java ints.
    # Before 3 they automatically turn into longs, after 3 then there is no
    # difference between ints and longs anyway - they're both the int type:
    # http://www.python.org/dev/peps/pep-0237/
    # http://stackoverflow.com/questions/4581842/
    # http://stackoverflow.com/questions/2104884/
    # The docs for __hash__ say it should return an integer, but that, since
    # 2.5 it can return a long, and the system will use the 32-bit hash of
    # that object.  See:
    # http://docs.python.org/2/reference/datamodel.html#object.__hash__
    # To make this work for Python 2.2 to 2.5, we check for int and return
    # the hash if it isn't one (because presumably it's a long).
    # We don't worry about pre-2.2 at all - that may throw an overflow
    # error above.
    if isinstance(hashCode, int):
        return hashCode
    else:
        return hash(hashCode)
    
class Attribute(Immutable):
    __slots__ = ('__name', '__value')
    def __init__(self, name, value):
        self.__name = name
        self.__value = value
    def _equalityFields(self):
        return (self.__name, self.__value)
    @property
    def name(self): return self.__name
    @property
    def value(self): return self.__value
    def appendString(self, s):
        s.append(self.__name)
        s.append("=\"")
        s.append(self.__value)
        s.append("\"")
    
class XmlElement(object):

    def __init__(self, qName):
        # NB below is how you define instance variables in python - if you put
        # them above they're class variables (i.e. like static in Java).
        self.qName = qName
        self.attributes = []
        # can contain XmlElement or string because you can add a string child.
        self.children = []
        self.value = None
    
    def addAttribute(self, name, value):
        self.attributes.append(Attribute(name, str(value)))
        return self


    def _addChildImpl(self, child):
        if (self.value):
            raise ValueError(
                "Can't have a String value and child elements together")
        self.children.append(child)
        return self
   

    def addXmlStringAsChild(self, xmlString):
        self._addChildImpl(xmlString)
        
    # This returns this, not the child, as coding made it clear that that was
    # more useful.  Don't confuse it with newChild which returns the
    # child.
    def addChild(self, child):
        return self._addChildImpl(child)

    def newChild(self, qName):
        newChild = XmlElement(qName)
        return self.addChild(newChild)

    def setValue(self, value):
        # check if list is empty
        # http://stackoverflow.com/questions/53513/
        if (self.children):
            raise ValueError(
                    "Can't have child elements and a String value together")
        self.value = str(value)
        return self

    def appendXmlString(self, stringList):
        stringList.append("<")
        stringList.append(self.qName)
        for a in self.attributes:
            stringList.append(" ")
            a.appendString(stringList)
        if (not self.children and not self.value):
            stringList.append("/>")
        else:
            stringList.append(">")
            if (self.value):
                stringList.append(self.value)
            else:
                for c in self.children:
                    if isinstance(c, XmlElement):
                        c.appendXmlString(stringList)
                    else:
                        stringList.append(c)
            stringList.append("</")
            stringList.append(self.qName)
            stringList.append(">")

    def toXmlString(self):
        # making a list and joining seems to be an efficient way to make a big
        # python string.
        # http://www.skymind.com/~ocrow/python_string/
        stringList = []
        self.appendXmlString(stringList)
        return ''.join(stringList)

# From http://stackoverflow.com/questions/11301138/
try:
    basestring  # attempt to evaluate basestring
    def isString(s):
        return isinstance(s, basestring)
except NameError:
    def isString(s):
        return isinstance(s, str)

def logSafe(string):
    return string # TODO

def __getExampleCode(exampleCodeOrNone):
    if exampleCodeOrNone is None:
        return ''
    else:
        return ' (e.g. ' + exampleCodeOrNone + ')'

def fullNameOfClass(cls):
    # auto-imported classes like str have module __builtin__.  But that's a bit
    # confusing in error messages.  Below is how we test for that, to exclude
    # it.  __module__ can also be None according to the docs.
    if cls.__module__ is None or cls.__module__ == str.__class__.__module__:
        return cls.__name__
    return cls.__module__ + '.' + cls.__name__

def wrongTypeString(param, paramName, expectedType, exampleCodeOrNone=None):
    # str of a type is like <type 'object'>
    return ('%s has type %s, when it should have type %s%s.' % 
        (paramName, fullNameOfClass(param.__class__), 
            fullNameOfClass(expectedType), __getExampleCode(exampleCodeOrNone)))

def wrongSupertypeString(param, paramName, expectedType, 
        exampleCodeOrNone=None):
    return ('%s has type %s, when it should be a subclass of %s%s.' % 
        (paramName, fullNameOfClass(param.__class__), 
            fullNameOfClass(expectedType), __getExampleCode(exampleCodeOrNone)))

# Precompiling doesn't actually make all that much difference, but it is
# faster.
# We're using match to test against this, and match looks for a match at the
# beginning.  So we don't need a ^, but we do need a $ (so as not to match
# a valid string with invalid stuff after it).
_STATION_ID_REGEXP_STRING = '[a-zA-Z0-9_-]{1,60}$' 
_STATION_ID_REGEXP = re.compile(_STATION_ID_REGEXP_STRING)
def checkStationId(stationId, beTolerant):
    if not isString(stationId):
        # Refer to it as 'station ID' - that way this works for methods that
        # take stationId and/or id.
        raise TypeError('The station ID should be a str.')
    if beTolerant:
        stationId = stationId.strip()
    if not _STATION_ID_REGEXP.match(stationId):
        raise ValueError('Invalid station ID (%r) - it should match the '
            'regular expression %s.' %
                (logSafe(stationId), _STATION_ID_REGEXP_STRING))
    return stationId

try:
    intTypes = (int, long)
except:
    # Python 3, where there is no long type.
    intTypes = int
    
try:
    import numbers
    numericTypes = numbers.Number
except:
    # Python 2, before 2.6
    try:
        import decimal
        # Python 2.4 or later
        numericTypes = (int, long, float, decimal.Decimal)
    except:
        # Before Python 2.4
        numercTypes = (int, long, float)
        
try:
    from math import isnan, isinf # if this works we're on 2.6+
except:
    def isnan(number):
        return (number != number)
    # found this worked on Python 2.5 whilst float('inf') did not.
    # At http://stackoverflow.com/questions/2919754/ it says that float('inf')
    # is guaranteed to work on 2.6, but that's pretty much irrelevant since on
    # 2.6 we have math.isinf anyway.
    plusInf = 1e30000
    minusInf = -plusInf
    def isinf(number):
        return (number == plusInf or number == minusInf)

def isAllDigits(s):
    for c in s:
        asciiCode = ord(c)
        # 0 has ASCII code 48, 9 has 57
        if asciiCode < 48 or asciiCode > 57:
            return False
    return True

def strictParseInt(s):
    if not isAllDigits(s):
        raise ValueError('Invalid int string %s' % s)
    return int(s)

def checkNumeric(param, paramName):
    if not isinstance(param, numericTypes):
        raise TypeError('%s should be a numeric type, but it was of type %s.' %
                        (paramName, fullNameOfClass(param.__class__)))
    elif isnan(param):
        raise ValueError('%s cannot be NaN.' % paramName)
    elif isinf(param):
        raise ValueError('%s cannot be +inf or -inf.' % paramName)
    return param

# This is not tolerant of floats as that could mask bugs.
def checkInt(param, paramName):
    if not isinstance(param, intTypes):
        raise TypeError('%s should be an int, but it was of type %s.' %
            (paramName, fullNameOfClass(param.__class__)))
    return param

def checkString(param, paramName):
    if not isString(param):
        raise TypeError('%s should be a string, but it was of type %s.' %
            (paramName, fullNameOfClass(param.__class__)))
    return param

def checkBoolean(param, paramName):
    if not isinstance(param, bool):
        raise TypeError('%s should be a boolean (True or False), but it was '
            'of type %s.' % (paramName, fullNameOfClass(param.__class__)))
    return param

def checkDate(param, paramName):
    if type(param) is not datetime.date:
        raise TypeError('%s should be a datetime.date, but it was of type %s.' %
            (paramName, fullNameOfClass(param.__class__)))
    return param

def checkDatetime(param, paramName):
    if type(param) is not datetime.datetime:
        raise TypeError('%s should be a datetime.datetime, but it was of type %s.' %
            (paramName, fullNameOfClass(param.__class__)))
    return param

def checkDict(param, paramName):
    if not isinstance(param, dict):
        raise TypeError('%s should be a dict, but it was of type %s.' %
            (paramName, fullNameOfClass(param.__class__)))
    return param

def checkTupleItems(tupleToCheck, checkMethod, paramName):
    for i in range(len(tupleToCheck)):
        try:
            checkMethod(tupleToCheck[i])
        except:
            checkMethod(tupleToCheck[i], '%s[%d]' % (paramName, i))
    return tupleToCheck



# TIME STUFF BELOW.  We put it here instead of in degreedays.time because we don't
# want the source of the public API to be confused by a load of internal stuff.

def formatUtcOffset(offset):
    # we don't use offset.total_seconds() cos it was only added in 3.2
    totalMinutes = (offset.days * 1440) + (offset.seconds // 60)
    if totalMinutes < 0:
        sign = '-'
        modTotalMinutes = -totalMinutes
    elif totalMinutes > 0:
        sign = '+'
        modTotalMinutes = totalMinutes
    else:
        return 'Z'
    split = divmod(modTotalMinutes, 60)
    return '%s%02d:%02d' % (sign, split[0], split[1])

def parseUtcOffset(isoString):
    if isoString == 'Z':
        return datetime.timedelta(minutes=0)
    if len(isoString) == 6 and isoString[3] == ':':
        # expecting e.g. -08:00
        hoursString = isoString[1:3]
        minutesString = isoString[4:6]
        if isAllDigits(hoursString) and \
                isAllDigits(minutesString):
            hours = int(hoursString)
            minutes = int(minutesString)
            if hours >= 0 and hours <= 23 and \
                    minutes >= 0 and minutes <= 59:
                totalMinutes = (hours * 60) + minutes
                if totalMinutes <= 1080:
                    signChar = isoString[0]
                    if signChar == '-':
                        return datetime.timedelta(minutes=-totalMinutes)
                    elif signChar == '+':
                        return datetime.timedelta(minutes=totalMinutes)
    raise ValueError(('Invalid isoString (%s) - this expects an ISO-format '
        'string like Z for UTC, or -08:00 for 8 hours behind UTC, or '
        '+06:30 for 6 and a half hours ahead of UTC.  The maximum '
        'allowed is +18:00 and the minimum is -18:00.') % isoString)

# This isn't just a function that parses datetime strings, it's an object
# so that it can also cache datetime.timezone/degreedays.time._TimeZone
# objects for reuse, so we can parse a load of datetimes without them each
# having their own separate timezone object.
# It takes the function to create a tzinfo subclass from, so as not to have
# a circular dependency on degreedays.time module.
# Not thread safe, best use from one thread only.
class IsoDateTimeParser(object):
    __slots__= ('__createTimeZoneFromOffset', '__tzstrToTimeZoneDict')
    def __init__(self, createTimeZoneFromOffset):
        self.__createTimeZoneFromOffset = createTimeZoneFromOffset
        self.__tzstrToTimeZoneDict = {}
    def __getValueErrorMessage(self, isoString):
        return ('Invalid isoString (%s) - this expects ISO format to the '
            'level of minutes (i.e. no seconds etc.), e.g. 2020-08-26T20:45Z '
            '(for the UTC time-zone) or 2020-08-26T12:45-08:00 (for an '
            'explicit timezone expressed in terms of the hours and minutes '
            'offset from UTC, with a minimum of -18:00 and a maximum of '
            '+18:00).') % isoString
    def parse(self, isoString):
        checkString(isoString, 'str')
        # possible lengths:
        # YYYY-MM-DDTHH:MMZ - 17 chars
        # YYYY-MM-DDTHH:MM-08:00 - 22 chars
        length = len(isoString)
        if length == 22:
            tzstr = isoString[-6:]
        elif length == 17:
            tzstr = isoString[-1:]
        else:
            raise ValueError(self.__getValueErrorMessage(isoString))
        try:
            timeZone = self.__tzstrToTimeZoneDict[tzstr]
        except KeyError:
            try:
                timeZone = self.__createTimeZoneFromOffset(
                    parseUtcOffset(tzstr))
            except ValueError:
                raise ValueError(self.__getValueErrorMessage(isoString))
            self.__tzstrToTimeZoneDict[tzstr] = timeZone
        # We parse manually.  We would use:
        # dt = datetime.datetime.strptime(localStr, '%Y-%m-%dT%H:%M')
        # but in Python 2.5 we often get "AttributeError: strptime", which I
        # think may be something to do with
        # https://bugs.python.org/issue7980
        # strptime seems to work OK in 2.6.4, but, given what it says at the
        # link above I don't trust it to work consistently in multiple threads,
        # so let's be cautious and do it ourselves.
        # Y Y Y Y - M M - D D  T  H  H  :  M  M
        # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
        if isoString[4] == '-' and isoString[7] == '-' and \
                isoString[10] == 'T' and isoString[13] == ':':
            try:
                return datetime.datetime(
                    strictParseInt(isoString[0:4]),
                    strictParseInt(isoString[5:7]),
                    strictParseInt(isoString[8:10]),
                    strictParseInt(isoString[11:13]),
                    strictParseInt(isoString[14:16]),
                    0, # second
                    0, # microsecond
                    timeZone)
            except ValueError:
                pass # just raise our own below
        raise ValueError(self.__getValueErrorMessage(isoString))

def formatDateTime(dt):
    # Like for the parser above, we avoid doing
    # dt.strftime('%Y-%m-%dT%H:%M')
    # because it causes problems in Python 2.5.  This is simple enough and it
    # works well.  Also by using it we don't have to deal with the Python 2.7
    # issue that it can't format years before 1900:
    # https://bugs.python.org/issue1777412
    s = '%04d-%02d-%02dT%02d:%02d' % (dt.year, dt.month, dt.day, 
        dt.hour, dt.minute)     
    offset = dt.utcoffset()
    if offset is not None:
        s += formatUtcOffset(offset)
    return s