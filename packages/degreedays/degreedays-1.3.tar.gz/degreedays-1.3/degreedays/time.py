
#from datetime import date

from degreedays._private import Immutable
from degreedays._private import XmlElement
import degreedays._private as private
import datetime

__all__ = ['DayRange', 'DayRanges', 'DayOfWeek', 'StartOfMonth', 'StartOfYear']

_DAY_RANGE_EXAMPLE = ('DayRange(datetime.date(2012, 1, 1), '
        'datetime.date(2012, 11, 30)) '
    'or DayRange.singleDay(datetime.date.today() - datetime.timedelta(1)) '
    '(for yesterday only)')
# using datetime.date is perfect for us as it's timezone independent and immutable
class DayRange(Immutable):
    __slots__ = ('__first', '__last')
    def __init__(self, first, last):
        self.__first = private.checkDate(first, 'first')
        if last is not first:
            private.checkDate(last, 'last')
            if (first > last):
                raise ValueError("first (%r) cannot be > last (%r)" % (first, last))
        self.__last = last
    def _equalityFields(self):
        return (self.__first, self.__last)
    @classmethod
    def singleDay(cls, firstAndLast):
        return DayRange(firstAndLast, firstAndLast)
    @property
    def first(self): return self.__first
    @property
    def last(self): return self.__last
    def __containsDate(self, testDate):
        return (testDate >= self.__first and testDate <= self.__last)
    def contains(self, testDateOrDayRange):
        if type(testDateOrDayRange) is datetime.date:
            return self.__containsDate(testDateOrDayRange)
        elif type(testDateOrDayRange) is DayRange:
            return (self.__containsDate(testDateOrDayRange.first) and
                self.__containsDate(testDateOrDayRange.last))
        else:
            raise ValueError(('testDateOrDayRange should be either a '
                'datetime.date or a degreedays.time.DayRange, not a %s.') %
                private.fullNameOfClass(testDateOrDayRange.__class__))
    def __len__(self):
        return (self.last - self.first).days + 1
    def __iter__(self):
        for i in range(len(self)):
            yield self.first + datetime.timedelta(days=i)
    def __repr__(self):
        return 'DayRange(%r, %r)' % (self.__first, self.__last)
    def __str__(self):
        return '%s to %s' % (self.__first, self.__last)
    def _toXml(self, elementName = 'DayRange'):
        return XmlElement(elementName) \
                .addAttribute("first", self.__first.isoformat()) \
                .addAttribute("last", self.__last.isoformat())
    @classmethod
    def _check(cls, param, paramName='dayRange'):
        if type(param) is not DayRange:
            raise TypeError(private.wrongTypeString(param, paramName,
                DayRange, _DAY_RANGE_EXAMPLE))
        return param

_DAY_RANGES_EXAMPLE = ('DayRanges('
    'DayRange(datetime.date(2020, 1, 1), datetime.date(2020, 3, 31)), '
    'DayRange(datetime.date(2020, 4, 1), datetime.date(2020, 6, 30)))')
class _DayRangesTupleBuilder(Immutable):
    __slots__ = ('__list', 'isContiguous', '__lastAddedOrNone')
    def __init__(self):
        self.__list = []
        self.isContiguous = True
        self.__lastAddedOrNone = None
    def add(self, item):
        if type(item) is DayRange:
            if self.__lastAddedOrNone is not None:
                daysAfter = (item.first - self.__lastAddedOrNone.last).days
                if daysAfter > 1:
                    self.isContiguous = False
                elif daysAfter <= 0:
                    raise ValueError(('Problem DayRange items: %s cannot be '
                        'followed by %s because DayRange items must be in '
                        'in chronological order, without overlap.') % \
                        (self.__lastAddedOrNone, item))
            self.__list.append(item)
            self.__lastAddedOrNone = item
        elif private.isString(item):
            DayRange._check(item,
                'An item passed into the DayRanges constructor')
        else:
            # assume it's a sequence, just let it throw error if not
            for innerItem in item:
                self.add(innerItem)
    def build(self):
        return tuple(self.__list)

