from termcolor import colored


def log(msg, level='INFO'):
    print(colored(msg, 'red' if level != 'INFO' else 'green'))
