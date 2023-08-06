#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    thegmu_im_catalog.py
    ~~~~~~~~~~~~~~~~~~~~

    Library that creates a flat file database of all image files in a
    directory.

    #. Create a catalog for grouping by size, dimensions, format,
    creation date, etc. for manual management.

"""

import csv
import os
import filetype
from _collections import OrderedDict

from wand.image import Image
from wand.exceptions import WandRuntimeError, CacheError

from thegmu_imagemanage.thegmu_im_errors import \
    TheGMUImageManageCatalogError


class TheGMUImageManageCatalog():
    """Use /usr/bin/stat and ImageMagick indentity to
    create the catalog data.
    """

    CATALOG_FILE_DEFAULT = 'thegmu_imagemanage.catalog.txt'

    CATALOG_RECORD = OrderedDict([('file_name', None),
                                  ('format', None),
                                  ('WxH', None),
                                  ('size', None),
                                  ('date', None),
                                  ('epoch', None),
                                  ('md5sum', None),
                                  ('ext', None)])

    def _catalog_build(self):
        """After all the data has been collected from stat and
        ImageMagick then build the catalog suitable for output
        to the catalog file.

        Requirements
        1. Filter out files that are not images.
        2. The catalog file contains the catalog name information in
           comma seperated version:
        file name, FORMAT, WxH, sizeinbytes, YYYYMMDD-HHMMSS, epoch, MD5SUM, EXT

        """

        catalog = self.data['catalog']['current']
        work_types = self.data['catalog']['work_types']

        self.data['catalog']['skipped'] = OrderedDict()

        os.chdir(self.data['catalog']['working_directory'])

        count = 0
        itype = "image/"

        for work_file in work_types:

            if (work_file not in catalog):
                raise TheGMUImageManageCatalogError("%s catalog file not found"
                                                    % (work_file, ))

            # Filter out non images
            if (not self._catalog_validate_file(work_types, itype, work_file)):
                continue

            count += 1

            if (catalog[work_file]['md5sum'] is None):

                work_md5sum = self.get_md5sum(work_file)

                try:

                    with Image(filename=work_file) as work_img:

                        catalog[work_file]['format'] = work_img.format
                        catalog[work_file]['WxH'] = "%sx%s" % \
                            (work_img.width, work_img.height)
                        catalog[work_file]['md5sum'] = work_md5sum

                        # self.log.debu("%s => %s" % (work_file, image_record))

                except WandRuntimeError as wand_error:
                    self.log.debu("%s => wand error %s, skipping. " %
                                  (work_file, wand_error))
                    self.data['catalog']['skipped'][work_file] = \
                        'imagemagick runtime error'
                    continue
                except CacheError as wand_error:
                    self.log.debu("%s => wand error %s, skipping. " %
                                  (work_file, wand_error))
                    self.data['catalog']['skipped'][work_file] = \
                        "iamgemagick cache error"
                    continue

            if ((self.test_count is not None) and
                    (count >= self.test_count)):
                break

        self.cd_start_dir()

    def _catalog_emit(self):
        """Write the catalog file from previously seeded stat and
        imagemagick data."""

        catalog_file = self.data['catalog']['catalog_file']
        work_images = self.data['catalog']['current']

        self.log.prog("start")
        with open(catalog_file, 'w') as catalog_fh:
            work_header = self.get_list_csv_text(
                list(self.CATALOG_RECORD.keys()))
            catalog_fh.write(work_header + os.linesep)

            for work_file in work_images:
                work_record = work_images[work_file]
                emit_record = self.get_list_csv_text(
                    list(work_record.values()))
                catalog_fh.write(emit_record + os.linesep)

        self.log.prog("done")

    @staticmethod
    def _catalog_get_working_dir(working_directory):
        """Environment variable THGMU_IMAGEMANAGE_TEST_DIR
           working_directory passed in
           $PWD if working_direction is None.
        """

        actual_working_directory = os.getenv("THEGMU_IMAGEMANAGE_TEST_DIR",
                                             working_directory)

        if (actual_working_directory is None):
            actual_working_directory = os.getcwd()

        return actual_working_directory

    @classmethod
    def _catalog_get_catalog_file(cls, catalog_file):
        """Environment variable THGMU_IMAGEMANAGE_TEST_CATALOG_FILE
           catalog_file passed in
           self.CATALOG_FILE_DEFAULT if None.
        """

        actual_file = os.getenv("THEGMU_IMAGEMANAGE_TEST_CATALOG_FILE",
                                catalog_file)

        if (actual_file is None):
            actual_file = cls.CATALOG_FILE_DEFAULT

        return actual_file

    def _catalog_validate_file(self, work_types, itype, work_file):
        """Is the work_file a valid image file that belongs in the catalog?"""

        catalog = self.data['catalog']['current']
        itypelen = len(itype)

        if ((work_types[work_file][:itypelen] != itype) and
                (work_file.find('thegmu_imagemanage') > -1)):
            if (work_file in catalog):
                del(catalog[work_file])
            return False

        if (work_file.find(',') > -1):
            self.log.debu(
                "%s => comma found in file name, skipping file." %
                (work_file,))
            self.data['catalog']['skipped'][work_file] = 'comma name'
            if (work_file in catalog):
                del(catalog[work_file])
            return False

        if (catalog[work_file]['size'] == 0):
            self.log.debu("%s => 0 bytes, skipping, empty file." %
                          (work_file,))
            self.data['catalog']['skipped'][work_file] = "empty"
            if (work_file in catalog):
                del(catalog[work_file])
            return False

        if (work_types[work_file][:itypelen] != itype):
            self.log.debu("%s => %s,  skipping, not an image." %
                          (work_file, work_types[work_file]))
            self.data['catalog']['skipped'][work_file] = "unknown file type"
            if (work_file in catalog):
                del(catalog[work_file])
            return False

        return True

    def _catalog_log_skip(self):
        """Log to a file a listing of all the files skipped as well as
        the reason."""

        catalog_file = self.data['catalog']['catalog_file']
        log_file = "%s.skip.log" % catalog_file

        try:
            with open(log_file, 'w') as log_fh:
                for work_file in self.data['catalog']['skipped']:
                    log_line = "%s,%s" % (
                        work_file, self.data['catalog']['skipped'][work_file])
                    self.log.debu(log_line)
                    log_fh.write(log_line + os.linesep)
        except PermissionError:
            self.log.prog("%s permission defined, skipping log file" %
                          (log_file))
        else:
            self.log.prog("%s skip log file created." % (log_file, ))

    def catalog(self, cmd_name, working_directory=None, catalog_file=None):
        """Given a line of text containing the command to catalog
        then create a catalog file. Repeated calls update the
        catalog of file changes in the directory of request. The catalog
        file is never updated once created so the file is recreated each time
        with 100% of all data.

        :param cmd_name: 'catalog'.
        :param working_directory: directory with images to catalog.
        :param catalog_file: file to list all the image information.

        """

        self.catalog_init(cmd_name, working_directory, catalog_file)

        working_directory = self.data['catalog']['working_directory']

        self.log.prog("catalog start")
        self.log.prog("%s found %s total files." %
                      (working_directory, self.data['catalog']['file_count']))

        self.catalog_set_directory_files()
        self.catalog_set_file_stats()
        self.catalog_load()
        self.catalog_update()
        self.catalog_set_filetype()

        self._catalog_build()

        self._catalog_emit()
        self._catalog_log_skip()

        self.log.prog("catalog processed %s image files." %
                      (len(self.data['catalog']['current']), ))
        self.log.prog("catalog skipped %s non-image files." %
                      (len(self.data['catalog']['skipped']), ))
        self.log.prog("catalog end")

    def catalog_excel(
            self,
            cmd_name,
            working_directory=None,
            catalog_file=None):
        """Invokes catalog and then creates an excel file.
        
        :param cmd_name: display and logging only.
        :param working_directory: any directory subject to override by\
        the catalog.
        :param catalog_file: the text catalog file for the images. 
        """
        self.catalog(cmd_name, working_directory, catalog_file)

        self._catalog_emit_excel()

    def catalog_init(self, cmd_name, working_directory, catalog_file):
        """Initialize and validate paramaters passed to catalog
        as well as load an previous catalog file found.

        :param cmd_name: display purposes only for logging.
        :working_directory: image directory.
        :catalog_file: the catalog file for the iamges.
        """

        self.data['catalog'] = dict()

        self.log.debu("%s passed working_directory: %s" %
                      (cmd_name, working_directory, ))
        self.log.debu("%s passed catalog_file %s" % (cmd_name, catalog_file, ))

        working_directory = self._catalog_get_working_dir(working_directory)
        catalog_file = self._catalog_get_catalog_file(catalog_file)

        self.log.debu("%s actual working_directory: %s" %
                      (cmd_name, working_directory, ))
        self.log.debu("%s actual catalog_file %s" % (cmd_name, catalog_file, ))

        self.data['catalog']['working_directory'] = working_directory

        if (not os.path.isdir(working_directory)):
            msg = "%s image directory not found." % working_directory
            raise TheGMUImageManageCatalogError(msg)

        catalog_dir = os.path.dirname(catalog_file)
        if ((catalog_dir != "") and (not os.path.isdir(catalog_dir))):
            msg = "%s catalog directory not found." % catalog_dir
            raise TheGMUImageManageCatalogError(msg)

        self.data['catalog']['catalog_file'] = os.path.abspath(catalog_file)

        self.data['catalog']['file_count'] = \
            len([x for x in os.listdir(working_directory)
                 if os.path.isfile(os.path.join(working_directory, x))])

        self.catalog_load()

    def catalog_load(self):
        """Load an exist catalog file."""
        catalog_file = self.data['catalog']['catalog_file']
        working_directory = self.data['catalog']['working_directory']

        os.chdir(working_directory)
        if (os.path.isfile(catalog_file)):
            self.data['catalog']['prev'] = OrderedDict()
            with (open(catalog_file, 'r')) as catalog_fh:
                reader = csv.DictReader(catalog_fh)
                for row in reader:
                    row['size'] = int(row['size'])
                    row['epoch'] = int(row['epoch'])
                    self.data['catalog']['prev'][row['file_name']] = row

            self.log.prog("%s images read from pervious catalog." %
                          (len(self.data['catalog']['prev'])))
        self.cd_start_dir()

    def catalog_set_filetype(self,):
        """Add the image file mime type data per file,"""

        if ('current' not in self.data['catalog']):
            msg = "Programming error, files need to be collected"
            " before ImageMagick data is collected."
            raise TheGMUImageManageCatalogError(msg)

        working_directory = self.data['catalog']['working_directory']

        self.log.debu("working_directory: %s" % (working_directory, ))
        self.log.debu("cwd: %s" % (os.getcwd(), ))
        os.chdir(working_directory)

        work_types = dict((x, filetype.guess(x))
                          for x in self.data['catalog']['work_files'])

        work_types = dict(map((lambda a: (a, "unknown")
                               if work_types[a] is None
                               else (a, "%s" % work_types[a].mime)),
                              work_types))

        self.data['catalog']['work_types'] = work_types

        self.cd_start_dir()

    def catalog_set_directory_files(self):
        """List the working_directory for files and create
        the image record. Not all files will be be images and
        these non-image files will be pruned later"""

        working_directory = self.data['catalog']['working_directory']

        os.chdir(working_directory)
        work_files = sorted([x for x in os.listdir() if os.path.isfile(x)])
        self.cd_start_dir()

        self.data['catalog']['work_files'] = work_files
        self.data['catalog']['current'] = OrderedDict()

        for work_file in work_files:
            image_record = OrderedDict(self.CATALOG_RECORD)
            image_record['file_name'] = work_file
            self.data['catalog']['current'][work_file] = image_record

    def catalog_set_file_stats(self):
        """Update the file record by adding os.stat data per file."""

        working_directory = self.data['catalog']['working_directory']

        os.chdir(working_directory)

        for work_file in self.data['catalog']['work_files']:

            statinfo = os.stat(work_file, follow_symlinks=False)
            record = self.data['catalog']['current'][work_file]
            record['size'] = statinfo.st_size
            record['epoch'] = int(statinfo.st_mtime)
            record['date'] = self.get_mtime_datetime(record['epoch'])
            work_ext = self.get_file_ext(work_file)
            if ((len(work_ext) > 0) and (work_ext[0] == ".")):
                work_ext = work_ext[1:]
            record['ext'] = work_ext

        self.cd_start_dir()

    def catalog_update(self):
        """Remove previous catalog files that no longer exist or
        or have more recent dates and then populate the
        catalog with image date from the previous catalog for
        those files that have the same date.
        """
        catalog_file = self.data['catalog']['catalog_file']
        if (not os.path.isfile(catalog_file)):
            return

        if (('current' not in self.data['catalog']) or
                ('prev' not in self.data['catalog'])):
            msg = "Programming error, previous and existing files must be "
            "populated prior to calling catalog_update."
            raise TheGMUImageManageCatalogError(msg)

        work_files = self.data['catalog']['work_files']

        update_count = 0
        delete_files = set()
        for work_file in self.data['catalog']['prev']:
            if (work_file not in work_files):
                self.log.prog("%s deleted from previous catalog run." %
                              (work_file))
                delete_files.add(work_file)

            elif(self.data['catalog']['prev'][work_file]['epoch'] !=
                 self.data['catalog']['current'][work_file]['epoch']):
                self.log.prog("%s modified from previous catalog run." %
                              (work_file))
                delete_files.add(work_file)
            else:
                self.data['catalog']['current'][work_file] = \
                    self.data['catalog']['prev'][work_file]
                update_count += 1

        for work_file in delete_files:
            del(self.data['catalog']['prev'][work_file])

        self.log.prog("%s images cataloged from previous run." %
                      (update_count, ))
