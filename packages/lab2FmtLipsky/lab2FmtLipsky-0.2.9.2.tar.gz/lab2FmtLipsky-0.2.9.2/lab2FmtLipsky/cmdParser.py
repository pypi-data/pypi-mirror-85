import argparse
import logging

logger = logging.getLogger('Formatter')


class CmdParser:
    """
    CmdParser

    1.list of commands
    2.parsing inputted command
    3.divide inputted command and save to dictionary
    """

    def __init__(self):
        pass

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(prog='Lab1V7', description='Danial\'s console app', add_help=True)
        parser.add_argument('-f', '--file', help='put full_path/name_of_file for checking')
        parser.add_argument('-d', '--directory', help='put full_path/name_of_directory for checking')
        parser.add_argument('-p', '--project', help='put full_path/name_of_project for checking')
        parser.add_argument('-ff', '--fixed', help='if you would like to format file - put True, else False (F is def)', default=False)
        parser.add_argument('-v', '--verify', help='verify of formatting correctness', default=True)

        args = parser.parse_args()
        args_dict = vars(args)

        if len(args_dict) == 0:
            print('Wrong usage')

        logger.debug(f'Received arguments: {args_dict}')
        return args_dict
