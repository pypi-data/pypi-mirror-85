#!/usr/bin/env python
#
# Copyright 2007 The Closure Linter Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Full regression-type (Medium) tests for gjslint.

Tests every error that can be thrown by gjslint.  Based heavily on
devtools/javascript/gpylint/full_test.py
"""
__author__ = ('robbyw@google.com (Robert Walker)',
              'ajp@google.com (Andy Perelson)')

import os
import sys
import unittest

import gflags as flags
import unittest as googletest

from closure_linter import errors
from closure_linter import runner
from closure_linter.common import filetestcase

_RESOURCE_PREFIX = 'closure_linter/testdata'


class GJsLintTestSuite(unittest.TestSuite):
  """Test suite to run a GJsLintTest for each of several files.

  If sys.argv[1:] is non-empty, it is interpreted as a list of filenames in
  testdata to test. Otherwise, _TEST_FILES is used.

  The tests are executed with flags from filetestcase.AnnotatedFileTestCase
  """

  def __init__(self, tests=()):
    unittest.TestSuite.__init__(self, tests)


    if sys.argv[0] == 'setup.py':
      argv = sys.argv[2:]
    else:
      argv = sys.argv[1:]

    flags.FLAGS(['test'] + argv)

    if argv:
      test_files = argv
    else:
      test_files = os.listdir(os.path.join(
        os.path.dirname(runner.__file__),
        'testdata',
        ))
      excepted = [
        'bugs.js',  # Not implemented - known bugs.
        'not_strict.js',  # Don't know what to expect for non-strict.
        'file_level_comment.js',  # Not implemented.
        ]
      test_files = [t for t in test_files if t not in excepted]

    for test_file in test_files:
      resource_path = os.path.join(_RESOURCE_PREFIX, test_file)
      self.addTest(
          filetestcase.AnnotatedFileTestCase(
              resource_path,
              runner.Run,
              errors.ByName))


if __name__ == '__main__':
  # Don't let main parse args; it happens in the TestSuite.
  googletest.main(argv=sys.argv[0:1], defaultTest='GJsLintTestSuite')
