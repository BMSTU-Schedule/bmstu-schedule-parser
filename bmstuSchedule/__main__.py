import argparse

from datetime import datetime
from bmstuSchedule import run
from bmstuSchedule.configs.config import *


def argConfig():
    parser = argparse.ArgumentParser(description='Bauman Moscow State Technical University EU Schedule iCal parser')
    parser.add_argument('-s', '--semester_first_monday', default='05-02-2018', type=date_parser,
                        help='Semester first week monday date')
    parser.add_argument('group', type=str, help='Group code')
    return parser


def date_parser(date):
    try:
        return datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        msg = 'date has incorrect format. It must have format: `dd-mm-yyyy`'
        raise argparse.ArgumentTypeError(msg)


def main(args=None):
    namespace = argConfig().parse_args(args)
    try:
        run(namespace.group.upper(), namespace.semester_first_monday)
    except ConnectionError as ex:
        selfMadeLogger(ex, 'ERROR')


if __name__ == "__main__":
    main()
