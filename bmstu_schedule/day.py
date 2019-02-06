import textwrap

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
            event = configs.ICAL_BODY.format(
                summary='{} {}'.format(subject.type or '', subject.name),
                startDate=subject.start_date,
                startTime=self.start_time,
                endDate=subject.start_date,
                endTime=self.end_time,
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


