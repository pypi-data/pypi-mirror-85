
import degreedays._private as private
import degreedays.time
import degreedays.geo
from degreedays._private import XmlElement
import datetime
import degreedays.api as api
import re
import bisect

__all__ = ['Location', 'GeographicLocation',
    'Period',
    'Breakdown', 'DatedBreakdown', 'AverageBreakdown',
    'Calculation', 'TimeSeriesCalculation',
    'DataSpec', 'DatedDataSpec', 'AverageDataSpec', 
    'TimeSeriesDataSpec', 'DataSpecs',
    'LocationDataRequest', 'LocationInfoRequest', 'DataApi',
    'TemperatureUnit', 'Temperature',
    'TimeSeriesInterval',
    'LocationError', 'SourceDataError',
    'DataValue', 'DatedDataValue', 'TimeSeriesDataValue',
    'DataSet', 'DatedDataSet', 'AverageDataSet', 'TimeSeriesDataSet',
    'DataSets',
    'Station', 'Source',
    'LocationDataResponse', 'LocationInfoResponse']

_ABSTRACT_INIT_FACTORY = ('This is an abstract superclass.  To create an '
    'instance use the class factory methods, for example: ')
_ABSTRACT_INIT_RESPONSE = ('This is an abstract superclass.  Only the '
    'subclasses %s can be instantiated directly, though usually the API would '
    'create them automatically.')

_LOCATION_EXAMPLE = ("Location.stationId('KNYC'), "
    "Location.longLat(degreedays.geo.LongLat(-122.45361, 37.80544)), "
    "Location.postalCode('10036', 'US'), "
    "Location.postalCode('WC2N 5DN', 'GB')")
class Location(private.Immutable):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY + _LOCATION_EXAMPLE + '.')
    @classmethod
    def stationId(cls, stationId):
        # Having to import impl for class factory methods like this is ugly...
        # But we can't do it at the top because then that's a circular import
        # (as impl depends on this module).
        # This seems to be the only way to avoid cluttering this module up
        # conceptually for the user by forcing them to see way more classes
        # than they'll need.
        # Apparently at least this isn't a performance hit:
        # http://stackoverflow.com/questions/477096/python-import-coding-style
        # "Because of the way python caches modules, there isn't a performance
        # hit. In fact, since the module is in the local namespace, there is a
        # slight performance benefit to importing modules in a function."
        import degreedays.api.data.impl as impl
        return impl.StationIdLocation(stationId)
    @classmethod
    def longLat(cls, longLat):
        import degreedays.api.data.impl as impl
        return impl.LongLatLocation(longLat)
    @classmethod
    def postalCode(cls, postalCode, countryCode):
        import degreedays.api.data.impl as impl
        return impl.PostalCodeLocation(postalCode, countryCode)
    @classmethod
    def _check(cls, param, paramName='location'):
        if not isinstance(param, Location):
            raise TypeError(private.wrongSupertypeString(param, paramName,
                Location, _LOCATION_EXAMPLE))
        return param

_GEOGRAPHIC_LOCATION_EXAMPLE = (
    "Location.longLat(degreedays.geo.LongLat(-122.45361, 37.80544)), "
    "Location.postalCode('10036', 'US'), "
    "Location.postalCode('WC2N 5DN', 'GB').")   
class GeographicLocation(Location):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY +
            _GEOGRAPHIC_LOCATION_EXAMPLE + '.')

_PERIOD_EXAMPLE = ("Period.latestValues('5'), "
    "Period.dayRange(degreedays.time.DayRange("
        "datetime.date(2012, 1, 1), "
        "datetime.date(2012, 10, 31)))")  
class Period(private.Immutable):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY + _PERIOD_EXAMPLE + '.')
    @classmethod
    def latestValues(cls, numberOfValues, minimumNumberOfValuesOrNone=None):
        import degreedays.api.data.impl as impl
        return impl.LatestValuesPeriod(
            numberOfValues, minimumNumberOfValuesOrNone)
    @classmethod
    def dayRange(cls, dayRange, minimumDayRangeOrNone=None):
        import degreedays.api.data.impl as impl
        return impl.DayRangePeriod(dayRange, minimumDayRangeOrNone)
    @classmethod
    def _check(cls, param, paramName='period'):
        if not isinstance(param, Period):
            raise TypeError(private.wrongSupertypeString(param, paramName,
                Period, _PERIOD_EXAMPLE))
        return param

_BREAKDOWN_EXAMPLE = ('DatedBreakdown.daily(Period.latestValues(30)), '
    'DatedBreakdown.monthly(Period.latestValues(12)), '
    'AverageBreakdown.fullYears(Period.latestValues(5))')   
class Breakdown(private.Immutable):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY + _BREAKDOWN_EXAMPLE + '.')

_DATED_BREAKDOWN_EXAMPLE = ('DatedBreakdown.daily(Period.latestValues(30)), '
    'DatedBreakdown.monthly(Period.latestValues(12)), '
    'DatedBreakdown.yearly(Period.latestValues(5))')
class DatedBreakdown(Breakdown):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY + _DATED_BREAKDOWN_EXAMPLE + '.')
    @property
    def allowPartialLatest(self): raise NotImplementedError()
    def _checkAllowPartialLatest(self, allowPartialLatest):
        return private.checkBoolean(allowPartialLatest, 'allowPartialLatest')
    def _reprStart(self):
        raise TypeError('Subclass must override this')
    def __repr__(self):
        if self.allowPartialLatest:
            return self._reprStart() + ', allowPartialLatest=True)'
        else:
            return self._reprStart() + ')'
    def _addAllowPartialLatestXml(self, xmlElement):
        if self.allowPartialLatest:
            xmlElement.addAttribute('allowPartialLatest', 'true')
        return xmlElement
    @classmethod
    def daily(cls, period, allowPartialLatest=False):
        import degreedays.api.data.impl as impl
        return impl.DailyBreakdown(period, allowPartialLatest)
    @classmethod
    def weekly(cls, period, firstDayOfWeek, allowPartialLatest=False):
        import degreedays.api.data.impl as impl
        return impl.WeeklyBreakdown(period, firstDayOfWeek, allowPartialLatest)
    @classmethod
    def monthly(cls, period, startOfMonth=degreedays.time.StartOfMonth(1),
            allowPartialLatest=False): 
        import degreedays.api.data.impl as impl
        return impl.MonthlyBreakdown(period, startOfMonth, allowPartialLatest)
    @classmethod
    def yearly(cls, period, startOfYear=degreedays.time.StartOfYear(1, 1),
            allowPartialLatest=False):
        import degreedays.api.data.impl as impl
        return impl.YearlyBreakdown(period, startOfYear, allowPartialLatest)
    @classmethod
    def custom(cls, dayRanges, allowPartialLatest=False):
        import degreedays.api.data.impl as impl
        return impl.CustomBreakdown(dayRanges, allowPartialLatest)
    @classmethod
    def _check(cls, param, paramName='datedBreakdown'):
        if not isinstance(param, DatedBreakdown):
            raise TypeError(private.wrongSupertypeString(param, paramName,
                DatedBreakdown, _DATED_BREAKDOWN_EXAMPLE))
        return param

_AVERAGE_BREAKDOWN_EXAMPLE = (
    'AverageBreakdown.fullYears(Period.latestValues(5)) for a ' +
    '5-year average covering the 5 most recent full calendar years') 