class DayRanges(Immutable):
    __slots__ = ('__dayRanges', '__isContiguous')
    def __init__(self, *args):
        builder = _DayRangesTupleBuilder()
        for arg in args:
            builder.add(arg)
        self.__dayRanges = builder.build()
        if len(self.__dayRanges) == 0:
            raise ValueError('Must have at least one DayRange.')
        self.__isContiguous = builder.isContiguous
    def _equalityFields(self):
        return self.__dayRanges
    @property
    def isContiguous(self):
        return self.__isContiguous
    @property
    def fullRange(self):
        return DayRange(self.__dayRanges[0].first, self.__dayRanges[-1].last)
    def __len__(self):
        return len(self.__dayRanges)
    def __iter__(self):
        return self.__dayRanges.__iter__()
    def __getitem__(self, index):
        return self.__dayRanges[index]
    def __str__(self):
        length = len(self.__dayRanges)
        return 'DayRanges(%d value%s covering %s)' % (length,
            's' if length > 1 else '', self.fullRange)
    def __repr__(self):
        # self.__dayRanges is a tuple so that will add brackets.  But we don't
        # need double brackets, so we do DayRanges%r instead of DayRanges(%r).
        return 'DayRanges%r' % (self.__dayRanges,)
    def _toXml(self, elementName = 'DayRanges'):
        e = XmlElement(elementName)
        for range in self.__dayRanges:
            e.addChild(range._toXml())
        return e
    @classmethod
    def _check(cls, param, paramName='dayRanges'):
        if type(param) is not DayRanges:
            raise TypeError(private.wrongTypeString(param, paramName,
                DayRange, _DAY_RANGES_EXAMPLE))
        return param

_DAY_OF_WEEK_EXAMPLE = ('DayOfWeek.MONDAY, DayOfWeek.TUESDAY, ..., or '
    'DayOfWeek(0) for Monday etc. (using the int constants that Python uses in '
    'its calendar module)')
# This metaclass stuff is to make it possible to iterate over the values, like
# "for dow in DayOfWeek".  See TemperatureUnit for an explanation and
# references.
class _DayOfWeekMetaclass(type):
    def __iter__(self):
        for i in range(7):
            yield DayOfWeek(i)
_DayOfWeekSuper = _DayOfWeekMetaclass('_DayOfWeekSuper', (Immutable,),
    {'__slots__': ()})            
class DayOfWeek(_DayOfWeekSuper):
    __slots__ = ('__index', '__name', '__nameUpper', '__isoIndex')
    __map = {}
    # Below are set later.  We want them defined here as class variables so that
    # they show up in intellisense if you type "DayOfWeek.".
    MONDAY = None
    TUESDAY = None
    WEDNESDAY = None
    THURSDAY = None
    FRIDAY = None
    SATURDAY = None
    SUNDAY = None
    def __init__(self, index):
        if index == 0:
            self.__name = 'Monday'
        elif index == 1:
            self.__name = 'Tuesday'
        elif index == 2:
            self.__name = 'Wednesday'
        elif index == 3:
            self.__name = 'Thursday'
        elif index == 4:
            self.__name = 'Friday'
        elif index == 5:
            self.__name = 'Saturday'
        elif index == 6:
            self.__name = 'Sunday'
        else:
            raise ValueError('Invalid int value for day of week (%r) - '
                'expecting int between 0 (Monday) and 6 (Sunday).')
        self.__nameUpper = self.__name.upper()
        self.__index = index
        self.__isoIndex = index + 1
    # We need this because of the way we're caching values and allowing direct
    # use of the constructor with indexes (e.g. DayOfWeek(0) for Monday) so we
    # can take the int contsants python's calendar module uses.  This prevents
    # direct use of the constructor from creating a new instance each time.
    def __new__(cls, index):
        existing = DayOfWeek.__map.get(index, None)
        if existing is not None:
            return existing
        newItem = super(DayOfWeek, cls).__new__(cls)
        # We don't need to call __init__... python does it for us after this
        # __new__ method has returned the un-initialized item.  And it passes
        # the index parameter to __init__ as well.
        DayOfWeek.__map[index] = newItem
        return newItem
    def _equalityFields(self):
        return self.__index,
    @property
    def index(self): return self.__index
    @property
    def isoIndex(self): return self.__isoIndex
    def __str__(self):
        return self.__name
    def __repr__(self):
        return 'DayOfWeek.' + self.__nameUpper
    @classmethod
    def _check(cls, param, paramName='dayOfWeek'):
        if type(param) is not DayOfWeek:
            raise TypeError(private.wrongTypeString(param, paramName,
                DayOfWeek, _DAY_OF_WEEK_EXAMPLE))
        return param   
