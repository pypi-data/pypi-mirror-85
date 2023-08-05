"""Unit tests for knilb.parser module.

"""
import unittest
import sys
import os
import uuid
# Python 2 and Python 3 compatible
try:
    import unittest.mock as mock
except ImportError:
    import mock

from knilb import parser


class TestParseArgs(unittest.TestCase):

    def setUp(self):
        # let's pretend cli is "$ python knilb http://localhost:5000 1234567890"
        self.cli = {'cloud': 'http://localhost:5000', 'passkey': '1234567890'}

    def tearDown(self):
        pass

    def test_parse_args_positional_arguments_and_default_optional(self):
        # mock sys.argv to include script name as sys.argv[0]
        # $ knilb http://cloud 1234
        test_sys_argv = [__package__, self.cli['cloud'], self.cli['passkey']]
        with mock.patch.object(sys, 'argv', test_sys_argv):
            result = parser.parse_args()
            self.assertEqual(result.cloud, self.cli['cloud'])
            self.assertEqual(result.passkey, self.cli['passkey'])
            self.assertEqual(result.uuid, str(uuid.getnode()))
            self.assertFalse(result.register)
            self.assertFalse(result.verbose)
            self.assertFalse(result.step)
            self.assertEqual(result.mock.name, os.devnull)

    def test_parse_args_missing_positional_arguments(self):
        test_sys_argv = [__package__]
        # mock sys.argv as if user did not include any positional args
        with mock.patch.object(sys, 'argv', test_sys_argv):
            # mock to stop print error msg - make testing pretty
            with mock.patch('sys.stderr', open(os.devnull, 'w')):
                self.assertRaises(SystemExit, parser.parse_args)

    def test_parse_args_optional_arg_uuid(self):
        uuid = '12345abcdef'
        test_sys_argv = [__package__, self.cli['cloud'], self.cli['passkey'],
                        '-u', uuid]
        # mock sys.argv as if user did not include any positional args
        with mock.patch.object(sys, 'argv', test_sys_argv):
            result = parser.parse_args()
            self.assertEqual(result.uuid, uuid)
    
    def test_parse_args_optional_arg_set_true_verbose_and_true_step(self):
        test_sys_argv = [__package__, self.cli['cloud'], self.cli['passkey'],
                         '-v', '-s']
        # mock sys.argv as if user did not include any positional args
        with mock.patch.object(sys, 'argv', test_sys_argv):
            result = parser.parse_args()
            self.assertTrue(result.verbose)
            self.assertTrue(result.step)

    def test_parse_args_optional_file_default_mock_ini(self):
        # Exampe command 'knilb http://cloud 1234 -m' <-- m flag without file
        filename = 'mock.ini'  # default filename hardcoded in application
        test_sys_argv = [__package__, self.cli['cloud'], self.cli['passkey'],
                         '-m']
        with mock.patch.object(sys, 'argv', test_sys_argv):
            result = parser.parse_args()
            self.assertEqual(os.path.basename(result.mock.name), filename)

        
    def test_parse_args_optional_file_exists(self):
        # Example command 'knilb http://cloud 1234' <-- no m flag
        filename = 'test_mock.ini'
        abspath_filename = os.path.join(os.path.abspath(__package__), filename)
        test_sys_argv = [__package__, self.cli['cloud'], self.cli['passkey'],
                         '-m', abspath_filename]
        with mock.patch.object(sys, 'argv', test_sys_argv):
            result = parser.parse_args()
            self.assertEqual(os.path.basename(result.mock.name), filename)

    def test_parse_args_optional_file_does_not_exist(self):
        # Example command 'knilb http://cloud 1234 -m fake.ini' <-- bad file
        filename = 'this_file_does_not_exist.ini'
        abspath_filename = os.path.join(os.path.abspath(__package__), filename)
        test_sys_argv = [__package__, self.cli['cloud'], self.cli['passkey'],
                         '-m', abspath_filename]
        with mock.patch.object(sys, 'argv', test_sys_argv):
            # mock to stop print error msg - make testing pretty
            with mock.patch('sys.stderr', open(os.devnull, 'w')):
                self.assertRaises(SystemExit, parser.parse_args)            
            
