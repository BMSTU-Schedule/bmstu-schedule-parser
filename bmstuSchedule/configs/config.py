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
    RRULE:FREQ=WEEKLY;INTERVAL={interval};
    LOCATION:{auditorium}
    DESCRIPTION:{professor}
    END:VEVENT'''
iCalBottom = '\nEND:VCALENDAR'
