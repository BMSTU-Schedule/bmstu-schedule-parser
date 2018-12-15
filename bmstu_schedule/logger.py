from termcolor import colored

class AwesomeLogger:

    @staticmethod
    def info(msg):
        print(colored(msg, 'green'))

    @staticmethod
    def shit(msg):
        print(colored(msg, 'red'))
