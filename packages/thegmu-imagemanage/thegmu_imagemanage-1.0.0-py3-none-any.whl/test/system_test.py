# -*- coding: utf-8 -*-
"""system_test: end-to-end tests."""

import datetime
import glob
import os
import shutil
import unittest

import thegmu_imagemanage
import thegmu_imagemanage.thegmu_im as imagemanage

from thegmu_imagemanage.thegmu_im import TheGMUImageManage
from thegmu_imagemanage import script
from thegmu_imagemanage.thegmu_im_errors import \
    TheGMUImageManageError


class TheGMUImageManageSystemTest(unittest.TestCase):
    """SystemTest: end-to-end tests."""

    TEST_DIR = os.path.abspath(os.path.dirname(thegmu_imagemanage.__file__))
    TEST_DIR = os.path.realpath(os.path.join(TEST_DIR, "../test"))
    TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')

    def setUp(self):
        os.chdir(self.TEST_DIR)
        self.test_image_dir = 'run'
        if (os.path.isdir(self.test_image_dir)):
            shutil.rmtree(self.test_image_dir)
        shutil.copytree('data/commands', self.test_image_dir)

        # Set count to a small number to limit files being processed
        self.test_count = None
        self.test_count = 6

    def tearDown(self):
        pass

    def test01_noop(self):
        """Invoke main with no options"""
        print("")
        script.print_dashes("test01_noop")
        script.begin()

        self.assertRaises(TypeError, imagemanage.main)

        noop_list = []

        print("Test missing default commands file by passing no command line options")
        self.assertRaises(SystemExit, imagemanage.main, noop_list)

        print("Usage message when passing '-h'")
        self.assertRaises(SystemExit, imagemanage.main, ['-h', ])
        script.end()
        script.print_dashes("test01_noop")

    def test02_catalog(self):
        """Catalog a directory of files."""
        print("")
        script.print_dashes("test02_catalog")
        script.begin()

        gim = TheGMUImageManage()

        gim.log.set_level_from_string("DEBUG")

        test02_bad_file = 'test02_one_bad_command.commands.txt'
        test02_bad_file = os.path.join(self.test_image_dir,
                                       test02_bad_file)

        test02_command_file = 'test02_catalog.commands.txt'
        test02_command_file = os.path.join(self.test_image_dir,
                                           test02_command_file)

        print("test02_bad_file: %s" % (test02_bad_file, ))
        self.assertTrue(os.path.isfile(test02_bad_file),
                        "Test data file not found.")
        bad_args = [test02_bad_file, ]

        gim.init_args(bad_args)
        gim.init_commands_from_command_file()
        print("")
        print("test02_catalog Testing a bad command raises and exception.")
        self.assertRaises(TheGMUImageManageError, gim.run_commands)

        print("")
        print(
            "test02_catalog Testing catalog command: %s" %
            (test02_command_file, ))
        self.assertTrue(os.path.isfile(test02_command_file),
                        "Test data file not found.")

        catalog_args = [test02_command_file, ]

        gim.init_args(catalog_args)
        gim.init_commands_from_command_file()
        gim.test_count = self.test_count
        gim.run_commands()
        script.end()
        script.print_dashes("test02_catalog")

    def test03_empty_files(self):
        """Test listing and removing empty files."""
        print("")
        script.print_dashes("test03_empty_files")
        script.begin()

        src_dir = 'data/empty_files'
        tgt_dir = self.test_image_dir
        expected_num_empty_files = 4
        shutil.copytree(src_dir, tgt_dir, dirs_exist_ok=True)

        gim = TheGMUImageManage()

        gim.log.set_level_from_string("DEBUG")

        test03_commands = os.path.join(self.test_image_dir, 'no.commands.txt')

        test03_argv = [test03_commands, ]

        gim.init_args(test03_argv)

        num_empty = gim.list_empty_files('test03', tgt_dir)

        self.assertEqual(num_empty, expected_num_empty_files,
                         "Four empty files expected.")

        num_deleted = gim.remove_empty_files('test03', tgt_dir)

        self.assertEqual(num_deleted, expected_num_empty_files,
                         "Four empty files expected.")

        script.end()
        script.print_dashes("test03_empty_files")

    def test04_duplicate_files(self):
        """Test listing and removing duplicate files using
        md5sum checksums."""

        print("")
        script.print_dashes("test04_duplicate_files")
        script.begin()

        src_dir = 'data/duplicate_files'
        tgt_dir = self.test_image_dir
        expected_num_duplicate_files = 1
        shutil.copytree(src_dir, tgt_dir, dirs_exist_ok=True)

        gim = TheGMUImageManage()

        gim.log.set_level_from_string("DEBUG")

        test04_commands = os.path.join(tgt_dir, 'no.commands.txt')

        test04_argv = [test04_commands]

        gim.init_args(test04_argv)

        num_duplicate = gim.set_duplicate_files('test04', tgt_dir)

        self.assertEqual(num_duplicate, expected_num_duplicate_files,
                         "One duplciate file expected.")

        num_deleted = gim.remove_duplicate_files('test04', tgt_dir)

        self.assertEqual(num_deleted, expected_num_duplicate_files,
                         "One duplicate file expected.")

        script.end()
        script.print_dashes("test04_duplicate_files")

    def test05_convert(self):
        """Test TheGMUImageManageConvert object."""

        print("")
        script.print_dashes("test5_convert")
        script.begin()

        src_dir = 'data/conversion_files'
        tgt_dir = self.test_image_dir
        shutil.copytree(src_dir, tgt_dir, dirs_exist_ok=True)

        gim = TheGMUImageManage()
        gim.log.set_level_from_string("DEBUG")

        cmd = gim.IDENTIFY_FORMATS_CMD
        print(cmd)

        gim.convert_list_formats()
        image_formats = gim.get_image_formats()
        print("Imagemagick formats: ", image_formats)
        print("Format lower case is file extension except for CONVERSION_EXT:",
              list(gim.CONVERSION_EXT))
        self.assertTrue('JPEG' in image_formats)

        test05_commands = os.path.join(tgt_dir, 'no.commands.txt')

        test05_argv = [test05_commands, ]

        gim.init_args(test05_argv)

        self.assertEqual('jpg', gim.get_file_ext("foo.jpg"))
        self.assertEqual('jpg', gim.get_image_format_ext('JPG'))
        self.assertEqual('jpg', gim.get_image_format_ext('JPEG'))
        self.assertEqual('jpg', gim.get_image_format_ext('JPE'))
        self.assertEqual('png', gim.get_image_format_ext('PNG'))
        self.assertEqual('webp', gim.get_image_format_ext('WEBP'))

        expected_converted = 1

        num_converted = gim.convert_format_simple(
            'test05_convert', 'PNG', 'JPEG', self.test_image_dir,
            '/dev/null')

        self.assertEqual(num_converted, expected_converted)

        script.end()
        script.print_dashes("test05_convert")

    # @unittest.skip("commened out")
    def test06_remove_multiple_format(self):
        """Test TheGMUImageManageOS remove files with multiple formats."""

        print("")
        test_name = "test06_remove_multiple_format_files"
        script.print_dashes(test_name)
        script.begin()

        src_dir = 'data/multiple_format_files'
        tgt_dir = self.test_image_dir
        shutil.copytree(src_dir, tgt_dir, dirs_exist_ok=True)

        gim = TheGMUImageManage()
        gim.log.set_level_from_string("DEBUG")

        test06_commands = os.path.join(tgt_dir, 'no.commands.txt')

        test06_argv = [test06_commands, ]

        gim.init_args(test06_argv)

        expected_converted = 1

        num_files = gim.remove_multiple_format_files(test_name,
                                                     self.test_image_dir)

        self.assertEqual(expected_converted, num_files)

        script.end()
        script.print_dashes(test_name)

    def test07_jpeg_optimize_size(self):
        """Test TheGMUImageManageOS jpeg optimize size method."""

        print("")
        test_name = "test07_jpeg_optimeize_size"
        script.print_dashes(test_name)
        print("TODAY: %s" % (datetime.date.today()))
        script.begin()

        src_dir = 'data/jpeg_optimize_size_files'
        tgt_dir = self.test_image_dir
        shutil.copytree(src_dir, tgt_dir, dirs_exist_ok=True)

        gim = TheGMUImageManage()
        gim.log.set_level_from_string("DEBUG")

        test07_commands = os.path.join(tgt_dir, 'no.commands.txt')
        test07_catalog_file = os.path.join(tgt_dir, 'test07_catalog.txt')

        test07_argv = [test07_commands, ]

        gim.init_args(test07_argv)

        expected_converted = 1

        test_size = 10

        num_files = gim.jpeg_optimize_size(test_name, test_size,
                                           self.test_image_dir,
                                           test07_catalog_file)

        self.assertEqual(expected_converted, num_files)

        script.end()
        script.print_dashes(test_name)

    def test08_catalog_excel(self):
        """Test TheGMUImageManageCatalog Excel file creation."""

        print("")
        test_name = "test08_catalog_excel"
        script.print_dashes(test_name)
        script.begin()

        src_dir = 'data/duplicate_files'
        tgt_dir = self.test_image_dir
        shutil.copytree(src_dir, tgt_dir, dirs_exist_ok=True)

        test08_commands = os.path.join(tgt_dir, 'test08_catalog.commands.txt')

        test08_argv = ['-v', test08_commands, ]

        imagemanage.main(test08_argv)

        script.end()
        script.print_dashes(test_name)

    def test09_flatten_file_names(self):
        """Test flattening file name puncutation to underscore."""

        print("")
        test_name = "test09_flatten_file_names"
        script.print_dashes(test_name)
        script.begin()

        src_dir = 'data/flatten_files'
        tgt_dir = self.test_image_dir
        shutil.copytree(src_dir, tgt_dir, dirs_exist_ok=True)

        test09_commands = os.path.join(tgt_dir, 'test09_flatten.commands.txt')

        test09_argv = ['-v', test09_commands, ]

        expected_files = ['empty01__.txt', 'empty02__.txt', 'empty03__.txt',
                          'empty04_.txt', 'empty04___.txt']

        imagemanage.main(test09_argv)

        result_files = glob.glob(os.path.join(self.test_image_dir, "empty*"))
        result_files = sorted([x.split('/')[-1]
                               for x in result_files])

        print("%s expected_files: %s" % (test_name, expected_files, ))
        print("%s   result_files: %s" % (test_name, result_files, ))
        self.assertEqual(expected_files, result_files)

        script.end()
        script.print_dashes(test_name)

    def test10_excel_file_delete(self):
        """Test deleting image files marked for deletion in and excel file."""

        print("")
        test_name = "test10_excel_file_delete"
        script.print_dashes(test_name)
        script.begin()

        src_dirs = ['data/conversion_files', 'data/excel_delete']
        tgt_dir = self.test_image_dir

        for src_dir in src_dirs:
            shutil.copytree(src_dir, tgt_dir, dirs_exist_ok=True)

        test10_commands = os.path.join(tgt_dir,
                                       'test10_excel_file.commands.txt')

        test10_argv = ['-v', test10_commands, ]
        imagemanage.main(test10_argv)

        test_excel_glob = "test10_excel_file_delete.catalog.*.xlsx"
        result_files = glob.glob(os.path.join(self.test_image_dir,
                                              test_excel_glob))

        self.assertEqual(len(result_files), 2)
        test_excel_file = "test10_excel_file_delete.catalog.sample.xlsx"

        gim = TheGMUImageManage()

        gim.init_args(test10_argv)

        gim.log.set_level_from_string("DEBUG")

        test10_catalog = '%s.catalog.txt' % test_name
        test_delete_file = os.path.join(
            self.test_image_dir, 'trees_green1.png')

        self.assertTrue(os.path.exists(test_delete_file))
        expected_num_deleted = 1

        gim.excel_file_commands(test_name, test_excel_file,
                                working_directory=self.test_image_dir,
                                catalog_file=test10_catalog)

        num_deleted = gim.data[test_excel_file]['delete_count']
        self.assertEqual(num_deleted, expected_num_deleted)

        self.assertFalse(os.path.exists(test_delete_file))

        script.end()
        script.print_dashes(test_name)
