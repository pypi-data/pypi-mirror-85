# -*- coding: utf-8 -*-

"""bootstrap.bootstrap: provides entry point main()."""

import logging

from RubyFormatter.fileFormatter import FileFormatter
from RubyFormatter.cmdParser import CmdParser
# import RubyFormatter.log

__version__ = "0.2.5"

logger = logging.getLogger('Formatter')

logger.debug(f'program started')


def run():
    FileFormatter(CmdParser.parse_arguments()).run()


def main():
    print("Executing bootstrap version %s." % __version__)
    print("formatter is run")
    run()


logger.debug(f'program finished')


