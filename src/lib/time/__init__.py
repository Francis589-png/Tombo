"""
Tombo Time Library - Date and Time Operations
"""
import time as py_time
import datetime

def tombo_now():
    """Get current datetime."""
    return datetime.datetime.now()

def tombo_today():
    """Get current date."""
    return datetime.date.today()

def tombo_utc_now():
    """Get current UTC datetime."""
    return datetime.datetime.utcnow()

def tombo_time():
    """Get current time as seconds since epoch."""
    return py_time.time()

def tombo_sleep(seconds):
    """Sleep for specified seconds."""
    py_time.sleep(float(seconds))
    return None

def tombo_delay(milliseconds):
    """Sleep for specified milliseconds."""
    py_time.sleep(float(milliseconds) / 1000.0)
    return None

def tombo_timestamp():
    """Get current timestamp."""
    return int(py_time.time())

def tombo_timezone():
    """Get local timezone offset in seconds."""
    return -py_time.timezone if py_time.daylight == 0 else -py_time.altzone

def tombo_date(year, month, day):
    """Create a date object."""
    return datetime.date(int(year), int(month), int(day))

def tombo_datetime(year, month, day, hour=0, minute=0, second=0):
    """Create a datetime object."""
    return datetime.datetime(int(year), int(month), int(day), 
                            int(hour), int(minute), int(second))

def tombo_date_add(date, days=0, months=0, years=0):
    """Add days/months/years to a date."""
    import dateutil.relativedelta as rd
    try:
        delta = rd.relativedelta(days=int(days), months=int(months), years=int(years))
        return date + delta
    except:
        # Fallback if dateutil not available
        date = date + datetime.timedelta(days=int(days))
        return date

def tombo_date_sub(date, days=0, months=0, years=0):
    """Subtract days/months/years from a date."""
    return tombo_date_add(date, -days, -months, -years)

def tombo_date_diff(date1, date2):
    """Get difference between two dates in days."""
    if isinstance(date1, datetime.datetime) and isinstance(date2, datetime.datetime):
        return (date1 - date2).days
    elif isinstance(date1, datetime.date) and isinstance(date2, datetime.date):
        return (date1 - date2).days
    return 0

def tombo_date_format(date, fmt='%Y-%m-%d'):
    """Format date as string."""
    if isinstance(date, (datetime.date, datetime.datetime)):
        return date.strftime(str(fmt))
    return str(date)

def tombo_date_parse(date_str, fmt='%Y-%m-%d'):
    """Parse string to date."""
    try:
        return datetime.datetime.strptime(str(date_str), str(fmt)).date()
    except ValueError as e:
        raise ValueError(f"Cannot parse date '{date_str}': {e}")

# Calendar operations
def tombo_year(date):
    """Get year from date."""
    if isinstance(date, (datetime.date, datetime.datetime)):
        return date.year
    return 0

def tombo_month(date):
    """Get month from date."""
    if isinstance(date, (datetime.date, datetime.datetime)):
        return date.month
    return 0

def tombo_day(date):
    """Get day from date."""
    if isinstance(date, (datetime.date, datetime.datetime)):
        return date.day
    return 0

def tombo_hour(dt):
    """Get hour from datetime."""
    if isinstance(dt, datetime.datetime):
        return dt.hour
    return 0

def tombo_minute(dt):
    """Get minute from datetime."""
    if isinstance(dt, datetime.datetime):
        return dt.minute
    return 0

def tombo_second(dt):
    """Get second from datetime."""
    if isinstance(dt, datetime.datetime):
        return dt.second
    return 0

def tombo_weekday(date):
    """Get weekday (0=Monday, 6=Sunday)."""
    if isinstance(date, (datetime.date, datetime.datetime)):
        return date.weekday()
    return 0

def tombo_isoweekday(date):
    """Get ISO weekday (1=Monday, 7=Sunday)."""
    if isinstance(date, (datetime.date, datetime.datetime)):
        return date.isoweekday()
    return 0

def tombo_is_leap_year(year):
    """Check if year is leap year."""
    year = int(year)
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def tombo_days_in_month(year, month):
    """Get number of days in month."""
    year = int(year)
    month = int(month)
    if month == 2:
        return 29 if tombo_is_leap_year(year) else 28
    elif month in (4, 6, 9, 11):
        return 30
    else:
        return 31

# Timing utilities
class StopWatch:
    """Simple stopwatch for timing."""
    def __init__(self):
        self.start_time = None
        self.elapsed = 0
    
    def start(self):
        self.start_time = py_time.time()
        self.elapsed = 0
        return self
    
    def stop(self):
        if self.start_time:
            self.elapsed = py_time.time() - self.start_time
            self.start_time = None
        return self
    
    def reset(self):
        self.start_time = None
        self.elapsed = 0
        return self
    
    def time(self):
        if self.start_time:
            return py_time.time() - self.start_time
        return self.elapsed

def tombo_stopwatch():
    """Create a stopwatch object."""
    return StopWatch()

def tombo_measure(func, *args):
    """Measure time to run a function."""
    start = py_time.time()
    result = func(*args)
    elapsed = py_time.time() - start
    return {
        'result': result,
        'time': elapsed
    }

def register(env):
    """Register time library functions in the interpreter environment."""
    functions = {
        # Time functions
        'now': tombo_now,
        'today': tombo_today,
        'utc_now': tombo_utc_now,
        'time': tombo_time,
        'sleep': tombo_sleep,
        'delay': tombo_delay,
        'timestamp': tombo_timestamp,
        'timezone': tombo_timezone,
        
        # Date operations
        'date': tombo_date,
        'datetime': tombo_datetime,
        'date_add': tombo_date_add,
        'date_sub': tombo_date_sub,
        'date_diff': tombo_date_diff,
        'date_format': tombo_date_format,
        'date_parse': tombo_date_parse,
        
        # Calendar
        'year': tombo_year,
        'month': tombo_month,
        'day': tombo_day,
        'hour': tombo_hour,
        'minute': tombo_minute,
        'second': tombo_second,
        'weekday': tombo_weekday,
        'isoweekday': tombo_isoweekday,
        'is_leap_year': tombo_is_leap_year,
        'days_in_month': tombo_days_in_month,
        
        # Timing
        'stopwatch': tombo_stopwatch,
        'measure': tombo_measure,
    }
    
    for name, func in functions.items():
        env.set(name, func)
