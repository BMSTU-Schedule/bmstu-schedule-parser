from termcolor import colored

# don't judge me for this
class AwesomeLogger:

    @staticmethod
    def info(msg):
        print(colored(msg, 'green'))

    @staticmethod
    def shit(msg):
        print(colored(msg, 'red'))
