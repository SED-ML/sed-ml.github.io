""" Test the example SED-ML files

:Author: Jonathan Karr <karr@mssm.edu>
:Date: 2021-04-20
:Copyright: 2021, SED-ML Editors
:License: MIT
"""

from biosimulators_utils.combine.data_model import CombineArchiveContentFormat
from biosimulators_utils.combine.io import CombineArchiveReader
from biosimulators_utils.combine.validation import validate
from biosimulators_utils.omex_meta.data_model import OmexMetaSchema
from biosimulators_utils.simulator.exec import exec_sedml_docs_in_archive_with_containerized_simulator
from biosimulators_utils.utils.core import flatten_nested_list_of_strings
from biosimulators_utils.warnings import BioSimulatorsWarning
import glob
import json
import math
import os
import parameterized
import shutil
import tempfile
import unittest
import warnings


EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), '..', 'examples')
with open(os.path.join(EXAMPLES_DIR, 'simulator-compatibility.json'), 'r') as file:
    EXAMPLES = json.load(file)


CHECK_SIMULATION = os.getenv('CHECK_SIMULATION', '1').lower() in ['1', 'true']


class ExamplesTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dirname = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dirname)

    def test_simulator_compatibility_annotated(self):
        all_example_filenames = [os.path.relpath(filename, EXAMPLES_DIR)
                                 for filename in glob.glob(os.path.join(EXAMPLES_DIR, '**', '*.omex'), recursive=True)]
        example_filenames = [example['filename'] for example in EXAMPLES]
        missing_example_filenames = set(all_example_filenames).difference(set(example_filenames))
        if missing_example_filenames:
            raise ValueError('The following examples should be added to `examples/simulator-compatibility.json`:\n  {}'.format(
                '\n  '.join(sorted(missing_example_filenames))))

    @parameterized.parameterized.expand([(example['filename'], example,) for example in EXAMPLES])
    def test_example(self, name, example):
        example_name = example['filename']
        example_filename = os.path.join(EXAMPLES_DIR, example_name)

        # Validate archive
        self.validate_archive(example_filename)

        # Execute archive
        if CHECK_SIMULATION:
            simulation_checked = False
            for simulator in example['simulators']:
                if 'notImplemented' not in simulator and 'failure' not in simulator:
                    simulation_checked = True
                    temp_dirname = os.path.join(self.temp_dirname, example_name + '-output')
                    os.makedirs(temp_dirname)
                    exec_sedml_docs_in_archive_with_containerized_simulator(
                        example_filename, temp_dirname, 'ghcr.io/biosimulators/' + simulator['id'] + ':latest')

            if not simulation_checked:
                warnings.warn('No simulator is available to test its execution.')

    def validate_archive(self, filename):
        reader = CombineArchiveReader()
        name = os.path.relpath(filename, EXAMPLES_DIR)
        temp_dirname = os.path.join(self.temp_dirname, name)
        if not os.path.isdir(temp_dirname):
            os.makedirs(temp_dirname)
        archive = reader.run(filename, temp_dirname)

        error_msgs, warning_msgs = validate(
            archive, temp_dirname,
            formats_to_validate=list(CombineArchiveContentFormat.__members__.values()),
            metadata_schema=OmexMetaSchema.biosimulations,
        )

        if warning_msgs:
            msg = 'The COMBINE/OMEX archive may be invalid.\n  {}'.format(
                flatten_nested_list_of_strings(warning_msgs).replace('\n', '\n  '))
            warnings.warn(msg, BioSimulatorsWarning)

        if error_msgs:
            msg = 'The COMBINE/OMEX archive is not valid.\n  {}'.format(
                flatten_nested_list_of_strings(error_msgs).replace('\n', '\n  '))
            raise ValueError(msg)