class AverageBreakdown(Breakdown):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY +
            _AVERAGE_BREAKDOWN_EXAMPLE, '.')
    @classmethod
    def fullYears(cls, period):
        import degreedays.api.data.impl as impl
        return impl.FullYearsAverageBreakdown(period)
    @classmethod
    def _check(cls, param, paramName='averageBreakdown'):
        if not isinstance(param, AverageBreakdown):
            raise TypeError(private.wrongSupertypeString(param, paramName,
                AverageBreakdown, _AVERAGE_BREAKDOWN_EXAMPLE))
        return param

# TemperatureUnit follows the pattern shown by one of the answers at:
# http://stackoverflow.com/questions/36932/
# Though we define CELSIUS and FAHRENHEIT inside the class (initially as None,
# then set after the definition), so as to make them appear in PyDev
# intellisense.
# The metaclass stuff is to enable people to iterate over the units like:
# "for u in TemperatureUnit".  It's complicated to make it compatible with
# Python 2 and 3.  Our approach is based on that described at:
# http://mikewatkins.ca/2008/11/29/python-2-and-3-metaclasses/
# We have to pass a dict into TemperatureUnitMetaclass, which would imply
# mutability, but following the guidance at
# http://stackoverflow.com/questions/9654133/
# we pass a dictionary containing empty __slots__ in, which works great at
# ensuring immutability.
class _TemperatureUnitMetaclass(type):
    def __iter__(self):
        for u in (TemperatureUnit.CELSIUS, TemperatureUnit.FAHRENHEIT):
            yield u
_TemperatureUnitSuper = _TemperatureUnitMetaclass('_TemperatureUnitSuper',
    (private.Immutable,), {'__slots__': ()})
class TemperatureUnit(_TemperatureUnitSuper):
    __slots__ = ('_shortChar', '_name', '__nameUpper',
        '_minTimesTen', '_maxTimesTen')
    CELSIUS = None # Set later
    FAHRENHEIT = None # as above
    def __init__(self, shortChar):
        self._shortChar = shortChar
        if shortChar == 'C' and TemperatureUnit.CELSIUS is None:
            self._name = 'Celsius'
            self._minTimesTen = -2730
            self._maxTimesTen = 30000
        elif shortChar == 'F' and TemperatureUnit.FAHRENHEIT is None:
            self._name = 'Fahrenheit'
            self._minTimesTen = -4594
            self._maxTimesTen = 54320
        else:
            raise TypeError('This is not built for direct '
                'instantiation.  Please use either TemperatureUnit.CELSIUS or '
                'TemperatureUnit.FAHRENHEIT.')
        self.__nameUpper = self._name.upper()
    def _equalityFields(self):
        return self._shortChar
    def __str__(self):
        return self._name
    def __repr__(self):
        return 'TemperatureUnit.' + self.__nameUpper
    def _toXml(self):
        return XmlElement('TemperatureUnit').setValue(self._name)
    @classmethod
    def _check(cls, param, paramName='temperatureUnit'):
        if type(param) is not TemperatureUnit:
            raise TypeError(private.wrongTypeString(param, paramName,
                TemperatureUnit,
                'TemperatureUnit.CELSIUS or TemperatureUnit.FAHRENHEIT'))
        return param  
TemperatureUnit.CELSIUS = TemperatureUnit('C')
TemperatureUnit.FAHRENHEIT = TemperatureUnit('F')

def _formatTemperature(value):
    s = '%.1f' % value
    # We did use rstrip('.0') but that didn't work with 0.0.
    if s.endswith('.0'):
        return s[:-2]
    return s

def _formatTemperatureTimesTen(timesTenValue):
    # Must divide by 10.0 to avoid it doing whole integer division (in python
    # 2 anyway; 3 is different: http://www.python.org/dev/peps/pep-0238/)
    return _formatTemperature(timesTenValue / 10.0)

_TEMPERATURE_EXAMPLE = ('Temperature.celsius(15.5), '
    'Temperature.fahrenheit(65)')  
class Temperature(private.Immutable):
    __slots__ = ('__valueTimesTen', '__unit')
    def __init__(self, value, unit):
        value = private.checkNumeric(value, 'value')
        # round returns a float, but int(...) of that should work fine,
        # according to:
        # http://stackoverflow.com/questions/3387655/
        self.__valueTimesTen = int(round(value * 10))
        if (self.__valueTimesTen < unit._minTimesTen or 
                self.__valueTimesTen > unit._maxTimesTen):
            raise ValueError('Invalid %s temperature %s - cannot be less ' 
                'than %s or greater than %s' %
                (unit.__name, _formatTemperature(value), 
                    _formatTemperatureTimesTen(unit._minTimesTen),
                    _formatTemperatureTimesTen(unit._maxTimesTen)))
        self.__unit = TemperatureUnit._check(unit, 'unit')
    def _equalityFields(self):
        return (self.__valueTimesTen, self.__unit)
    @classmethod
    def celsius(cls, value):
        return Temperature(value, TemperatureUnit.CELSIUS)
    @classmethod
    def fahrenheit(cls, value):
        return Temperature(value, TemperatureUnit.FAHRENHEIT)
    @property
    def value(self): 
        # Must divide by 10.0 for same reason as in _formatTemperatureTimesTen
        return self.__valueTimesTen / 10.0
    @property
    def unit(self): return self.__unit
    def __repr__(self):
        if self.__unit == TemperatureUnit.CELSIUS:
            return 'Temperature.celsius(' + _formatTemperatureTimesTen(
                self.__valueTimesTen) + ')'
        else:
            return 'Temperature.fahrenheit(' + _formatTemperatureTimesTen(
                self.__valueTimesTen) + ')'
    def __str__(self):
        return (_formatTemperatureTimesTen(self.__valueTimesTen) + ' ' +
            self.__unit._shortChar)
    def _toXml(self, elementNameExtra=''):
        return XmlElement(self.__unit._name + elementNameExtra).setValue(
            _formatTemperatureTimesTen(self.__valueTimesTen))
    @classmethod
    def _check(cls, param, paramName='temperature'):
        if type(param) is not Temperature:
            raise TypeError(private.wrongTypeString(param, paramName,
                Temperature, _TEMPERATURE_EXAMPLE))
        return param

class _TimeSeriesIntervalMetaclass(type):
    def __iter__(self):
        for i in (TimeSeriesInterval.HOURLY,):
            yield i
_TimeSeriesIntervalSuper = _TimeSeriesIntervalMetaclass(
    '_TimeSeriesIntervalSuper', (private.Immutable,), {'__slots__': ()})
class TimeSeriesInterval(_TimeSeriesIntervalSuper):
    __slots__ = ('__code', '__name', '__nameUpper')
    HOURLY = None # Set later
    def __init__(self, code):
        self.__code = code
        if code == 0 and TimeSeriesInterval.HOURLY is None:
            self.__name = 'Hourly'
        else:
            raise TypeError('This is not built for direct '
                'instantiation.  Please use TimeSeriesInterval.HOURLY.')
        self.__nameUpper = self.__name.upper()
    def _equalityFields(self):
        return self.__code
    def __str__(self):
        return self.__name
    def __repr__(self):
        return 'TimeSeriesInterval.' + self.__nameUpper
    def _toXml(self):
        return XmlElement('Interval').setValue(self.__name)
    @classmethod
    def _check(cls, param, paramName='interval'):
        if type(param) is not TimeSeriesInterval:
            raise TypeError(private.wrongTypeString(param, paramName,
                TimeSeriesInterval, 'TimeSeriesInterval.HOURLY'))
        return param  
