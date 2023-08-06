#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    thegmu_im_excel_file.py
    ~~~~~~~~~~~~~~~~~~~~~~~

    Library that loads existing Excel catalog files and manages image files
    based upon individual file commands in the spreadsheet.


"""

import os
from openpyxl import load_workbook as OpenpyxlLoadworkbook


class TheGMUImageManageExcelFile():
    """Load a previously created Excel catalog file and execute individual image
    commands. Does not change the Excel file, only read it.
    """

    def _excel_delete_files(self, cmd_name, excel_file):
        """Delete image files per user request where the
        Excel file rows have already been set.

        :param cmd_name: display and logging only.
        :param excel_file: the spreadsheet file to load.

        :return count: count of files deleted.
        """
        working_directory = self.data['catalog']['working_directory']

        os.chdir(working_directory)

        self.log.debu("%s %s file delete." % (cmd_name, excel_file))

        bad_delete_request = [x for x in self.data[excel_file]['rows']
                              if (x['delete'] not in ('delete', None))]

        for row in bad_delete_request:
            self.log.warn("%s: " % (row['file_name'], ) +
                          "'delete' column value 'delete' is the only " +
                          "accepted value, got '%s'." % (row['delete'], ))

        delete_request = [x for x in self.data[excel_file]['rows']
                          if (x['delete'] == 'delete')]

        if (len(delete_request) == 0):
            return 0

        delete_count = 0
        for row in delete_request:
            if (not os.path.exists(row['file_name'])):
                self.log.prog("%s: file not found, delete ignored." %
                              (row['file_name'], ))
            else:
                os.unlink(row['file_name'])
                self.log.prog("'%s' file deleted." % (row['file_name'], ))
                delete_count += 1

        self.cd_start_dir()

        self.data[excel_file]['delete_count'] = delete_count

        return delete_count

    def _excel_file_load(self, cmd_name, excel_file):
        """Set the self.data[excel_file]['rows'] by
        loading a specified file presumably updated by a user for
        individual file commands.
        
        :param cmd_name: display only.
        :param excel_file: file on disk to read in.
        """
        working_directory = self.data['catalog']['working_directory']

        os.chdir(working_directory)

        if (not os.path.isfile(excel_file)):
            raise OSError("%s: %s file not found." % (cmd_name, excel_file))

        book = OpenpyxlLoadworkbook(filename=excel_file, read_only=True)

        sheet = book['Catalog']
        excel_rows = []

        for row_index, sheet_row in enumerate(sheet.rows):

            row = [x.value for x in sheet_row]
            if (row_index == 0):
                header = row
            else:
                excel_rows.append(dict(zip(header, row)))

        self.data[excel_file]['rows'] = excel_rows

        self.cd_start_dir()

    def excel_file_commands(self, cmd_name, excel_file,
                            working_directory=None,
                            catalog_file=None):
        """Run individual file commands from an Excel spreadsheet the
        user as updated.
        
        :param cmd_name: command name for display only.
        :param excel_file: user requested file taken from the command file.
        :param working_directory: the image directory. 
        :param catalog_file: the catalog file of images.   
        """

        self.catalog_init(cmd_name, working_directory, catalog_file)

        self.data[excel_file] = dict()

        self._excel_file_load(cmd_name, excel_file)

        self._excel_delete_files(cmd_name, excel_file)
