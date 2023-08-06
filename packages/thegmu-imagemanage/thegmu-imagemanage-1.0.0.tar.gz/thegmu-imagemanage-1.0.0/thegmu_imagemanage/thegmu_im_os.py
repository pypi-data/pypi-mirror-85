#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    thegmu_im_os.py
    ~~~~~~~~~~~~~~~~~~~~

    Library that like the python "os" and "os.path" libraries provides
    various destructive and informative file operations.

"""

import os
from collections import OrderedDict
from collections import Counter
import shutil

from thegmu_imagemanage import script
from thegmu_imagemanage.thegmu_im_errors import TheGMUImageManageError


class TheGMUImageManageOS():
    """Operating system services for updating and deleting files.
    ImageMagick may be used to convert from one type to another.
    """

    FLATTEN_SPEC = r""" {}[](),:;<>!'"@#$%^&*|`"""
    JPEG_OPTIMIZE_CMD = 'jpegoptim'
    JPEG_OPTIMIZE_ARGS = ' -q -s -S%i '
    JPEG_OPTIMIZE_MIN_SIZE = 10000

    def _get_duplicate_md5sum_files(self, working_directory, duplicate_sizes,
                                    size_list):
        """List duplicate md5sum files given duplicate size data.
        """
        catalog = self.data['catalog']['current']

        # Optimize md45sum calls by loading previous runs.
        self.catalog_load()
        self.catalog_update()

        md5sum_list = dict()

        os.chdir(working_directory)

        for work_size in duplicate_sizes:
            for work_file in size_list[work_size]:
                work_mtime = catalog[work_file]['epoch']
                work_date = catalog[work_file]['date']
                work_md5sum = catalog[work_file]['md5sum']
                if (work_md5sum is None):
                    work_md5sum = self.get_md5sum(work_file)
                record = [work_file, work_date, work_mtime, ]
                if (work_md5sum in md5sum_list):
                    md5sum_list[work_md5sum].append(record)
                else:
                    md5sum_list[work_md5sum] = [record, ]

        self.cd_start_dir()

        md5sum_duplicate_files = dict((x, md5sum_list[x])
                                      for x in md5sum_list
                                      if (len(md5sum_list[x]) > 1))

        if (len(md5sum_duplicate_files) == 0):
            self.log.prog("No duplicate files deteceted.")
            return None

        for work_md5sum in md5sum_duplicate_files:
            md5sum_duplicate_files[work_md5sum].sort(key=lambda a: a[2])

        return md5sum_duplicate_files

    def _set_duplicate_size_files(self):
        """List duplicate size files before running md5sum for
        optimization.
        """
        catalog = self.data['catalog']['current']
        self.catalog_set_file_stats()

        size_list = dict()
        duplicate_sizes = set()

        for work_file in catalog:
            work_size = catalog[work_file]['size']
            if (work_size in size_list):
                size_list[work_size].append(work_file)
                duplicate_sizes.add(work_size)
            else:
                size_list[work_size] = [work_file, ]

        if (len(duplicate_sizes) == 0):
            self.log.prog("No duplicate files deteceted.")
            return None

        duplicate_sizes = sorted(list(duplicate_sizes))

        for work_size in duplicate_sizes:
            self.log.debu("%s bytes size duplicates: %s" %
                          (work_size, size_list[work_size]))

        return (duplicate_sizes, size_list)

    def flatten_comma_names(self, cmd_name,
                            working_directory=None,
                            catalog_file=None):
        """See flaten_file_names, calls flatten_file_names
        passing a list of a single comma as the spec.
        File names with commas are ignored for processing.
        Use this command to get rid of the comma file names.
        
        :param cmd_name: command name for display only.
        :param working_directory: the immage directory.
        :param catalog_file: the image catalog file.
        
        :return count: the number of files renamed. 
        """

        return self.flatten_file_names(cmd_name, working_directory,
                                       catalog_file, r""",""")

    def flatten_file_names(self, cmd_name,
                           working_directory=None,
                           catalog_file=None,
                           spec=None):
        """Flatten file names means to replace file name puncutation with
        and spaces with underscore '_'. In the event that the
        name already exists then a new version is created with '_N_'.

        :param cmd_name: for logging and display only.
        :param working_directory: any directory subject to override by the \
        catalog library.
        :param catalog_file: previously created catalog file.
        :param spec: a string of characters to flatten.

        :return count: count of file names flattened.
        """

        self.set_directory_files(cmd_name, working_directory, catalog_file)
        working_directory = self.data['catalog']['working_directory']

        if (spec is None):
            spec = self.FLATTEN_SPEC

        spec = spec.replace("_", "")

        self.log.prog(r'"%s" is the list flatten file name characters.' %
                      (spec, ))

        os.chdir(working_directory)
        change_files = []
        for work_file in self.data['catalog']['work_files']:

            new_work_file = work_file

            first_pos = -1
            for spec_char in spec:
                first_pos = new_work_file.find(str(spec_char))
                if (first_pos > -1):
                    break

            if (first_pos == -1):
                continue

            # Special case spaces, replace verbatim with underscore.
            if (spec.find(" ") > -1):
                new_work_file = new_work_file.replace(" ", "_")

            replace_str = ""
            for spec_char in spec:
                new_work_file = new_work_file.replace(
                    str(spec_char), replace_str)

            if (new_work_file != work_file):

                while(os.path.exists(new_work_file) or
                      (new_work_file in [x[1] for x in change_files])):
                    new_work_file = (new_work_file[:first_pos] + "_" +
                                     new_work_file[first_pos:])

                self.log.debu("%s => %s file name flatten." %
                              (work_file, new_work_file))

                if (os.path.exists(new_work_file)):
                    self.log.warn("%s => %s flatten file exists, ignoring." %
                                  (work_file, new_work_file))
                else:
                    change_files.append((work_file, new_work_file))

        for work_file, new_work_file in change_files:
            shutil.move(work_file, new_work_file)

        self.cd_start_dir()

        return len(change_files)

    def jpeg_optimize_size(self, cmd_name, kilobytes,
                           working_directory=None,
                           catalog_file=None):
        """Run the program "jpegoptim" to shrink a jpeg to a target
        size.

        :param cmd_name: for display purposes only.
        :param working_directory: any directory subject to default \
        and override by the catalog library.

        :return count: count of optimized files.
        """

        jpeg_cmd = self.JPEG_OPTIMIZE_CMD

        if (not script.command_exists(jpeg_cmd)):
            raise IOError("'%s' jpeg optimization command not found." %
                          (jpeg_cmd, ))

        jpeg_args = self.JPEG_OPTIMIZE_ARGS
        jpg_size = int(kilobytes) * 1000
        min_size = self.JPEG_OPTIMIZE_MIN_SIZE

        if (jpg_size < min_size):
            msg = "%s: " % cmd_name
            msg += "%i kilobytes is the smallest optimize jpeg size" % min_size
            msg += ", %s is an invalid size. " % kilobytes
            raise TheGMUImageManageError(msg)

        self.catalog(cmd_name, working_directory, catalog_file)
        working_directory = self.data['catalog']['working_directory']

        catalog = self.data['catalog']['current']
        self.log.prog("%s: %s files found." %
                      (cmd_name, len(catalog), ))

        jpg_files = [x for x in catalog if catalog[x]['format'] == 'JPEG']
        self.log.debu("%s: found %s jpg files." % (cmd_name, len(jpg_files), ))
        jpg_check_size = jpg_size + int(jpg_size / 9)
        jpg_files = [x for x in jpg_files if catalog[x]['size'] >
                     jpg_check_size]

        self.log.prog("%s: found %s jpg files size > %sKB" %
                      (cmd_name, len(jpg_files), kilobytes))

        os.chdir(working_directory)

        jpeg_args = jpeg_args % int(kilobytes)

        for work_file in jpg_files:
            cmd = "%s %s %s" % (jpeg_cmd, jpeg_args, work_file)
            script.runcmd(cmd, console=True)

        self.cd_start_dir()
        return len(jpg_files)

    def set_duplicate_files(self, cmd_name, working_directory=None):
        """List duplicate files in the working directory where
        working_directory is defined by the catalog
        library.

        Duplicate files must first have equal file sizes. Only after
        equal file size is determined is the md5sum calculated.

        The original is the one with the earliest time stamp.

        :param cmd_name: for display purposes only.
        :param working_directory: any directory subject to default \
        and override by the catalog library.

        :return count: count of duplicate files.
        """

        count = self.set_directory_files(cmd_name, working_directory)
        self.catalog_load()
        self.catalog_update()

        if (count == 0):
            return 0

        working_directory = self.data['catalog']['working_directory']
        self.data['duplicate_files'] = []

        size_result = self._set_duplicate_size_files()

        if (size_result is None):
            return 0

        (duplicate_sizes, size_list) = size_result

        md5sum_duplicate_files = \
            self._get_duplicate_md5sum_files(working_directory,
                                             duplicate_sizes, size_list)

        if (md5sum_duplicate_files is None):
            return 0

        duplicates = dict()
        for record in list(md5sum_duplicate_files.values()):
            duplicates[','.join(str(x) for x in record[0])] = record[1:]

        duplicate_files = []
        for original in duplicates:
            duplicate_files += [x[0] for x in duplicates[original]]
            duplicate = ','.join(str(x) for x in duplicates[original])
            self.log.prog("%s original => %s" %
                          (original, duplicate))

        self.log.prog("Duplicate files found %s: %s" %
                      (len(duplicate_files), ' '.join(duplicate_files)))

        self.data['duplicate_files'] = duplicate_files

        return len(duplicate_files)

    def list_empty_files(self, cmd_name, working_directory=None):
        """List empty files in the working directory where
        working_directory is defined by TheGMUImageManageCatalog
        library.

        :param command_name: 'remove_empty_files'
        :param working_directory: any directory subject to default \
        and override by the catalog library.
        
        :return count: count of empty files.
        """

        self.set_directory_files(cmd_name, working_directory)

        catalog = self.data['catalog']['current']

        empty_files = [x for x in catalog if catalog[x]['size'] == 0]

        self.data['empty_files'] = empty_files

        self.log.prog('%s found %s empty files:%s%s' %
                      (working_directory,
                       len(empty_files),
                       os.linesep,
                       ' '.join(empty_files)
                       ))
        return len(empty_files)

    def remove_duplicate_files(self, cmd_name, working_directory=None):
        """Remove duplicate files in a working_directory as determined
        by the catalog library.

        :param cmd_name: reporting name only.
        :param working_directory: a directory that can be None or \
        possiby overridden by emnvironment variable.

        :return count: count of files deleted.
        """

        self.set_duplicate_files(cmd_name, working_directory)
        duplicate_files = self.data['duplicate_files']

        if (len(duplicate_files) == 0):
            self.log.prog("%s no duplicate files detected." % (cmd_name, ))
            return 0

        working_directory = self.data['catalog']['working_directory']
        os.chdir(working_directory)

        duplicate_files = self.data['duplicate_files']

        if (len(duplicate_files) == 0):
            return 0

        for duplicate_file in duplicate_files:
            os.unlink(duplicate_file)

        self.cd_start_dir()

        self.log.prog("%s %s duplicate files deleted: %s" %
                      (cmd_name, len(duplicate_files),
                       ' '.join(duplicate_files)))

        self.data['duplicate_files'] = []
        return len(duplicate_files)

    def remove_empty_files(self, cmd_name, working_directory=None):
        """Remove empty files in a working_directory as determined
        by the catalog library.

        :param cmd_name: reporting name only.
        :param working_directory: a directory that can be None or \
        possiby overridden by emnvironment variable.

        :return count: count of files deleted.
        """

        self.list_empty_files(cmd_name, working_directory)

        working_directory = self.data['catalog']['working_directory']
        os.chdir(working_directory)
        empty_files = self.data['empty_files']

        if (len(empty_files) == 0):
            self.log.prog("%s no empty files detected." % (cmd_name, ))
            return 0

        for empty_file in empty_files:
            os.unlink(empty_file)

        self.cd_start_dir()

        self.log.prog("%s %s empty files deleted: %s" %
                      (cmd_name, len(empty_files), ' '.join(empty_files)))

        self.data['empty_files'] = []
        return len(empty_files)

    def remove_multiple_format_files(self, cmd_name, working_directory=None):
        """Remove files with multiple formats such as jpg and png
        using a working_directory as determined by the catalog library.
        When multiple formats are detected then the larger file is deleted.
        Given files 'a.jpg' and 'a.png' then delete the larger file.

        :param cmd_name: reporting name only.
        :param working_directory: a directory that can be None or \
        possiby overridden by emnvironment variable.

        :return count: count of files deleted.
        """

        self.catalog_init(cmd_name, working_directory, '/dev/null')
        self.catalog_set_directory_files()
        self.catalog_set_file_stats()
        catalog = self.data['catalog']['current']
        working_directory = self.data['catalog']['working_directory']

        work_files = self.data['catalog']['work_files']

        work_file_roots = [self.replace_file_ext(x, '') for x in work_files]

        multiple_count = Counter(work_file_roots)

        multiple_roots = [x for x in multiple_count if multiple_count[x] > 1]

        work_multiple_files = OrderedDict()

        os.chdir(working_directory)

        for work_file_root in multiple_roots:
            root_len = len(work_file_root)
            work_multiple_files[work_file_root] = \
                [(x, int(catalog[x]['size']))
                 for x in work_files if (x[:root_len] == work_file_root)]

            work_multiple_files[work_file_root].sort(key=lambda a: a[1],
                                                     reverse=True)
            self.log.debu("%s delete file => %s" %
                          (work_file_root,
                           work_multiple_files[work_file_root][0][0]))
            os.unlink(work_multiple_files[work_file_root][0][0])

        self.log.debu("%s found %s multiple format files.%s%s" %
                      (working_directory, len(multiple_roots), os.linesep,
                       work_multiple_files))

        return len(multiple_roots)

    def set_directory_files(self, cmd_name, working_directory=None,
                            catalog_file=None):
        """List directory files in the working_directory where
        working_directory is defined by the catalog library.
        Set list to self.data['catalog]['work_files']

        :param cmd_name: for display only.
        :param working_directory: any directory subject to default \
        if None or overridden by environment variable.

        :return count: count of files set in self.data['catalog]['work_files'].
        """

        self.catalog_init(cmd_name, working_directory, catalog_file)
        self.catalog_set_directory_files()
        working_directory = self.data['catalog']['working_directory']

        self.log.debu("%s start" % (cmd_name, ))
        self.log.debu("%s found %s total files." %
                      (working_directory, self.data['catalog']['file_count']))

        self.catalog_set_file_stats()

        return self.data['catalog']['file_count']