DayOfWeek.MONDAY = DayOfWeek(0)
DayOfWeek.TUESDAY = DayOfWeek(1)
DayOfWeek.WEDNESDAY = DayOfWeek(2)
DayOfWeek.THURSDAY = DayOfWeek(3)
DayOfWeek.FRIDAY = DayOfWeek(4)
DayOfWeek.SATURDAY = DayOfWeek(5)
DayOfWeek.SUNDAY = DayOfWeek(6)              

_START_OF_MONTH_EXAMPLE = ("StartOfMonth(1) for regular calendar months "
    "starting on the 1st of each month, "
    "StartOfMonth(2) for the \"months\" starting on the 2nd of each month, "
    "etc.")
class StartOfMonth(Immutable):
    __slots__ = ('__dayOfMonth',)
    def __init__(self, dayOfMonth):
        private.checkInt(dayOfMonth, 'dayOfMonth')
        if (dayOfMonth < 1 or dayOfMonth > 28):
            raise ValueError('Invalid dayOfMonth (' +
                str(dayOfMonth) + ') - it cannot be less than 1 '
                'or greater than 28 (to ensure it can work for all '
                'months of all years).')
        self.__dayOfMonth = dayOfMonth
    def _equalityFields(self):
        return self.__dayOfMonth
    @property
    def dayOfMonth(self): return self.__dayOfMonth
    def __repr__(self):
        return 'StartOfMonth(%d)' % self.__dayOfMonth
    def __str__(self):
        return '---%02d' % self.__dayOfMonth
    @classmethod
    def _check(cls, param, paramName='startOfMonth'):
        if type(param) is not StartOfMonth:
            raise TypeError(private.wrongTypeString(param, paramName,
                StartOfMonth, _START_OF_MONTH_EXAMPLE))
        return param
    
def _minNoDaysInMonth(monthOfYear):
    return [
        0, # dummy value, just so the first month index is 1.
        31, # Jan
        29, # Feb
        31, # Mar
        30, # Apr
        31, # May
        30, # Jun
        31, # Jul
        31, # Aug
        30, # Sep
        31, # Oct
        30, # Nov
        31 # Dec
    ][monthOfYear]

_START_OF_YEAR_EXAMPLE = ("StartOfYear(1, 1) for regular calendar years "
    "starting on the 1st of January, "
    "StartOfYear(4, 6) for \"years\" starting on the 6th of April, etc.")
