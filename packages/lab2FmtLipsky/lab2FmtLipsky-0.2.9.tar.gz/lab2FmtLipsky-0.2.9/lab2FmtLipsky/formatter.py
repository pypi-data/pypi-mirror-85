import logging

from fileFormatter import FileFormatter
from cmdParser import CmdParser
import log


logger = logging.getLogger('Formatter')

logger.debug(f'program started')


def run():
    FileFormatter(CmdParser.parse_arguments()).run()

run()


logger.debug(f'program finished')

#
# import lab2FmtLipsky
#
# lab2FmtLipsky.FileFormatter(lab2FmtLipsky.CmdParser.parse_arguments()).run()
