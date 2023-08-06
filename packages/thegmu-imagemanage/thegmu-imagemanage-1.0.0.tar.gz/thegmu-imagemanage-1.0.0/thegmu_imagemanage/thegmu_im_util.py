#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    thegmu_im_util.py
    ~~~~~~~~~~~~~~~~~~~~

    Library of utilities such has creating the md5sum checksum for a file.

"""

from datetime import datetime
import hashlib
import pathlib
from _collections import OrderedDict

from thegmu_imagemanage import script


class TheGMUImageManageUtil():
    """Utilities such as creating md5sum checksums."""

    IDENTIFY_FORMATS_CMD = (
        r"""identify -list format | """
        r"""grep -E -e'^\s+[A-Z0-9]+\*?\s+[A-Z0-9]+\s' | """
        r"""sed -r 's/\s+/ /g' | sed -r 's/^\s//' | """
        r"""cut -d ' ' -f 1 | """
        r"""xargs""")

    IMAGEMAGICK_FORMATS = []

    CONVERSION_EXT = OrderedDict([('JPEG', 'jpg'),
                                  ('JPE', 'jpg'),
                                  ('unknown', 'none')])

    @staticmethod
    def get_file_ext(work_file):
        """Cananical file extension determination for this application.

        :param work_file: the file name

        :return extension: the file extension. 
        """
        work_ext = pathlib.PurePosixPath(work_file).suffix
        if ((len(work_ext) > 0) and (work_ext[0] == ".")):
            work_ext = work_ext[1:]
        return work_ext

    @classmethod
    def get_image_format_ext(cls, image_format):
        """Use the Imagemagick 'identify --list format' program
        to list image file formats.
        
        :param image_format: JPEG, PNG, or other Imagemagick format. 
        
        :return extension: the file extension associated with the format.
        """

        image_formats = cls.get_image_formats()

        if (image_format not in list(image_formats)):
            return cls.CONVERSION_EXT['unknown']

        if (image_format in list(cls.CONVERSION_EXT)):
            return cls.CONVERSION_EXT[image_format]

        return image_format.lower()

    @classmethod
    def get_image_formats(cls):
        """Use the Imagemagick 'identify --list format' program
        to list image file formats.
        
        :return formats: a list of Imagemagick formats. 
        """

        if (len(cls.IMAGEMAGICK_FORMATS) == 0):
            cmd = cls.IDENTIFY_FORMATS_CMD
            image_formats = script.runcmd(cmd, console=False,
                                          encoding='ascii',).strip()
            image_formats = image_formats.replace('*', '')
            image_formats = image_formats.split(' ')
            cls.IMAGEMAGICK_FORMATS = image_formats

        return cls.IMAGEMAGICK_FORMATS

    @staticmethod
    def get_list_csv_text(csv_list):
        """Converts a Python list into a thegmu_imagemange CSV text line.

        :param csv_list: a Python iterable to be cast as a list.

        :return csv_text: formated csv text from csv_list
        """
        csv_text = ','.join(str(x) for x in list(csv_list))
        return csv_text

    @staticmethod
    def get_md5sum(md5sum_file):
        """Python md5sum checksum for file similarity comparison.

        .. admonition:: Keep In Mind

            Files are slurped into main memory, although images shouldn't
            be more than a few megabytes.

        :param md5sum_file: any file that fits in memory.

        :return md5sum: string in hexidecimal format.
        """
        with open(md5sum_file, 'rb',) as md5sum_fh:
            return str(hashlib.md5(md5sum_fh.read()).hexdigest())

    @staticmethod
    def get_mtime_datetime(mtime):
        """Given the modified, mtime from a stat call return a canonical
        date used by this application.

        :param mtime: from a stat calle, st_mtime

        :return datetime: string YYYY-MM-DD-HH:MM:SS
        """

        work_date = str(datetime.fromtimestamp(int(mtime)))
        work_date = work_date.replace(" ", "-")
        return work_date

    @classmethod
    def replace_file_ext(cls, work_file, new_ext):
        """Replace the existing file extension with a new one.

        :param work_file: the file name to have extension replaced.

        :return new_work_file: the file extension replaced
        """
        work_ext = cls.get_file_ext(work_file)
        new_work_file = work_file[:work_file.rfind(work_ext)]
        new_work_file += new_ext
        return new_work_file

    @classmethod
    def replace_file_ext_by_format(cls, work_file, image_format):
        """Replace the existing file extension with a new one using
        a passed in image format.

        :param work_file: the file name to have extension replaced.

        :return new_work_file: the file extension replaced
        """
        new_ext = cls.get_image_format_ext(image_format)
        work_ext = cls.get_file_ext(work_file)
        new_work_file = work_file[:work_file.rfind(work_ext)]
        new_work_file += new_ext
        return new_work_file
