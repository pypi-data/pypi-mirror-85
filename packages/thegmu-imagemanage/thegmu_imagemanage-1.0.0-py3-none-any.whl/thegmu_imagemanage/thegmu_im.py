#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    thegmu_imagemanage.py
    ~~~~~~~~~~~~~~~~~~~~~

    Command line tool to manage images based on personal requirements and
    not public utility.

    #. Create a catalog for grouping by size, dimensions, format,
    creation date, etc. for manual management.
    #. Rename files to sort by file name using any of the group
    dimensions.

"""
import argparse
import os
import re
import sys

from thegmu_imagemanage import thegmu_log
from thegmu_imagemanage.thegmu_im_catalog import TheGMUImageManageCatalog
from thegmu_imagemanage.thegmu_im_catalog_excel import \
    TheGMUImageManageCatalogExcel
from thegmu_imagemanage.thegmu_im_convert import TheGMUImageManageConvert
from thegmu_imagemanage.thegmu_im_errors import \
    TheGMUImageManageBadCommandError
from thegmu_imagemanage.thegmu_im_excel_file import \
    TheGMUImageManageExcelFile
from thegmu_imagemanage.thegmu_im_os import TheGMUImageManageOS
from thegmu_imagemanage.thegmu_im_util import TheGMUImageManageUtil


class TheGMUImageManage(TheGMUImageManageCatalog,
                        TheGMUImageManageCatalogExcel,
                        TheGMUImageManageConvert,
                        TheGMUImageManageExcelFile,
                        TheGMUImageManageOS,
                        TheGMUImageManageUtil):
    """Program control that parses command line options and
    dispatches to functionality based on those options.
    """

    COMMAND_FILE_DEFAULT = 'thegmu_imagemanage.commands.txt'

    TLA = 'gim'  # TheGMULog Three Letter Abbreviation

    COMMENT_REGEX = re.compile(r"^#|^$")
    USAGE = """
    thegmu_imagemanage.py [options] [command_file]

    command_file:
        default:
            'thegmu_iamgemmanage.commands.txt' is default when none given.
        format:
            One command per line with the parameters space seperated.

"""

    def __init__(self):
        """Initialize logging, initialize variables to constants."""

        self.args = None
        self.command_file = None
        self.commands = None
        self.data = None
        self.image_formats = None
        self.log = thegmu_log.TheGMULog(self.TLA)
        self.test_count = None

    def cd_start_dir(self):
        """Change directory to the directory the program was started in."""
        os.chdir(self.data['start_dir'])

    def command_not_found(self, *kwargs):
        """command_not_found is invoked when a command listed in the
        command file supplied is not found. Raises an exception."""

        self.log.debu("'%s' command not fouund." % (kwargs[0], ))
        raise TheGMUImageManageBadCommandError("'%s' command not fouund %s" %
                                               (kwargs[0], kwargs))

    def init_args(self, argv=None):
        """argparse.ArgumentParser

        :param argv: If None then sys.argv is used.
            Passing this parameter is for testing purposes.

        """
        if (argv is None):
            argv = sys.argv

        parser = argparse.ArgumentParser(
            description=TheGMUImageManage.USAGE,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help="""Output debug messages.""")

        parser.add_argument(
            'command_file',
            nargs='?',
            default=self.COMMAND_FILE_DEFAULT)

        self.args = parser.parse_args(args=argv)
        if (self.args.command_file == self.COMMAND_FILE_DEFAULT):
            if (not os.path.isfile(self.args.command_file)):
                self.log.warn("""'%s' \
file neeeds to be created in the working \
directory before running this program without options,
showing help instead.
""" % (self.args.command_file, ))
                return self.init_args(['-h', ])

        self.log.prog("'%s' command file name requested." %
                      (self.args.command_file))

        if (not os.path.isfile(self.args.command_file)):
            raise IOError("%s file not found." % self.args.command_file)

        if self.args.verbose:
            self.log.set_level_from_string("DEBUG")

        self.command_file = self.args.command_file
        self.data = dict()
        self.data['start_dir'] = os.getcwd()
        return None

    def init_commands_from_command_file(self):
        """Read in the command file, filtering out comment lines that
        start with a hash. Inialitzie the array of commands.
        """
        self.log.debu("Processing command file: %s" % (self.command_file, ))
        self.commands = []
        skip_re = self.COMMENT_REGEX

        with open(self.command_file, 'r') as command_fh:

            next_command = command_fh.readline()
            while(next_command):
                next_command = next_command.strip()
                self.log.debu(next_command)
                if (not skip_re.match(next_command)):
                    self.commands.append(next_command)
                next_command = command_fh.readline()

    def init_image_formats(self):
        """Set 'self.image_formats using the utilility library."""

        if (self.image_formats is None):
            self.image_formats = self.get_image_formats()

    def run_commands(self):
        """Using commands already appended to self.commands as a line
        of text that is space delimited, dispatch the command from the
        method in this object of the same method name. Abort the program
        if a command is not recognized.
        """

        for cmd_line in self.commands:
            cmd = cmd_line.split()
            self.log.debu("cmd: %s" % (cmd, ))
            command = cmd[0]

            command_method = getattr(self, command, self.command_not_found)

            self.log.debu("command_method: %s" % (command_method, ))
            command_method(*cmd)

    @staticmethod
    def run(argv):
        """Run-time and test invocation runner.
        
        :param argv: sys.argv command line paramater. 
        """

        gim = TheGMUImageManage()

        gim.init_args(argv)

        gim.init_commands_from_command_file()

        gim.run_commands()


def main(argv):
    """Command line and test invocation runner.

   :param argv: command line sys.argv is the expected format
    and is not used directly but handed of to parsearg.
    """

    gim = TheGMUImageManage()
    gim.run(argv)


if __name__ == '__main__':
    main(sys.argv[1:])
