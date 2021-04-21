""" Test the example SED-ML files

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-04-20
:Copyright: 2021, SED-ML Editors
:License: MIT
"""

from biosimulators_utils.combine.io import CombineArchiveReader
from biosimulators_utils.combine.validation import validate
from biosimulators_utils.utils.core import flatten_nested_list_of_strings
import glob
import math
import os
import shutil
import tempfile
import unittest
import warnings


class ExamplesTestCase(unittest.TestCase):
    EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')

    def setUp(self):
        self.temp_dirname = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dirname)

    def test(self):
        example_filenames = glob.glob(os.path.join(self.EXAMPLES_DIR, '**', '*.omex'), recursive=True)
        example_filenames.sort()

        failed_examples = []
        warned_examples = []
        print('Validating {} examples ...'.format(len(example_filenames)))
        for i_example, example_filename in enumerate(example_filenames):
            print('  {} {} ...'.format(i_example + 1, example_filename))

            errors, warns = self.validate_archive(example_filename)
            if errors:
                example_name = os.path.relpath(example_filename, self.EXAMPLES_DIR)
                failed_examples.append({"name": example_name, "messages": errors})
            if warns:
                example_name = os.path.relpath(example_filename, self.EXAMPLES_DIR)
                warned_examples.append({"name": example_name, "messages": warns})

        if warned_examples:
            msg = 'The following examples may be invalid:\n  {}\n\n  {}'.format(
                '\n  '.join(example['name'] for example in warned_examples),
                '\n\n  '.join('{} {} {}\n  {}'.format(
                    '=' * max(0, math.ceil((100 - len(example['name'])) / 2)),
                    example['name'],
                    '=' * max(0, math.ceil((100 - len(example['name'])) / 2)),
                    flatten_nested_list_of_strings(example['messages'])
                ) for example in warned_examples)
            )
            warnings.warn(msg, UserWarning)
        if failed_examples:
            msg = 'The following examples are invalid:\n  {}\n\n  {}'.format(
                '\n  '.join(example['name'] for example in failed_examples),
                '\n\n  '.join('{} {} {}\n  {}'.format(
                    '=' * max(0, math.ceil((100 - len(example['name'])) / 2)),
                    example['name'],
                    '=' * max(0, math.ceil((100 - len(example['name'])) / 2)),
                    flatten_nested_list_of_strings(example['messages'])
                ) for example in failed_examples)
            )
            raise Exception(msg)

    def validate_archive(self, filename):
        reader = CombineArchiveReader()
        name = os.path.relpath(filename, self.EXAMPLES_DIR)
        temp_dirname = os.path.join(self.temp_dirname, name)
        if not os.path.isdir(temp_dirname):
            os.makedirs(temp_dirname)
        try:
            archive = reader.run(filename, temp_dirname)
        except ValueError:
            return (reader.errors, reader.warnings)
        return validate(archive, temp_dirname)
