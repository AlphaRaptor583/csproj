import datetime # this module handles timeslots
def format_time(time_str: str): # fixes time formatting for database compatibility
    h,m = map(int, time_str.split(":"))
    return datetime.time(hour=h, minute=m)
def next_available_timeslots(start_time, end_time, duration):
    slots = []
    current = datetime.datetime.combine(datetime.date.today(), start_time)
    end_dt = datetime.datetime.combine(datetime.date.today(), end_time)
    delta = datetime.timedelta(minutes=duration)
    while current + delta <= end_dt:
        slots.append(current.strftime("%H:%M"))
        current += delta
    return slots
