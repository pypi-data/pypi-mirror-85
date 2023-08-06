#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    thegmu_im_convert.py
    ~~~~~~~~~~~~~~~~~~~~

    Library that converts images between formats such as PNG and JPEG
    using the Imagemagick convert library.


"""

import os

from wand.image import Image

from thegmu_imagemanage.thegmu_im_errors import \
    TheGMUImageManageConvertError


class TheGMUImageManageConvert():
    """Use ImageMagick 'convert' to change formats from PNG to JPEG, etc.
    """

    def convert_list_formats(self, _cmd_name=None):
        """Print to console the possible Imagemagick formats available for 
        conversion.
        
        :param cmd_name: display only.
        
        """

        self.init_image_formats()

        self.log.prog("Imagemagick valid image formats for conversion:%s%s" %
                      (os.linesep, ' '.join(self.image_formats)))

    # pylint: disable=too-many-arguments
    def convert_format_simple(self, cmd_name, format_from, format_to,
                              working_directory=None,
                              catalog_file=None, ):
        """Convert all images in the working_directory using
        one parameter conversion routine that relies on Imagemagick
        default quality and memory usage policies set in the
        Imagematick policy /etc/imagemagick/policy.xml

        Leaves the original file in place.

        :param cmd_name: display only logging name.
        :param format_from: any valid Imagemagick format.
        :param format_to: any valid Imagemagick format.
        :param working_directory: directory with images to convert.
        :param catalog_file: the text file to store image information.

        :data catalog: self.data['catalog']['current']
        
        :return count: count of files converted. 
        """

        self.init_image_formats()

        if (format_to not in self.image_formats):
            msg = "%s: convert %s unrecognized converstion format: %s" % \
                (cmd_name, format_to, format_to)
            raise TheGMUImageManageConvertError(msg)

        if (format_from not in self.image_formats):
            msg = "%s convert %s unrecognized converstion format: %s" % \
                (cmd_name, format_from, format_from)
            raise TheGMUImageManageConvertError(msg)

        if (('catalog' not in self.data) or
                ('current' not in self.data['catalog'])):
            self.catalog('convert_format_simple', working_directory,
                         catalog_file)

        catalog = self.data['catalog']['current']
        working_directory = self.data['catalog']['working_directory']
        self.data['catalog']['converted_files'] = []

        count = 0

        os.chdir(working_directory)
        for work_file in catalog:

            work_image = catalog[work_file]

            if (work_image['format'] != format_from):
                continue

            new_work_file = self.replace_file_ext_by_format(work_file,
                                                            format_to)

            if ((work_file != new_work_file) and
                    os.path.isfile(new_work_file)):
                self.log.prog("%s %s => %s, convert file exists, skipping." %
                              (cmd_name, work_file, new_work_file))
                continue

            count += 1
            self.log.prog(
                "%s %s converting from %s to %s as %s" %
                (cmd_name, work_file, work_image['format'], format_to, new_work_file))

            with Image(filename=work_file) as work_img:
                work_img.save(filename="%s:%s" % (format_to, new_work_file))

            if (work_file != new_work_file):
                self.data['catalog']['converted_files'].append(work_file)

        self.log.prog("%s %s files converted from %s -> %s." %
                      (cmd_name, count, format_from, format_to))

        self.cd_start_dir()

        return count

    # pylint: disable=too-many-arguments
    def convert(self, cmd_name, format_from, format_to,
                working_directory=None,
                catalog_file=None, ):
        """Convert all images of one format in the working_directory using
        one parameter conversion routine that relies on Imagemagick
        default quality and memory usage policies set in the
        Imagematick policy /etc/imagemagick/policy.xml

        Deletes the original file.

        :param cmd_name: display only logging name.
        :param format_from: any valid Imagemagick format.
        :param format_to: any valid Imagemagick format.
        :param working_directory: directory with images to convert.
        :param catalog_file: the text file to store image information.

        :data catalog: self.data['catalog']['current']
        
        :return count: count of files converted.
        """

        count = self.convert_format_simple(cmd_name, format_from, format_to,
                                           working_directory, catalog_file)

        if (len(self.data['catalog']['converted_files']) > 0):
            for work_file in self.data['catalog']['converted_files']:
                self.log.prog("%s: %s deleting converted file." %
                              (cmd_name, work_file))
                os.unlink(work_file)

        return count
