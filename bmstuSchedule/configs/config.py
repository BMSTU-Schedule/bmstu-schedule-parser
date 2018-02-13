from termcolor import colored


def selfMadeLogger(msg, level='INFO'):
    print(colored(msg, 'red' if level != 'INFO' else 'green'))


# time-section
DATE_FORMAT = '%d-%m-%Y'

# iCal section
FULL_WEEKS = 17
PART_WEEKS = 8
iCalHeader = 'BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN'
iCalBody = \
    '''
    BEGIN:VEVENT
    SUMMARY:{summary}
    DTSTART:{startDate}T{startTime}
    DTEND:{endDate}T{endTime}
    RRULE:FREQ=WEEKLY;INTERVAL={interval};COUNT={count};
    LOCATION:{auditorium}
    DESCRIPTION:{professor}
    END:VEVENT'''
iCalBottom = '\nEND:VCALENDAR'

# bmstu
mainURL = 'https://students.bmstu.ru'
groupsListURL = '/schedule/list'