TimeSeriesInterval.HOURLY = TimeSeriesInterval(0)

_CALCULATION_EXAMPLE = (
    'Calculation.heatingDegreeDays(Temperature.celsius(15.5)), '
    'Calculation.coolingDegreeDays(Temperature.fahrenheit(65))')            
class Calculation(private.Immutable):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY + _CALCULATION_EXAMPLE + '.')
    @classmethod
    def heatingDegreeDays(cls, baseTemperature):
        import degreedays.api.data.impl as impl
        return impl.HeatingDegreeDaysCalculation(baseTemperature)
    @classmethod
    def coolingDegreeDays(cls, baseTemperature):
        import degreedays.api.data.impl as impl
        return impl.CoolingDegreeDaysCalculation(baseTemperature)
    @classmethod
    def _check(cls, param, paramName='calculation'):
        if not isinstance(param, Calculation):
            raise TypeError(private.wrongSupertypeString(param, paramName,
                Calculation, _CALCULATION_EXAMPLE))
        return param

_TIME_SERIES_CALCULATION_EXAMPLE = (
    'TimeSeriesCalculation.hourlyTemperature(TemperatureUnit.CELSIUS)')            
class TimeSeriesCalculation(private.Immutable):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY +
            _TIME_SERIES_CALCULATION_EXAMPLE + '.')
    @classmethod
    def hourlyTemperature(cls, temperatureUnit):
        import degreedays.api.data.impl as impl
        return impl.TemperatureTimeSeriesCalculation(
            TimeSeriesInterval.HOURLY, temperatureUnit)
    @classmethod
    def _check(cls, param, paramName='timeSeriesCalculation'):
        if not isinstance(param, TimeSeriesCalculation):
            raise TypeError(private.wrongSupertypeString(param, paramName,
                TimeSeriesCalculation, _TIME_SERIES_CALCULATION_EXAMPLE))
        return param

_DATA_SPEC_EXAMPLE = (
    'DataSpec.dated(calculation, datedBreakdown), '
    'DataSpec.average(calculation, averageBreakdown), '
    'DataSpec.timeSeries(timeSeriesCalculation, datedBreakdown)')
class DataSpec(private.Immutable):
    __slots__ = ()
    def __init__(self):
        raise TypeError(_ABSTRACT_INIT_FACTORY + _DATA_SPEC_EXAMPLE + '.')
    @classmethod
    def dated(cls, calculation, datedBreakdown):
        return DatedDataSpec(calculation, datedBreakdown)
    @classmethod
    def average(cls, calculation, averageBreakdown):
        return AverageDataSpec(calculation, averageBreakdown)
    @classmethod
    def timeSeries(cls, timeSeriesCalculation, datedBreakdown):
        return TimeSeriesDataSpec(timeSeriesCalculation, datedBreakdown)
    @classmethod
    def _check(cls, param, paramName='dataSpec'):
        if not isinstance(param, DataSpec):
            raise TypeError(private.wrongSupertypeString(param, paramName,
                DataSpec, _DATA_SPEC_EXAMPLE))
        return param
    
class DatedDataSpec(DataSpec):
    __slots__ = ('__calculation', '__breakdown')
    def __init__(self, calculation, datedBreakdown):
        self.__calculation = Calculation._check(calculation)
        self.__breakdown = DatedBreakdown._check(datedBreakdown)
    def _equalityFields(self):
        return (self.__calculation, self.__breakdown)
    @property
    def calculation(self): return self.__calculation
    @property
    def breakdown(self): return self.__breakdown
    def __repr__(self):
        return 'DatedDataSpec(%r, %r)' % (self.__calculation, self.__breakdown)
    def _toXml(self):
        return XmlElement('DatedDataSpec') \
            .addChild(self.__calculation._toXml()) \
            .addChild(self.__breakdown._toXml())
            
class AverageDataSpec(DataSpec):
    __slots__ = ('__calculation', '__breakdown')
    def __init__(self, calculation, averageBreakdown):
        self.__calculation = Calculation._check(calculation)
        self.__breakdown = AverageBreakdown._check(averageBreakdown)
    def _equalityFields(self):
        return (self.__calculation, self.__breakdown)
    @property
    def calculation(self): return self.__calculation
    @property
    def breakdown(self): return self.__breakdown
    def __repr__(self):
        return ('AverageDataSpec(%r, %r)' %
            (self.__calculation, self.__breakdown))
    def _toXml(self):
        return XmlElement('AverageDataSpec') \
            .addChild(self.__calculation._toXml()) \
            .addChild(self.__breakdown._toXml())

class TimeSeriesDataSpec(DataSpec):
    __slots__ = ('__calculation', '__breakdown')
    def __init__(self, timeSeriesCalculation, datedBreakdown):
        self.__calculation = TimeSeriesCalculation._check(timeSeriesCalculation)
        self.__breakdown = DatedBreakdown._check(datedBreakdown)
    def _equalityFields(self):
        return (self.__calculation, self.__breakdown)
    @property
    def calculation(self): return self.__calculation
    @property
    def breakdown(self): return self.__breakdown
    def __repr__(self):
        return 'TimeSeriesDataSpec(%r, %r)' % (self.__calculation, self.__breakdown)
    def _toXml(self):
        return XmlElement('TimeSeriesDataSpec') \
            .addChild(self.__calculation._toXml()) \
            .addChild(self.__breakdown._toXml())
            
_DATA_SPEC_KEY_REGEXP_STRING = '[-_.0-9a-zA-Z]{1,60}$'
_DATA_SPEC_KEY_REGEXP = re.compile(_DATA_SPEC_KEY_REGEXP_STRING)
# This assumes that it's already been checked to see that it's a string.
def _checkDataSpecStringKey(key):
    if not _DATA_SPEC_KEY_REGEXP.match(key):
        raise ValueError('Invalid DataSpec/DataSet key (%r) - it should match '
            'the regular expression %s.' % (key, _DATA_SPEC_KEY_REGEXP_STRING))
    return key    

_DATA_SPECS_EXAMPLE = ('DataSpecs(hddSpec), '
    'DataSpecs(hddSpec, cddSpec), '
    'DataSpecs(listOfDataSpecObjects)')            
