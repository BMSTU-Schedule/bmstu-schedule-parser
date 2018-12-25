# time-section
DATE_FORMAT = '%d-%m-%Y'
API_URL = 'http://142.93.174.191/start_date/'

# iCal section
STABLE = 17
PERIODIC = 9
ICAL_HEADER = 'BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN'
ICAL_BODY = \
    '''
    BEGIN:VEVENT
    SUMMARY:{summary}
    DTSTART:{startDate}T{startTime}
    DTEND:{endDate}T{endTime}
    RRULE:FREQ=WEEKLY;INTERVAL={interval};COUNT={count};
    LOCATION:{auditorium}
    DESCRIPTION:{professor}
    END:VEVENT'''
ICAL_BOTTOM = '\nEND:VCALENDAR'

# bmstu
MAIN_URL = 'https://students.bmstu.ru'
GROUPS_LIST_URL = '/schedule/list'


# logic
ALL_GROUPS_PARAM = 'all'