class StartOfYear(Immutable):
    __slots__ = ('__monthOfYear', '__dayOfMonth')
    def __init__(self, monthOfYear, dayOfMonth):
        private.checkInt(monthOfYear, 'monthOfYear')
        private.checkInt(dayOfMonth, 'dayOfMonth')
        if (monthOfYear < 1 or monthOfYear > 12):
            raise ValueError('Invalid monthOfYear (' + str(monthOfYear) +
                ') - it cannot be less than 1 (January) or greater than 12 '
                '(December).')
        if (dayOfMonth < 1):
            raise ValueError('Invalid dayOfMonth (' + str(dayOfMonth) +
                ') - it cannot be less than 1.')
        if (monthOfYear == 2 and dayOfMonth > 28):
            raise ValueError('Invalid dayOfMonth (' + str(dayOfMonth) + ') - '
                'when when the month is February (2), the day cannot be '
                'greater than 28.')
        noDaysInMonth = _minNoDaysInMonth(monthOfYear)
        if (dayOfMonth > noDaysInMonth):
            raise ValueError('Invalid dayOfMonth (' + str(dayOfMonth) +
                ') - it cannot be greater than ' + str(noDaysInMonth) +
                ' when the month is ' + str(monthOfYear) + '.')
        self.__monthOfYear = monthOfYear
        self.__dayOfMonth = dayOfMonth
    def _equalityFields(self):
        return (self.__monthOfYear, self.__dayOfMonth)
    @property
    def monthOfYear(self): return self.__monthOfYear
    @property
    def dayOfMonth(self): return self.__dayOfMonth
    def __repr__(self):
        return 'StartOfYear(%d, %d)' % (self.__monthOfYear, self.__dayOfMonth)
    def __str__(self):
        return '--%02d-%02d' % (self.monthOfYear, self.dayOfMonth)
    @classmethod
    def _check(cls, param, paramName='startOfYear'):
        if type(param) is not StartOfYear:
            raise TypeError(private.wrongTypeString(param, paramName,
                StartOfYear, _START_OF_YEAR_EXAMPLE))
        return param

# Like datetime.timezone, but works in Python < 3.2.  Private because some
# day we may want to discontinue it and use only datetime.timezone instead.
# But we keep it here as opposed to putting it in _private.py because we want
# a good namespace for pickling.  Pickling is important for this because it
# goes inside datetime objects, and, as those are part of standard python,
# people will probably expect to be able to pickle them.
class _TimeZone(Immutable, datetime.tzinfo):
    __slots__ = ('__offset')
    # See datetime.timezone for and tzinfo docs for this curious structure.
    # We need a no-args init for pickling, says tzinfo.
    def __new__(cls, offset):
        if type(offset) is not datetime.timedelta:
            raise ValueError('Expecting a datetime.timedelta')
        # we don't use offset.total_seconds() cos it was only added in 3.2
        totalMinutes = (offset.days * 1440) + (offset.seconds // 60)
        if totalMinutes < -1080 or totalMinutes > 1080:
            raise ValueError(('Invalid offset (%s) - it cannot be '
                'less than -1080 or greater than 1080, to correspond with a '
                'time-zone range of -18:00 to +18:00.') % offset)
        # Could disallow seconds and microseconds as we don't need them or
        # use them.
        return cls._create(offset)
    @classmethod
    def _create(cls, offset):
        self = object.__new__(cls)
        self.__offset = offset
        return self
    def __getinitargs__(self):
        # for pickling.  tzinfo.__reduce__ calls this.
        return (self.__offset,)
    def _equalityFields(self):
        return self.__offset
    def utcoffset(self, dt):
        return self.__offset
    def tzname(self, dt):
        # aim for same format as datetime.timezone
        iso = private.formatUtcOffset(self.__offset)
        if iso == 'Z':
            # This is what python 3.8's timezone class does.  Python 3.4
            # returns UTC+00:00.  We go with UTC cos that makes more sense.
            return 'UTC'
        else:
            return 'UTC' + iso
    def dst(self, dt):
        return None
    def fromutc(self, dt):
        if not isinstance(dt, datetime.datetime):
            raise TypeError('dt should be a datetime')
        elif dt.tzinfo is not self:
            raise ValueError('dt.tzinfo should be self')
        return dt + self.__offset
    def __str__(self):
        return self.tzname(None)
    def __repr__(self):
        return '%s(%r)' % (private.fullNameOfClass(self.__class__),
            self.__offset)

try:
    datetime.timezone  # attempt to evaluate datetime.timezone
    def _createTimeZone(offset):
        return datetime.timezone(offset)
except AttributeError:
    def _createTimeZone(offset):
        return _TimeZone(offset)