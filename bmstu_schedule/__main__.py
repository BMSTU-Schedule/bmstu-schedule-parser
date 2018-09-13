import argparse as ap
from datetime import datetime as dt
import requests
from bmstu_schedule import configs, logger as self_made_logger, run


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
        type=str,
        help='Group code'
    )

    return parser


def get_api_date():
    r = requests.get(url=configs.API_URL)
    self_made_logger.log('Fetching {}'.format(configs.API_URL))
    return r.json()['semester_start_date']


def date_parser(date):
    try:
        return dt.strptime(date or get_api_date(), configs.DATE_FORMAT)
    except ValueError:
        msg = 'date has incorrect format. It must have format: `dd-mm-yyyy`'
        raise ap.ArgumentTypeError(msg)


def main():
    args = setup_parser().parse_args()
    self_made_logger.log(
        "Semester start date: {}".format(args.semester_first_monday.date())
        )
    try:
        run(args.group.upper(), args.semester_first_monday, args.outdir)
    except ConnectionError as ex:
        self_made_logger.log(ex, 'ERROR')


if __name__ == "__main__":
    main()
