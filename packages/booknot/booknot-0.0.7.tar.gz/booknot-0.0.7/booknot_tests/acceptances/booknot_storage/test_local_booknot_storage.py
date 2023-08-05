import os
import unittest

from booknot.booknot_storage.local_booknot_storage import LocalBooknotStorage
from booknot_tests.fixtures import clone_fixture


class TestLocalBooknotStorage(unittest.TestCase):
    def setUp(self):
        pass

    def test_init_should_create_dot_booknote_directory(self):
        # Assign
        with clone_fixture('empty_directory') as directory:
            booknot_storage = LocalBooknotStorage(directory)

            # Acts
            booknot_storage.init_store()

            self.assertTrue(os.path.isdir(os.path.join(directory, '.booknot')))

    def test_init_should_populate_dot_booknote_directory(self):
        # Assign
        with clone_fixture('empty_directory') as directory:
            booknot_storage = LocalBooknotStorage(directory)

            # Acts
            booknot_storage.init_store()

            self.assertTrue(os.path.isdir(os.path.join(directory, '.booknot')))
            self.assertTrue(os.path.isfile(os.path.join(directory, '.booknot', 'index.rst.j2')))

    def test_is_sphinx_present_should_check_conf_py_is_present_in_parent(self):
        # Assign
        with clone_fixture('sphinx') as directory:
            working_dir = os.path.join(directory, 'reading_notes')
            booknot_storage = LocalBooknotStorage(working_dir)

            # Acts
            is_present = booknot_storage.is_sphinx_present()

            self.assertTrue(is_present)

    def test_is_sphinx_present_should_return_false_when_sphinx_is_not_present(self):
        # Assign
        with clone_fixture('empty_directory') as directory:
            working_dir = os.path.join(directory)
            booknot_storage = LocalBooknotStorage(working_dir)

            # Acts
            is_present = booknot_storage.is_sphinx_present()

            self.assertFalse(is_present)

if __name__ == '__main__':
    unittest.main()