class DataSpecs(private.Immutable):
    __slots__ = ('__specToKeyMap', '__keyToSpecMap', '__orderedKeys',
            '__specSet')
    def __init__(self, *args):
        self.__specToKeyMap = {}
        # Could use OrderedDict, but that is Python 2.7+ and I'm not sure we
        # want to restrict to that version just for that.
        self.__keyToSpecMap = {}
        self.__orderedKeys = []
        if len(args) == 1 and isinstance(args[0], dict):
            for key, item in private.getDictItemsIterable(args[0]):
                if not private.isString(key):
                    raise TypeError('If creating this with a dict (to specify '
                        'custom keys for the request XML), DataSpecs expects '
                        'string keys.  But the dict it was passed contained %r '
                        'as a key.' % key)
                elif not isinstance(item, DataSpec):
                    raise TypeError('If creating this with a dict (to specify '
                        'custom keys for the request XML), DataSpecs expects '
                        'the values associated with each key to be DataSpec '
                        'instances (e.g. DataSpec.dated(...) or '
                        'DataSpec.average(...)).  But for key %r it found %r' %
                        (key, item))
                key = _checkDataSpecStringKey(key)
                self.__specToKeyMap[item] = key
                self.__keyToSpecMap[key] = item
                self.__orderedKeys.append(key)
        else:
            def add(item):
                index = len(self.__orderedKeys)
                if index >= 100:
                    raise ValueError(
                        'Cannot have more than 100 DataSpec items.')
                if isinstance(item, DataSpec):
                    if not item in self.__specToKeyMap:
                        key = str(index) # simple integer key for now
                        self.__specToKeyMap[item] = key
                        self.__keyToSpecMap[key] = item
                        self.__orderedKeys.append(key)
                elif private.isString(item):
                    # Have to be careful with strings cos they look like a
                    # sequence but will cause a stack overflow, see:
                    # https://stackoverflow.com/questions/1835018/
                    DataSpec._check(item,
                        'An item passed into the DataSpecs constructor')
                else:
                    # assume it's a sequence, just let it throw error if not
                    # Could do a try catch too, so can give a useful error
                    # message if it's not a sequence or a DataSpec.
                    for innerItem in item:
                        add(innerItem)    
            for arg in args:
                add(arg)
        if len(self.__orderedKeys) == 0:
            raise ValueError('Must have at least one DataSpec')
        # We create specSet purely for a quick equality comparison, as
        # described at:
        # http://stackoverflow.com/questions/3210832/
        # Note it has to be frozenset, not set, because only frozenset (which
        # is immutable) is hashable.
        self.__specSet = frozenset(self.__specToKeyMap)
        # Make tuple so immutable.
        self.__orderedKeys = tuple(self.__orderedKeys)
    def _equalityFields(self):
        return self.__specSet
    @property
    def keys(self): return self.__orderedKeys
    def __getitem__(self, key):
        return self.__keyToSpecMap[key]
    def getKey(self, dataSpec):
        return self.__specToKeyMap[dataSpec]
    def _containsKey(self, key):
        return key in self.__keyToSpecMap
    def _dataSetsEquals(self, thisResults, thatDataSpecs, thatResultsMap):
        for spec, thisKey in private.getDictItemsIterable(self.__specToKeyMap):
            thisResult = thisResults[thisKey]
            thatKey = thatDataSpecs.__specToKeyMap[spec]
            thatResult = thatResultsMap[thatKey]
            if thisResult != thatResult:
                return False
        return True
    def _dataSetsHashCode(self, thisResultsMap):
        hashCode = 17
        # hashCode of the DataSpecs stored inside the DataSets.
        hashCode = 31 * hashCode + hash(self)
        # We want to sum the hashCodes of the DataSet objects corresponding to 
        # each unique DataSpec.
        # 
        # We need to sum without a multiplier because, if we used a multiplier,
        # then the result would depend on the order.  And we don't want that.
        # This is like how it's done in Java's AbstractSet.
        for key in private.getDictValuesIterable(self.__specToKeyMap):
            result = thisResultsMap[key]
            hashCode += hash(result)
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
        if not isinstance(hashCode, int):
            hashCode = hash(hashCode)
        return hashCode
    def __len__(self):
        return len(self.__orderedKeys)
    def __repr__(self):
        # We make this include the keys.  It's more useful for DataSets.__repr__
        # and for debugging, if necessary.  Also the keys are pretty short.
        s = []
        for key in self.__orderedKeys:
            s.append("'%s': %r" % (key, self.__keyToSpecMap[key]))
        s.sort()
        return 'DataSpecs({' + ', '.join(s) + '})'
    def _toXml(self):
        parent = XmlElement('DataSpecs')
        for key in self.__orderedKeys:
            child = self.__keyToSpecMap[key]._toXml().addAttribute('key', key)
            parent.addChild(child)
        return parent
    @classmethod
    def _check(cls, param, paramName='dataSpecs'):
        if type(param) is not DataSpecs:
            raise TypeError(private.wrongTypeString(param, paramName,
                DataSpecs, _DATA_SPECS_EXAMPLE))
        return param

_LOCATION_DATA_REQUEST_EXAMPLE = (
    "LocationDataRequest(Location.stationId('EGLL'), "
        "DataSpecs(DataSpec.dated("
            "Calculation.heatingDegreeDays(Temperature.fahrenheit(65)), "
                "DatedBreakdown.monthly(Period.latestValues(12)))))")
class LocationDataRequest(private.Immutable):
    __slots__ = ('__location', '__dataSpecs')
    def __init__(self, location, dataSpecs):
        self.__location = Location._check(location)
        self.__dataSpecs = DataSpecs._check(dataSpecs)
    def _equalityFields(self):
        return (self.__location, self.__dataSpecs)
    @property
    def location(self): return self.__location
    @property
    def dataSpecs(self): return self.__dataSpecs  
    def __repr__(self):
        return ('LocationDataRequest(%r, %r)' %
            (self.__location, self.__dataSpecs)) 
    def _toXml(self):
        return XmlElement('LocationDataRequest') \
            .addChild(self.__location._toXml()) \
            .addChild(self.__dataSpecs._toXml())
    @classmethod
    def _check(cls, param, paramName='locationDataRequest'):
        if type(param) is not LocationDataRequest:
            raise TypeError(private.wrongTypeString(param, paramName,
                LocationDataRequest, _LOCATION_DATA_REQUEST_EXAMPLE))
        return param
    
_LOCATION_INFO_REQUEST_EXAMPLE = (
    "LocationInfoRequest(Location.stationId('EGLL'), "
        "DataSpecs(DataSpec.dated("
            "Calculation.heatingDegreeDays(Temperature.fahrenheit(65)), "
                "DatedBreakdown.monthly(Period.latestValues(12)))))")
class LocationInfoRequest(private.Immutable):
    __slots__ = ('__location', '__dataSpecs')
    def __init__(self, location, dataSpecs):
        self.__location = Location._check(location)
        self.__dataSpecs = DataSpecs._check(dataSpecs)
    def _equalityFields(self):
        return (self.__location, self.__dataSpecs)
    @property
    def location(self): return self.__location
    @property
    def dataSpecs(self): return self.__dataSpecs  
    def __repr__(self):
        return ('LocationInfoRequest(%r, %r)' %
            (self.__location, self.__dataSpecs)) 
    def _toXml(self):
        return XmlElement('LocationInfoRequest') \
            .addChild(self.__location._toXml()) \
            .addChild(self.__dataSpecs._toXml())
    @classmethod
    def _check(cls, param, paramName='locationInfoRequest'):
        if type(param) is not LocationInfoRequest:
            raise TypeError(private.wrongTypeString(param, paramName,
                LocationInfoRequest, _LOCATION_INFO_REQUEST_EXAMPLE))
        return param
            
            
class LocationError(api.RequestFailureError):
    def __init__(self, failureResponse):
        api.RequestFailureError.__init__(self, failureResponse)
    @property
    def isDueToLocationNotRecognized(self):
        return self._testCode('LocationNotRecognized')
    @property
    def isDueToLocationNotSupported(self):
        return self._testCode('LocationNotSupported')

class SourceDataError(api.FailureError):
    def __init__(self, failure):
        api.FailureError.__init__(self, failure)
    @property
    def isDueToSourceDataErrors(self):
        return self._testCode('SourceDataErrors')
    @property
    def isDueToSourceDataCoverage(self):
        return self._testCode('SourceDataCoverage')
    @property
    def isDueToSourceDataGranularity(self):
        return self._testCode('SourceDataGranularity')

