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
import requests
from bs4 import BeautifulSoup as bsoup
from bmstu_schedule import configs
from bmstu_schedule.logger import AwesomeLogger
from bmstu_schedule.group_page_search import get_urls, unload_all_groups
from bmstu_schedule.day import parse_row, Subject


def run(group_code, semester_first_monday, outdir):
    Subject.semester_start_date = semester_first_monday

    AwesomeLogger.info('Going to schedules list page')
    list_page_response = requests.get(configs.MAIN_URL + configs.GROUPS_LIST_URL)
    AwesomeLogger.info('Parsing your group(s) url(s)')
    soup = bsoup(list_page_response.content, 'lxml')

    for valid_group_code, url in get_urls(group_code, outdir, soup):
        AwesomeLogger.info('Going to your group schedule page')
        page_html = requests.get(url)

        AwesomeLogger.info('Parsing your schedule')
        soup = bsoup(page_html.content, 'lxml')

        try:
            filename = '{}/{}.ics'.format(outdir, valid_group_code)
            with open(filename, 'w', encoding='u8') as ics:
                ics.writelines(textwrap.dedent(configs.ICAL_HEADER))

                for dID, day in enumerate(soup.select('div.col-md-6.hidden-xs')):
                    day_table = day.contents[1]
                    rows = day_table.findAll('tr')
                    for row in rows[2:]:
                        parse_row(row.contents, dID, ics)

                ics.write(textwrap.dedent(configs.ICAL_BOTTOM))
        except FileNotFoundError:
            AwesomeLogger.shit(
                'No such file or directory: {}'.format(outdir))
            return

        AwesomeLogger.info('Done!')
        AwesomeLogger.info('File saved at {}/{}.ics'.format(outdir, valid_group_code))
        AwesomeLogger.info('Now you can import it.')

