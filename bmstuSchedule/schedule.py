import re
import textwrap
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from bmstuSchedule.configs.config import *


class Subject:

    @staticmethod
    def calculateSemesterStartDate(beginningDate):
        Subject.semesterStartDate = datetime.strptime(beginningDate, '%d-%m-%Y').timestamp()

    def __init__(self, info, subjectDayIndex, weeksInterval, denominator):
        self.name, self.auditorium, self.professor = info
        timeShift = (denominator * 7 + subjectDayIndex) * SECONDS_IN_A_DAY

        self.startDate = datetime.fromtimestamp(Subject.semesterStartDate + timeShift).strftime('%Y%m%d')
        self.weeksInterval = weeksInterval

    def getInfo(self):
        return self.name, self.auditorium, self.professor, self.startDate, self.weeksInterval


class Lesson:

    def __init__(self, timing, subjects):
        self.startTime, self.endTime = map(lambda string: string.replace(':', '') + '00', timing.split(' - '))
        self.subjects = subjects

    def writeICSToFile(self, file):
        for subject in self.subjects:
            event = iCalBody.format(
                summary=subject.name,
                startDate=subject.startDate,
                startTime=self.startTime,
                endDate=subject.startDate,
                endTime=self.endTime,
                interval=subject.weeksInterval,
                auditorium=subject.auditorium,
                professor=subject.professor
            )
            file.write(textwrap.dedent(event))


def parseRow(cells, dayNumber, file):
    if len(set(cell for cell in cells[3:5])) > 1:
        subjects = []
        timing = cells[1].string

        for c in range(3, 5):
            try:
                subjects.append(Subject((cells[c].contents[i].string for i in range(0, 5, 2)),
                                        dayNumber,
                                        weeksInterval=(2 if cells[3].attrs != {'colspan': '2'} else 1),
                                        denominator=bool(c // 4)))
            except (IndexError, AttributeError):
                pass

        Lesson(timing, subjects).writeICSToFile(file)


def getUrlForGroup(groupID):
    selfMadeLogger('Going to schedules list page')
    listPageResponse = requests.get(mainURL + groupsListURL)
    selfMadeLogger('Parsing your group url')
    soup = BeautifulSoup(listPageResponse.content, 'lxml')
    groupHrefButton = soup.find('a', {'class': 'btn btn-sm btn-default text-nowrap'},
                                text=re.compile('.*{}.*'.format(groupID)))
    return mainURL + groupHrefButton.attrs['href']


def run(groupID, semesterFirstMonday):
    Subject.calculateSemesterStartDate(semesterFirstMonday)

    try:
        pageHTML = requests.get(getUrlForGroup(groupID))
    except AttributeError:
        selfMadeLogger('There is no schedule for the group you specified.', 'ERROR')
        raise SystemExit

    selfMadeLogger('Going to your schedule page')
    soup = BeautifulSoup(pageHTML.content, 'lxml')
    selfMadeLogger('Parsing your schedule')
    groupName = soup.select_one('h1').string

    file = open('{}.ics'.format(groupName), 'w')
    file.writelines(textwrap.dedent(iCalHeader))

    for dayIndex, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
        dayTable = day.contents[1]
        rows = dayTable.findAll('tr')
        for row in rows[2:]:
            parseRow(row.contents, dayIndex, file)

    file.write(textwrap.dedent(iCalBottom))
    file.close()
    selfMadeLogger('Done!')
    selfMadeLogger('Now you can import it.')