def _checkPercentageEstimated(percentageEstimated):
    if percentageEstimated == 0:
        # returns 0.0 for negative zero and fast-tracks common 0 case
        return 0.0
    private.checkNumeric(percentageEstimated, 'percentageEstimated')
    if percentageEstimated > 100:
        raise ValueError('Invalid percentageEstimated %r: cannot be > 100.'
            % percentageEstimated)
    elif percentageEstimated < 0:
        raise ValueError('Invalid percentageEstimated %r: cannot be < 0')
    return percentageEstimated
   
class DataValue(private.Immutable):
    __slots__ = ()
    def __init__(self):
        # To be sure that __init__ isn't called on this. Our __new__ should mean
        # only subclasses have their __init__ called.
        raise TypeError()
    def __new__(cls, value, percentageEstimated):
        # Kind of based on example at:
        # http://stackoverflow.com/questions/5953759/
        if cls is DataValue:
            private.checkNumeric(value, 'value')
            if _checkPercentageEstimated(percentageEstimated) > 0:
                return _EstimatedDataValue(value, percentageEstimated)
            else:
                return _SimpleDataValue(value, 0.0)
        else:
            return private.Immutable.__new__(cls)
    @property
    def value(self): raise NotImplementedError()
    @property
    def percentageEstimated(self): raise NotImplementedError()
    @classmethod
    def _check(cls, param, paramName='dataValue'):
        if not isinstance(param, DataValue):
            raise TypeError(private.wrongSupertypeString(param, paramName, DataValue))
        return param

class _SimpleDataValue(DataValue):
    __slots__ = ('__value',)
    # Pass percentageEstimated to make the auto-call of __init__ that occurs
    # after the superclass __new__ method have the right number of arguments.
    # Essentially we need to accept the args that DataValue(...) was called
    # with and the easiest way to do this is to match the signature here (even
    # though we don't need percentageEstimated for this one as it wouldn't be
    # called unless it was zero).
    def __init__(self, value, percentageEstimated):
        self.__value = value
    @property
    def value(self): return self.__value
    @property
    def percentageEstimated(self): return 0.0
    def _equalityFields(self):
        return self.__value
    def __str__(self):
        # %g works well for floats. %f adds unnecessary trailing zeroes.
        return '%g' % self.__value
    def __repr__(self):
        return 'DataValue(%g, 0.0)' % self.__value
    
class _EstimatedDataValue(DataValue):
    __slots__ = ('__value', '__percentageEstimated')
    # As for SimpleDataValue, it's best to match the signature of DataValue.
    def __init__(self, value, percentageEstimated):
        self.__value = value
        self.__percentageEstimated = percentageEstimated
    @property
    def value(self): return self.__value
    @property
    def percentageEstimated(self): return self.__percentageEstimated
    def _equalityFields(self):
        return (self.__value, self.__percentageEstimated)
    def __str__(self):
        return ('%g (%g%% estimated)' %
            (self.__value, self.__percentageEstimated))
    def __repr__(self):
        return ('DataValue(%g, %g)' %
                (self.__value, self.__percentageEstimated))
        
class DatedDataValue(DataValue):
    __slots__ = ()
    def __init__(self):
        # Like for DataValue.
        raise TypeError()
    def __new__(cls, value, percentageEstimated, dayRange):
        if cls is DatedDataValue:
            private.checkNumeric(value, 'value')
            degreedays.time.DayRange._check(dayRange)
            if dayRange.first == dayRange.last:
                if _checkPercentageEstimated(percentageEstimated) > 0:
                    return _EstimatedSingleDayDatedDataValue(
                        value, percentageEstimated, dayRange)
                else:
                    return _SingleDayDatedDataValue(value, 0.0, dayRange)
            else:
                if _checkPercentageEstimated(percentageEstimated) > 0:
                    return _EstimatedMultiDayDatedDataValue(
                        value, percentageEstimated, dayRange)
                else:
                    return _MultiDayDatedDataValue(value, 0.0, dayRange)
        else:
            # Need to go right up to the class above DataValue, as we don't want
            # to have to match DataValue's args.
            return private.Immutable.__new__(cls)
    @property
    def dayRange(self): raise NotImplementedError()
    @property
    def firstDay(self):
        return self.dayRange.first
    @property
    def lastDay(self):
        return self.dayRange.last
    def __repr__(self):
        return ('DatedDataValue(%g, %g, %r)' %
            (self.value, self.percentageEstimated, self.dayRange))
    @classmethod
    def _check(cls, param, paramName='datedDataValue'):
        if not isinstance(param, DatedDataValue):
            raise TypeError(private.wrongSupertypeString(
                param, paramName, DatedDataValue))
        return param
        
class _SingleDayDatedDataValue(DatedDataValue):
    __slots__ = ('__value', '__day')
    def __init__(self, value, percentageEstimated, dayRange):
        self.__value = value
        self.__day = dayRange.first
    def _equalityFields(self):
        return (self.__value, self.__day)
    @property
    def value(self): return self.__value
    @property
    def percentageEstimated(self): return 0.0
    @property
    def dayRange(self):
        return degreedays.time.DayRange(self.__day, self.__day)
    @property
    def firstDay(self): return self.__day
    @property
    def lastDay(self): return self.__day
    def __str__(self):
        return '%s: %g' % (self.__day, self.__value)

class _EstimatedSingleDayDatedDataValue(DatedDataValue):
    __slots__ = ('__value', '__percentageEstimated', '__day')
    def __init__(self, value, percentageEstimated, dayRange):
        self.__value = value
        self.__percentageEstimated = percentageEstimated
        self.__day = dayRange.first
    def _equalityFields(self):
        return (self.__value, self.__percentageEstimated, self.__day)
    @property
    def value(self): return self.__value
    @property
    def percentageEstimated(self): return self.__percentageEstimated
    @property
    def dayRange(self):
        return degreedays.time.DayRange(self.__day, self.__day)
    @property
    def firstDay(self): return self.__day
    @property
    def lastDay(self): return self.__day
    def __str__(self):
        return ('%s: %g (%g%% estimated)' %
            (self.__day, self.__value, self.__percentageEstimated))

class _MultiDayDatedDataValue(DatedDataValue):
    __slots__ = ('__value', '__dayRange')
    def __init__(self, value, percentageEstimated, dayRange):
        self.__value = value
        self.__dayRange = dayRange
    def _equalityFields(self):
        return (self.__value, self.__dayRange)
    @property
    def value(self): return self.__value
    @property
    def percentageEstimated(self): return 0.0
    @property
    def dayRange(self): return self.__dayRange
    def __str__(self):
        return '%s: %g' % (self.__dayRange, self.__value)

class _EstimatedMultiDayDatedDataValue(DatedDataValue):
    __slots__ = ('__value', '__percentageEstimated', '__dayRange')
    def __init__(self, value, percentageEstimated, dayRange):
        self.__value = value
        self.__percentageEstimated = percentageEstimated
        self.__dayRange = dayRange
    def _equalityFields(self):
        return (self.__value, self.__percentageEstimated, self.__dayRange)
    @property
    def value(self): return self.__value
    @property
    def percentageEstimated(self): return self.__percentageEstimated
    @property
    def dayRange(self): return self.__dayRange
    def __str__(self):
        return ('%s: %g (%g%% estimated)' %
            (self.__dayRange, self.__value, self.__percentageEstimated))

