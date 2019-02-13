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

import json
import requests
import re
import sys

from bmstu_schedule.logger import AwesomeLogger
from bmstu_schedule import configs

def group_code_formatter(group_url):
    try:
        return group_url.text.lstrip()[:11].rstrip()
    except AttributeError:
        AwesomeLogger.shit(
            'There is no schedule for the group you specified.')
        sys.exit(-1)


def get_urls(group_code, outdir, soup):

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
