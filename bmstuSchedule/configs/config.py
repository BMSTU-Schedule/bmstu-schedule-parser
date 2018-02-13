# time-section
semesterFirstMonday = '2018/02/05'
SECONDS_IN_A_DAY = 86400

# iCal section
iCalHeader = 'BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN'
iCalBody = \
    '''
    BEGIN:VEVENT
    SUMMARY:{summary}
    DTSTART:{startDate}T{startTime}
    DTEND:{endDate}T{endTime}
    RRULE:FREQ=WEEKLY;INTERVAL={interval};UNTIL=20180601T000000;
    LOCATION:{auditorium}
    DESCRIPTION:{professor}
    END:VEVENT'''
iCalBottom = '\nEND:VCALENDAR'

# bmstu
mainURL = 'https://students.bmstu.ru'
groupsListURL = '/schedule/list'