class TimeSeriesDataValue(DataValue):
    __slots__ = ()
    def __init__(self):
        # Like for DataValue.
        raise TypeError()
    def __new__(cls, value, percentageEstimated, datetime):
        if cls is TimeSeriesDataValue:
            private.checkNumeric(value, 'value')
            private.checkDatetime(datetime, 'datetime')
            if datetime.second > 0 or datetime.microsecond > 0:
                raise ValueError(('We expect the datetime of a TimeSeriesDataValue '
                    'to be specified to the level of minutes only (i.e. no seconds '
                    'or microseconds), but this datetime is %r.') % datetime)
            elif datetime.tzinfo is None:
                raise ValueError(('We expect the datetime of a TimeSeriesDataValue '
                    'to have its tzinfo property set, but this datetime (%r) does '
                    'not.') % datetime)
            if _checkPercentageEstimated(percentageEstimated) > 0:
                return _EstimatedTimeSeriesDataValue(
                    value, percentageEstimated, datetime)
            else:
                return _SimpleTimeSeriesDataValue(value, 0.0, datetime)
        else:
            # Need to go right up to the class above DataValue, as we don't want
            # to have to match DataValue's args.
            return private.Immutable.__new__(cls)
    @property
    def datetime(self): raise NotImplementedError()
    def __repr__(self):
        return ('TimeSeriesDataValue(%g, %g, %r)' %
            (self.value, self.percentageEstimated, self.datetime))
    @classmethod
    def _check(cls, param, paramName='timeSeriesDataValue'):
        if not isinstance(param, TimeSeriesDataValue):
            raise TypeError(private.wrongSupertypeString(
                param, paramName, TimeSeriesDataValue))
        return param
        
class _SimpleTimeSeriesDataValue(TimeSeriesDataValue):
    __slots__ = ('__value', '__datetime')
    def __init__(self, value, percentageEstimated, datetime):
        self.__value = value
        self.__datetime = datetime
    def _equalityFields(self):
        return (self.__value, self.__datetime)
    @property
    def value(self): return self.__value
    @property
    def percentageEstimated(self): return 0.0
    @property
    def datetime(self): return self.__datetime
    def __str__(self):
        return '%s: %g' % (private.formatDateTime(self.__datetime),
            self.__value)

class _EstimatedTimeSeriesDataValue(TimeSeriesDataValue):
    __slots__ = ('__value', '__percentageEstimated', '__datetime')
    def __init__(self, value, percentageEstimated, datetime):
        self.__value = value
        self.__percentageEstimated = percentageEstimated
        self.__datetime = datetime
    def _equalityFields(self):
        return (self.__value, self.__percentageEstimated, self.__datetime)
    @property
    def value(self): return self.__value
    @property
    def percentageEstimated(self): return self.__percentageEstimated
    @property
    def datetime(self): return self.__datetime
    def __str__(self):
        return ('%s: %g (%g%% estimated)' %
            (private.formatDateTime(self.__datetime), self.__value,
                self.__percentageEstimated))

class DataSet(private.Immutable):
    __slots__ = ()
    def __init__(self):
        raise TypeError(
            _ABSTRACT_INIT_RESPONSE % 'DatedDataSet and AverageDataSet')
    @property
    def percentageEstimated(self): raise NotImplementedError()
    @property
    def fullRange(self): raise NotImplementedError()
    
class DatedDataSet(DataSet):
    __slots__ = ('__percentageEstimated', '__values', '__isContiguous')
    def __init__(self, percentageEstimated, values):
        self.__percentageEstimated = _checkPercentageEstimated(
            percentageEstimated)
         # convert values to immutable tuple and check each item within it
        values = private.checkTupleItems(
            tuple(values), DatedDataValue._check, 'values')
        length = len(values)
        if length == 0:
            raise ValueError('Expecting at least one DatedDataValue')
        isContiguous = True
        for i in range(1, length):
            lastDayOfPrevious = values[i - 1].lastDay
            firstDayOfTest = values[i].firstDay
            daysAfter = (firstDayOfTest - lastDayOfPrevious).days
            if daysAfter != 1:
                if daysAfter > 1:
                    isContiguous = False
                else:
                    raise ValueError(('Problem DatedDataValue items at indexes '
                        '%d (%s) and %d (%s): values must be chronological, '
                        'with each one starting after the end of the '
                        'previous.') % ((i - 1), values[i - 1], i, values[i])) 
        self.__values = values
        self.__isContiguous = isContiguous
    def _equalityFields(self):
        return (self.__percentageEstimated, self.__values)
    @property
    def percentageEstimated(self): return self.__percentageEstimated
    @property
    def values(self): return self.__values
    @property
    def fullRange(self):
        return degreedays.time.DayRange(self.__values[0].firstDay,
            self.__values[-1].lastDay)
    @property
    def isContiguous(self): return self.__isContiguous
    def __str__(self):
        s = []
        s.append('DatedDataSet(')
        s.append(str(len(self.__values)))
        s.append(' value')
        if len(self.__values) != 1:
            s.append('s')
        else:
            # include the value itself.  No need for % estimated as it will be
            # the same as for the whole set.
            s.append(' (%g)' % self.__values[0].value)
        s.append(' covering ')
        s.append(str(self.fullRange))
        if self.__percentageEstimated > 0:
            s.append(', %g%% estimated' % self.__percentageEstimated)
        s.append(')')
        return ''.join(s)
    def __repr__(self):
        return ('DatedDataSet(percentageEstimated=%g, values=%r)' %
            (self.__percentageEstimated, self.__values))
        
class AverageDataSet(DataSet):
    __slots__ = ('__firstYear', '__lastYear', '__annualAverage',
            '__monthlyAverages')
    def __init__(self, firstYear, lastYear, annualAverage, monthlyAverages):
        self.__firstYear = private.checkInt(firstYear, 'firstYear')
        self.__lastYear = private.checkInt(lastYear, 'lastYear')
        if firstYear > lastYear:
            raise ValueError('firstYear (%s) cannot be greater than lastYear '
                '(%s).' % (firstYear, lastYear))
        self.__annualAverage = DataValue._check(annualAverage, 'annualAverage')
        self.__monthlyAverages = private.checkTupleItems(tuple(monthlyAverages),
            DataValue._check, 'monthlyAverages')
    def _equalityFields(self):
        return (self.__firstYear, self.__lastYear, self.__annualAverage,
            self.__monthlyAverages)
    @property
    def firstYear(self): return self.__firstYear
    @property
    def lastYear(self): return self.__lastYear
    @property
    def numberOfYears(self):
        return self.__lastYear - self.__firstYear + 1
    @property
    def annualAverage(self): return self.__annualAverage
    def monthlyAverage(self, monthIndexWithJanAs1):
        return self.__monthlyAverages[monthIndexWithJanAs1 - 1]
    @property
    def fullRange(self):
        return degreedays.time.DayRange(
            datetime.date(self.__firstYear, 1, 1),
            datetime.date(self.__lastYear, 12, 31))
    def __str__(self):
        return ('AverageDataSet(%d to %d, annualAverage = %s)' %
            (self.__firstYear, self.__lastYear, self.__annualAverage))
    def __repr__(self):
        return ('AverageDataSet(firstYear=%d, lastYear=%d, annualAverage=%r, '
            'monthlyAverages=%r)' %
            (self.__firstYear, self.__lastYear, self.__annualAverage,
                self.__monthlyAverages))

