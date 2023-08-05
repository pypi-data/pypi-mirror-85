from unittest import TestCase

import os
import tempfile
import logging

from hetrob.run import run_experiment_module


class TestRun(TestCase):

    def test_mock_run(self):
        import hetrob.examples.experiment_template as config

        temp_folder = tempfile.TemporaryDirectory()
        config.PATH = os.path.join(temp_folder.name, 'experiment')

        # This is important, because the run function produces a whole lot of console output, which we do not want to
        # have in the unittest summary.
        logging.disable(logging.CRITICAL)

        run_experiment_module(config)

        self.assertTrue(os.path.exists(config.PATH))

        statistics_path = os.path.join(config.PATH, 'stats.json')
        self.assertTrue(os.path.exists(statistics_path))

        log_path = os.path.join(config.PATH, 'output.log')
        self.assertTrue(os.path.exists(log_path))

        # As we are not using the temp folder as a context manager, we need to remember to close it properly at the end
        # end.
        temp_folder.cleanup()
