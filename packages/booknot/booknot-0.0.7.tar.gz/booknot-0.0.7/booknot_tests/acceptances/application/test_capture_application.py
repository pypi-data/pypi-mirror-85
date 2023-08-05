import os
import unittest
from datetime import datetime
from unittest.mock import Mock

from booknot.application.capture_application import CaptureApplication
from booknot.crawler.metadata import Metadata
from booknot_tests.fixtures import clone_fixture


class TestCatpureApplication(unittest.TestCase):
    def setUp(self):
        self.crawler_mock = Mock()
        self._tested = CaptureApplication(self.crawler_mock, '', 'http://any')

    def test_run_should_create_a_directory_for_the_note(self):
        with clone_fixture('empty_booknot') as directory:
            # Assign
            self._tested.directory = directory
            self.crawler_mock.fetch = Mock(return_value=Metadata(url="", title="my title", description="", capture_date=datetime(2020, 1, 1)))

            # Acts
            result = self._tested.run()

            # Assert
            note_directory = os.path.join(directory, '20200101__my_title')

            self.assertTrue(os.path.isdir(note_directory), f'note directory does not exists in {note_directory}')

    def test_run_should_create_the_manifest_of_the_note(self):
        with clone_fixture('empty_booknot') as directory:
            # Assign
            self._tested.directory = directory
            self.crawler_mock.fetch = Mock(return_value=Metadata(url="", title="my title", description="", capture_date=datetime(2020, 1, 1)))

            # Acts
            result = self._tested.run()

            # Assert
            note_manifest = os.path.join(directory, '20200101__my_title', 'manifest.json')

            self.assertTrue(os.path.isfile(note_manifest), f'note manifest does not exists in {note_manifest}')

    def test_run_should_create_the_index_of_the_note(self):
        with clone_fixture('empty_booknot') as directory:
            # Assign
            self._tested.directory = directory
            self.crawler_mock.fetch = Mock(return_value=Metadata(url="", title="my title", description="", capture_date=datetime(2020, 1, 1)))

            # Acts
            result = self._tested.run()

            # Assert
            note_index = os.path.join(directory, '20200101__my_title', 'index.rst')

            self.assertTrue(os.path.isfile(note_index), f'note manifest does not exists in {note_index}')

if __name__ == '__main__':
    unittest.main()
