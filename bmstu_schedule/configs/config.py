# bmstu-schedule-parser
# Copyright (C) 2018 BMSTU Schedule (George Gabolaev)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

# physical culture
PC_LESSON_KEYREGEX = r'.*(спорту|Физ воспитание).*'
PC_LESSONS_TIMES_MAPPING = {
    '083000': ('081500','094500'),
    '101500': ('100000','113000'),
    '120000': ('122000','135000'),
    '135000': ('140500','153500'),
    '154000': ('155000','172000'),
    '172500': ('172500','185500'),
}