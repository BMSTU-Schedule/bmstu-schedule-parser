import requests
import textwrap
from bs4 import BeautifulSoup
from .configs.config import *
from datetime import datetime


class Subject:

    @staticmethod
    def calculateSemesterStartDate(semesterFirstMonday):
        Subject.semesterStartDate = datetime.strptime(semesterFirstMonday, '%d-%m-%Y').timestamp()

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

def run(url, semesterFirstMonday=None):

    Subject.calculateSemesterStartDate(semesterFirstMonday)

    pageHTML = requests.get(url)
    soup = BeautifulSoup(pageHTML.content, 'lxml')
    groupName = soup.select_one('h1').string
    
    file = open(f'{groupName}.ics', 'w')
    file.writelines(textwrap.dedent(iCalHeader))

    for dayIndex, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
        dayTable = day.contents[1]
        rows = dayTable.findAll('tr')
        for row in rows[2:]:
            parseRow(row.contents, dayIndex, file)

    file.write(textwrap.dedent(iCalBottom))
    file.close()
