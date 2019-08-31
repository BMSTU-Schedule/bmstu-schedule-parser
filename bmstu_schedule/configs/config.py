# time-section
DATE_FORMAT = '%d-%m-%Y'
API_URL = 'https://bmstu-schedule.ru/start_date/'

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

# physical culture
PC_LESSON_KEYREGEX = r'.*спорту.*'
PC_LESSONS_TIMES_MAPPING = {
    '083000': ('081500','094500'),
    '101500': ('100000','113000'),
    '120000': ('122000','135000'),
    '135000': ('140500','153500'),
    '154000': ('155000','172000'),
    '172500': ('172500','185500'),
}