class TimeSeriesDataSet(DataSet):
    __slots__ = ('__percentageEstimated', '__values', '__dates', 
        '__firstOfDayIndexes')
    def getIllegalTimeMessage(self, values, laterIndex, afterStart):
        return ('Problem TimeSeriesDataValue items at index %d (with a '
            'datetime of %s) and index %d (with a datetime of %s).  %s') % \
            (laterIndex - 1,
            private.formatDateTime(values[laterIndex - 1].datetime),
            laterIndex, private.formatDateTime(values[laterIndex].datetime),
            afterStart)
    def __init__(self, percentageEstimated, values):
        self.__percentageEstimated = _checkPercentageEstimated(percentageEstimated)
         # convert values to immutable tuple and check each item within it
        values = private.checkTupleItems(
            tuple(values), TimeSeriesDataValue._check, 'values')
        length = len(values)
        if length == 0:
            raise ValueError('Expecting at least one TimeSeriesDataValue')
        lastDateTime = values[0].datetime
        lastDate = lastDateTime.date()
        dates = [lastDate]
        firstOfDayIndexes = [0]
        for i in range(1, len(values)):
            dt = values[i].datetime
            if dt <= lastDateTime:
                raise ValueError(self.getIllegalTimeMessage(values, i,
                    ('It is expected that values are chronological, with each '
                    'one coming after the last (when their timezones are taken '
                    'into account).')))
            # Ugly comparing all 3 fields but we don't really want to call
            # dt.date() and create a new object on every iteration.
            if dt.day != lastDate.day or dt.month != lastDate.month or \
                    dt.year != lastDate.year:
                dtDate = dt.date()
                if dtDate < lastDate:
                    raise ValueError(self.getIllegalTimeMessage(values, i,
                        ('The YYYY-MM-DD date part of the datetimes must ' 
                        'never go backwards.')))
                lastDate = dtDate
                dates.append(lastDate)
                firstOfDayIndexes.append(i)
            lastDateTime = dt
        self.__values = values
        self.__dates = tuple(dates)
        self.__firstOfDayIndexes = tuple(firstOfDayIndexes)
    def _equalityFields(self):
        return (self.__percentageEstimated, self.__values)
    @property
    def percentageEstimated(self): return self.__percentageEstimated
    @property
    def values(self): return self.__values
    @property
    def fullRange(self):
        return degreedays.time.DayRange(self.__values[0].datetime.date(),
            self.__values[-1].datetime.date())
    def getValuesWithin(self, dateOrDayRange):
        if type(dateOrDayRange) is datetime.date:
            dayRange = degreedays.time.DayRange.singleDay(dateOrDayRange)
        elif type(dateOrDayRange) is degreedays.time.DayRange:
            dayRange = dateOrDayRange
        else:
            raise ValueError(('dateOrDayRange should be of type datetime.date '
                'or degreedays.time.DayRange, not %s.') %
                private.fullNameOfClass(dateOrDayRange.__class__))
        # Find earliest date that is later than or equal to startDate
        startDateIndex = bisect.bisect_left(self.__dates, dayRange.first)
        if startDateIndex == len(self.__dates) or not dayRange.contains(
                self.__dates[startDateIndex]):
            return ()
        startValueIndex = self.__firstOfDayIndexes[startDateIndex]
        # find earliest date later than endDate
        endDateIndex = bisect.bisect_right(
            self.__dates, dayRange.last, startDateIndex)
        if endDateIndex == len(self.__dates):
            endValueIndexExclusive = len(self.__values)
        else:
            endValueIndexExclusive = self.__firstOfDayIndexes[endDateIndex]
        return self.__values[startValueIndex:endValueIndexExclusive]
    def __str__(self):
        s = []
        s.append('TimeSeriesDataSet(')
        s.append(str(len(self.__values)))
        s.append(' values covering ')
        first = self.__values[0]
        last = self.__values[-1]
        s.append(private.formatDateTime(first.datetime))
        s.append(' (%g)' % first.value)
        s.append(' to ')
        s.append(private.formatDateTime(last.datetime))
        s.append(' (%g)' % last.value)
        if self.__percentageEstimated > 0:
            s.append(', %g%% estimated' % self.__percentageEstimated)
        s.append(')')
        return ''.join(s)
    def __repr__(self):
        return ('TimeSeriesDataSet(percentageEstimated=%g, values=%r)' %
            (self.__percentageEstimated, self.__values))
       
class DataSets(object):
    __slots__ = ('__dataSpecsOrNone', '__results', '__cachedHashCode')
    def __init__(self, dataSpecsOrNone, stringKeyToResultDict):
        dictCopy = private.checkDict(stringKeyToResultDict,
            'stringKeyToResultDict').copy()
        if dataSpecsOrNone is not None:
            DataSpecs._check(dataSpecsOrNone, 'dataSpecsOrNone')
            if len(dataSpecsOrNone) != len(dictCopy):
                raise ValueError('Different size of dataSpecsOrNone (%s) '
                    'and stringKeyToResultDict (%s)' %
                    (len(dataSpecsOrNone), len(dictCopy)))
        for key, value in private.getDictItemsIterable(dictCopy):
            if dataSpecsOrNone is not None:
                if not dataSpecsOrNone._containsKey(key):
                    raise ValueError('stringKeyToResultDict contains a key %r '
                        'that is not in the corresponding DataSpecs from the '
                        'request' % key)
            elif not private.isString(key):
                raise TypeError('stringKeyToResultDict contains non-string '
                    'key of type %s' % private.fullNameOfClass(key.__class__))
            else:
                _checkDataSpecStringKey(key)
            if not isinstance(value, (DataSet, api.Failure)):
                raise TypeError('stringKeyToResultDict contains a value that '
                    'is neither a subclass of DataSpec nor a Failure; it has '
                    'type %s' % private.fullNameOfClass(value.__class__))
        self.__dataSpecsOrNone = dataSpecsOrNone
        self.__results = dictCopy
        self.__cachedHashCode = 0
    def __getitem__(self, dataSpecObjectOrStringKey):
        if private.isString(dataSpecObjectOrStringKey):
            # Unusual case, but useful for testing
            stringKey = dataSpecObjectOrStringKey
        elif isinstance(dataSpecObjectOrStringKey, DataSpec):
            if self.__dataSpecsOrNone is None:
                # http://stackoverflow.com/questions/1701199/ says ValueError
                # is the equivalent to IllegalStateException.
                raise ValueError("You can only use DataSpec objects to access "
                    "the corresponding DataSet objects if the DataSets object "
                    "has internal access to the original DataSpecs from the "
                    "request (which maps the string keys in the XML response "
                    "to the DataSpec objects used to request them). This "
                    "framework would usually ensure that the DataSets object "
                    "was created with access to the relevant DataSpecs object, "
                    "but are you perhaps parsing the XML response yourself? "
                    "If so, please ensure that your implementation passes the "
                    "DataSpecs object from the request into the DataSets "
                    "object, or do all your interrogation of this object using "
                    "string keys.")
            stringKey = self.__dataSpecsOrNone.getKey(dataSpecObjectOrStringKey)
        else:
            raise TypeError('Expecting a DataSpec object from the request '
                '(the usual way to use this), or a string key (less common, '
                'but occasionally useful for testing or debugging).  Instead, '
                'got %r' % dataSpecObjectOrStringKey)
        result = self.__results[stringKey]
        if isinstance(result, api.Failure):
            raise SourceDataError(result)
        return result
    def __eq__(self, other):
        if type(other) is not DataSets:
            return False
        if self.__dataSpecsOrNone is None:
            if other.__dataSpecsOrNone is not None:
                return False
            # need to use keys in comparison...  Which makes it simple.
            return self.__results == other.__results
        else:
            if self.__dataSpecsOrNone != other.__dataSpecsOrNone:
                return False
            return self.__dataSpecsOrNone._dataSetsEquals(self.__results,
                other.__dataSpecsOrNone, other.__results)
    def __ne__(self, other):
        return not (self == other) 
    def __hash__(self):
        # We cache the hash code, like in Java.  This should be thread safe,
        # like in Java, as reading or writing a single instance attribute is
        # supposed to be thread safe:
        # http://effbot.org/zone/thread-synchronization.htm
        # Assuming that's right, the worst that could happen with below is that
        # the hash code is calculated multiple times. But we should be confident
        # that this method will always return the same value.
        hashCode = self.__cachedHashCode
        if hashCode == 0:
            if self.__dataSpecsOrNone is None:
                # started out making a frozenset of the values and getting the
                # hash of that.  But actually using our own method should be
                # faster as we only need to iterate over the values instead of
                # copying them and so on.  Also a frozenset would remove
                # duplicates which would make hash collisions more likely.
                hashCode = private.getDictValuesHash(self.__results)
            else:
                hashCode = self.__dataSpecsOrNone._dataSetsHashCode(
                    self.__results)
            self.__cachedHashCode = hashCode
        return hashCode
    def __repr__(self):
        s = []
        for key in self.__results.keys():
            s.append("'%s': %r" % (key, self.__results[key]))
        s.sort() # As we do for DataSpecs
        return 'DataSets(%r, {%s})' % (self.__dataSpecsOrNone, ', '.join(s))
    @classmethod
    def _check(cls, param, paramName='dataSets'):
        if type(param) is not DataSets:
            raise TypeError(private.wrongTypeString(param, paramName, DataSets))
        return param
    
