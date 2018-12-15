import re
import sys
import json
from datetime import timedelta as tdelta

import textwrap
import requests
from bs4 import BeautifulSoup as bsoup
from bmstu_schedule import configs
from bmstu_schedule.logger import AwesomeLogger


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


def requester(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        raise AwesomeLogger.shit("No internet connection")


def group_code_formatter(group_url):
    try:
        return group_url.text.lstrip()[:11].rstrip()
    except AttributeError:
        AwesomeLogger.shit(
            'There is no schedule for the group you specified.')
        sys.exit(-1)



def unload_all_groups(soup, outdir):
    all_urls = soup.find_all(
        'a', 'btn btn-sm btn-default text-nowrap')
    urls_count = len(all_urls)

    mapping = []
    for url_id, group_url_button in enumerate(all_urls):
        try:
            valid_group_code = group_code_formatter(group_url_button)
            AwesomeLogger.info('Processing {} | {}/{} | [{}%]'.format(
                valid_group_code,
                url_id,
                urls_count,
                round(url_id / urls_count * 100, 2)
            ))

            url = configs.MAIN_URL + group_url_button['href']

            yield (
                valid_group_code,
                url,
            )

            mapping.append({
                "group": valid_group_code,
                "url": url
            })
        except Exception as ex:
            AwesomeLogger.shit((ex, url_id, group_url_button))

    with open(outdir + '/mapping.json', 'w', encoding='utf-8') as mapping_file:
        mapping_file.write(json.dumps(mapping, ensure_ascii=False))


def get_urls(group_code, outdir):
    AwesomeLogger.info('Going to schedules list page')
    list_page_response = requester(configs.MAIN_URL + configs.GROUPS_LIST_URL)
    AwesomeLogger.info('Parsing your group(s) url(s)')
    soup = bsoup(list_page_response.content, 'lxml')

    if group_code != configs.ALL_GROUPS_PARAM:
        group_url_button = soup.find(
            'a', {
                'class': re.compile('.*btn btn-sm btn-default text-nowrap.*')
            }, text=re.compile(r'.*\ {}.*'.format(group_code))
        )
        valid_group_code = group_code_formatter(group_url_button)
        AwesomeLogger.info('{} group found'.format(valid_group_code))
        yield (
            valid_group_code,
            configs.MAIN_URL + group_url_button.attrs['href']
        )
    else:
        yield from unload_all_groups(soup, outdir)


def run(group_code, semester_first_monday, outdir):
    Subject.semester_start_date = semester_first_monday

    for valid_group_code, url in get_urls(group_code, outdir):
        AwesomeLogger.info('Going to your group schedule page')
        page_html = requester(url)

        AwesomeLogger.info('Parsing your schedule')
        soup = bsoup(page_html.content, 'lxml')

        try:
            filename = '{}/{}.ics'.format(outdir, valid_group_code)
            with open(filename, 'w', encoding='u8') as fp:
                fp.writelines(textwrap.dedent(configs.ICAL_HEADER))

                for dID, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
                    day_table = day.contents[1]
                    rows = day_table.findAll('tr')
                    for row in rows[2:]:
                        parse_row(row.contents, dID, fp)

                fp.write(textwrap.dedent(configs.ICAL_BOTTOM))
        except FileNotFoundError:
            AwesomeLogger.shit(
                'No such file or directory: {}'.format(outdir))
            return

        AwesomeLogger.info('Done!')
        AwesomeLogger.info('File saved at {}/{}.ics'.format(outdir, valid_group_code))
        AwesomeLogger.info('Now you can import it.')

