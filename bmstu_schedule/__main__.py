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

import argparse as ap
from datetime import datetime as dt
import requests
from bmstu_schedule import configs, AwesomeLogger, run


def setup_parser():
    parser = ap.ArgumentParser(
        description='Bauman Moscow State Technical University ' +
        'EU Schedule iCal parser')

    parser.add_argument(
        '-s',
        '--semester_first_monday',
        default='',
        type=date_parser,
        help='Semester first week monday date',
    )

    parser.add_argument(
        '-o',
        '--outdir',
        default='.',
        type=str,
        help='Outdir path',
    )

    parser.add_argument(
        'group',
        type=group_code_handler,
        help='Group code'
    )

    return parser


def group_code_handler(group_code):
    return group_code.upper() if group_code != configs.ALL_GROUPS_PARAM else group_code


def get_api_date():
    AwesomeLogger.info('Fetching {}'.format(configs.API_URL))
    r = requests.get(url=configs.API_URL)
    return r.json()['semester_start_date']


def date_parser(date):
    try:
        return dt.strptime(date or get_api_date(), configs.DATE_FORMAT)
    except Exception:
        msg = 'date has incorrect format. It must be: "dd-mm-yyyy", got: "{}"'.format(
            date
        )
        raise ap.ArgumentTypeError(msg)


def main():
    args = setup_parser().parse_args()
    AwesomeLogger.info(
        "Semester start date: {}".format(args.semester_first_monday.date())
        )
    try:
        run(args.group, args.semester_first_monday, args.outdir)
    except ConnectionError as ex:
        AwesomeLogger.shit(ex)


if __name__ == "__main__":
    main()
