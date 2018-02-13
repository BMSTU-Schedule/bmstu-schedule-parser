import argparse as ap
from datetime import datetime

from bmstu_schedule import configs, logger as self_made_logger, run


def setup_parser():
    parser = ap.ArgumentParser(description='Bauman Moscow State Technical University EU Schedule iCal parser')
    
    parser.add_argument('-s', '--semester_first_monday', default='05-02-2018', type=date_parser,
                        help='Semester first week monday date')
    parser.add_argument('group', type=str, help='Group code')
    
    return parser


def date_parser(date):
    try:
        return datetime.strptime(date, configs.DATE_FORMAT)
    except ValueError:
        msg = 'date has incorrect format. It must have format: `dd-mm-yyyy`'
        raise ap.ArgumentTypeError(msg)


def main():
    args = setup_parser().parse_args()
    
    try:
        run(args.group.upper(), args.semester_first_monday)
    except ConnectionError as ex:
        self_made_logger.log(ex, 'ERROR')


if __name__ == "__main__":
    main()
