""" Test the example SED-ML files

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-04-20
:Copyright: 2021, SED-ML Editors
:License: MIT
"""

from biosimulators_utils.combine.io import CombineArchiveReader
from biosimulators_utils.combine.validation import validate
from biosimulators_utils.simulator.exec import exec_sedml_docs_in_archive_with_containerized_simulator
from biosimulators_utils.utils.core import flatten_nested_list_of_strings
import glob
import json
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
        all_example_filenames = [os.path.relpath(filename, self.EXAMPLES_DIR)
                                 for filename in glob.glob(os.path.join(self.EXAMPLES_DIR, '**', '*.omex'), recursive=True)]
        with open(os.path.join(self.EXAMPLES_DIR, 'simulator-compatibility.json'), 'r') as file:
            examples = json.load(file)

        example_filenames = [example['filename'] for example in examples]
        missing_example_filenames = set(all_example_filenames).difference(set(example_filenames))
        if missing_example_filenames:
            raise ValueError('The following examples should be added to `examples/simulator-compatibility.json`:\n  {}'.format(
                '\n  '.join(sorted(missing_example_filenames))))

        failed_examples = []
        warned_examples = []
        print('Validating {} examples ...'.format(len(examples)))
        for i_example, example in enumerate(examples):
            example_name = example['filename']
            print('  {} {} ...'.format(i_example + 1, example_name))
            example_filename = os.path.join(self.EXAMPLES_DIR, example_name)

            # Validate archive
            errors, warns = self.validate_archive(example_filename)
            if errors:
                failed_examples.append({"name": example_name, "messages": errors})
            if warns:
                warned_examples.append({"name": example_name, "messages": warns})

            # Execute archive
            simulation_checked = False
            for simulator in example['simulators']:
                if 'notImplemented' not in simulator and 'failure' not in simulator:
                    simulation_checked = True
                    temp_dirname = os.path.join(self.temp_dirname, example_name + '-output')
                    os.makedirs(temp_dirname)
                    try:
                        exec_sedml_docs_in_archive_with_containerized_simulator(
                            example_filename, temp_dirname, 'ghcr.io/biosimulators/' + simulator['id'] + ':latest')
                    except RuntimeError as exception:
                        failed_examples.append({"name": example_name, "messages": [[str(exception)]]})
                    shutil.rmtree(temp_dirname)

            if simulation_checked:
                warned_examples.append({"name": example_name, "messages": [['No simulator is available to test its execution.']]})

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