class Station(private.Immutable):
    __slots__ = ('__id', '__longLat', '__elevation', '__displayName')
    # Python has an id function, but popular opinion seems to be that it's fine
    # for an object to have an id attribute:
    # http://stackoverflow.com/questions/3497883/
    def __init__(self, id, longLat, elevation, displayName):
        self.__id = private.checkStationId(id, False)
        self.__longLat = degreedays.geo.LongLat._check(longLat)
        self.__elevation = degreedays.geo.Distance._check(elevation, 'elevation')
        self.__displayName = private.checkString(displayName, 'displayName')
    def _equalityFields(self):
        return (self.__id, self.__longLat, self.__elevation, self.__displayName)
    def __repr__(self):
        return ("Station('%s', %r, %r, '%s')" %
            (self.__id, self.__longLat, self.__elevation, self.__displayName))
    @property
    def id(self): return self.__id
    @property
    def longLat(self): return self.__longLat
    @property
    def elevation(self): return self.__elevation
    @property
    def displayName(self): return self.__displayName
    @classmethod
    def _check(cls, param, paramName='station'):
        if type(param) is not Station:
            raise TypeError(private.wrongTypeString(param, paramName, Station))
        return param
    
class Source(private.Immutable):
    __slots__ = ('__station', '__distanceFromTarget')
    def __init__(self, station, distanceFromTarget):
        self.__station = Station._check(station)
        self.__distanceFromTarget = degreedays.geo.Distance._check(
            distanceFromTarget, 'distanceFromTarget')
    def _equalityFields(self):
        return (self.__station, self.__distanceFromTarget)
    def __repr__(self):
        return 'Source(%r, %r)' % (self.__station, self.__distanceFromTarget)
    @property
    def station(self): return self.__station
    @property
    def distanceFromTarget(self): return self.__distanceFromTarget
    @classmethod
    def _check(cls, param, paramName='source'):
        if type(param) is not Source:
            raise TypeError(private.wrongTypeString(param, paramName, Source))
        return param
    
class LocationDataResponse(api.Response):
    __slots__ = ('__metadata', '__stationId', '__targetLongLat', '__sources',
        '__dataSets')
    def __init__(self, metadata, stationId, targetLongLat, sources,
            dataSets):
        self.__metadata = api.ResponseMetadata._check(metadata, 'metadata')
        self.__stationId = private.checkStationId(stationId, False)
        self.__targetLongLat = degreedays.geo.LongLat._check(
            targetLongLat, 'targetLongLat')
        self.__sources = private.checkTupleItems(
            tuple(sources), Source._check, 'sources')
        self.__dataSets = DataSets._check(dataSets)
    def _equalityFields(self):
        # metadata isn't included in equality check.
        return (self.__stationId, self.__targetLongLat, self.__sources,
            self.__dataSets)
    def __repr__(self):
        return ("LocationDataResponse(%r, '%s', %r, %r, %r)" %
            (self.__metadata, self.__stationId, self.__targetLongLat,
                self.__sources, self.__dataSets))
    @property
    def metadata(self): return self.__metadata
    @property
    def stationId(self): return self.__stationId
    @property
    def targetLongLat(self): return self.__targetLongLat
    @property
    def sources(self): return self.__sources
    @property
    def dataSets(self): return self.__dataSets
    
class LocationInfoResponse(api.Response):
    __slots__ = ('__metadata', '__stationId', '__targetLongLat', '__sources')
    def __init__(self, metadata, stationId, targetLongLat, sources):
        self.__metadata =  api.ResponseMetadata._check(metadata, 'metadata')
        self.__stationId = private.checkStationId(stationId, False)
        self.__targetLongLat = degreedays.geo.LongLat._check(
            targetLongLat, 'targetLongLat')
        self.__sources = private.checkTupleItems(
            tuple(sources), Source._check, 'sources')
    def _equalityFields(self):
        # metadata isn't included in equality check.
        return (self.__stationId, self.__targetLongLat, self.__sources)
    def __repr__(self):
        return ("LocationInfoResponse(%r, '%s', %r, %r)" %
            (self.__metadata, self.__stationId, self.__targetLongLat,
                self.__sources))
    @property
    def metadata(self): return self.__metadata
    @property
    def stationId(self): return self.__stationId
    @property
    def targetLongLat(self): return self.__targetLongLat
    @property
    def sources(self): return self.__sources
    
    
class DataApi(object):
    def __init__(self, requestProcessor):
        self.__requestProcessor = requestProcessor
    def __checkAndGet(self, request, expectedResponseType):
        response = self.__requestProcessor.process(request)
        if isinstance(response, expectedResponseType):
            return response
        elif isinstance(response, api.FailureResponse):
            code = response.failure.code
            if code.startswith('Location'):
                raise LocationError(response)
            # for general exceptions
            raise api.RequestFailureError._create(response)
        else:
            raise ValueError('For a request of type %r, the RequestProcessor '
                'should return a response of type %r or a FailureResponse, not '
                '%r' % (type(request), expectedResponseType, type(response)))
    def getLocationData(self, locationDataRequest):
        LocationDataRequest._check(locationDataRequest)
        return self.__checkAndGet(
            locationDataRequest, LocationDataResponse)
    def getLocationInfo(self, locationInfoRequest):
        LocationInfoRequest._check(locationInfoRequest)
        return self.__checkAndGet(
            locationInfoRequest, LocationInfoResponse)
    
