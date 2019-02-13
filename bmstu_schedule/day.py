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

import textwrap
import re

from datetime import timedelta as tdelta
from bmstu_schedule import configs

class Subject:
    semester_start_date = None

    def __init__(self, info, subject_day_index, weeks_interval, denominator):
        self.type, self.name, self.auditorium, self.professor = info

        time_shift = denominator * 7 + subject_day_index
        self.start_date = (
            self.semester_start_date + tdelta(days=time_shift)
        ).strftime('%Y%m%d')
        self.weeks_interval = weeks_interval


class Lesson:

    def __init__(self, timing, subjects):
        self.start_time, self.end_time = map(
            lambda string: string.replace(':', '') + '00',
            timing.split(' - ')
        )
        self.subjects = subjects

    def write_ics_to_file(self, file):
        for subject in self.subjects:
            if re.match(configs.PC_LESSON_KEYREGEX, subject.name):
                beginning, ending = configs.PC_LESSONS_TIMES_MAPPING[self.start_time]
            else:
                beginning, ending = self.start_time, self.end_time

            event = configs.ICAL_BODY.format(
                summary='{} {}'.format(subject.type or '', subject.name),
                startDate=subject.start_date,
                startTime=beginning,
                endDate=subject.start_date,
                endTime=ending,
                interval=subject.weeks_interval,
                count=configs.STABLE if subject.weeks_interval == 1
                else configs.PERIODIC,
                auditorium=subject.auditorium or '',
                professor=subject.professor or ''
            )
            file.write(textwrap.dedent(event))


def parse_row(cells, day_number, file):
    if len(set(cell for cell in cells[3:5])) > 1:
        subjects = []
        timing = cells[1].string

        for c in range(3, 5):
            try:
                subjects.append(
                    Subject(
                        (cells[c].contents[i].string for i in range(0, 7, 2)),
                        day_number,
                        weeks_interval=(
                            2 if cells[3].attrs != {
                                'colspan': '2'
                            } else 1
                        ),
                        denominator=(c == 4)
                    )
                )
            except (IndexError, AttributeError):
                pass

        Lesson(timing, subjects).write_ics_to_file(file)


