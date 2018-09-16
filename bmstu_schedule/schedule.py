import re
import textwrap
import sys
import requests

from bs4 import BeautifulSoup as bsoup
from datetime import timedelta as tdelta
from bmstu_schedule import configs, logger as self_made_logger


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
                            } else 1),
                        denominator=bool(c // 4)
                    )
                )
            except (IndexError, AttributeError):
                pass

        Lesson(timing, subjects).write_ics_to_file(file)


def requester(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        raise ConnectionError('No internet connection')


def get_url_for_group(group_id):
    self_made_logger.log('Going to schedules list page')
    list_page_response = requester(configs.MAIN_URL + configs.GROUPS_LIST_URL)
    self_made_logger.log('Parsing your group url')

    soup = bsoup(list_page_response.content, 'lxml')
    group_href_button = soup.find(
            re.compile('(a|span)'), {
                'class': re.compile('.*btn btn-sm btn-default text-nowrap.*')
            }, text=re.compile(r'.*\ {}.*'.format(group_id)))

    self_made_logger.log('{} group found'.format(group_id))
    return configs.MAIN_URL + group_href_button.attrs['href']


def run(group_id, semester_first_monday, outdir):
    Subject.semester_start_date = semester_first_monday

    try:
        page_html = requester(get_url_for_group(group_id))
    except AttributeError:
        self_made_logger.log(
            'There is no schedule for the group you specified.',
            'ERROR')
        sys.exit(-1)

    self_made_logger.log('Going to your group schedule page')
    soup = bsoup(page_html.content, 'lxml')
    self_made_logger.log('Parsing your schedule')
    group_name = soup.select_one('h1').string

    try:
        filename = '{}/{}.ics'.format(outdir, group_name)
        with open(filename, 'w', encoding='u8') as fp:
            fp.writelines(textwrap.dedent(configs.ICAL_HEADER))

            for dID, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
                day_table = day.contents[1]
                rows = day_table.findAll('tr')
                for row in rows[2:]:
                    parse_row(row.contents, dID, fp)

            fp.write(textwrap.dedent(configs.ICAL_BOTTOM))
    except FileNotFoundError:
        self_made_logger.log(
            'No such file or directory: {}'.format(outdir), 'ERROR')
        return

    self_made_logger.log('Done!')
    self_made_logger.log('File saved at {}/{}.ics'.format(outdir, group_name))
    self_made_logger.log('Now you can import it.')
