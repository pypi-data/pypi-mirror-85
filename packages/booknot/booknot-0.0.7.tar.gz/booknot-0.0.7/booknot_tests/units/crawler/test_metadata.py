import unittest
from datetime import datetime

from booknot.crawler.metadata import Metadata


class TestMetadata(unittest.TestCase):
    def setUp(self):
        pass

    def test_sanitize_dir_should_remove_uppercase_and_space(self):
        # Assign
        metadata = Metadata(url="", title="Yolo my title", description="", capture_date=datetime(2020, 1, 1))

        # Acts
        directory_name = metadata.sanitize_dir()

        # Assert
        self.assertEqual("20200101__yolo_my_title", directory_name)

    def test_sanitize_dir_should_remove_pipe(self):
        # Assign
        metadata = Metadata(url="", title="Yolo my | title", description="", capture_date=datetime(2020, 1, 1))

        # Acts
        directory_name = metadata.sanitize_dir()

        # Assert
        self.assertEqual("20200101__yolo_my___title", directory_name)

    def test_tomanifest_should_convert_date_to_iso_format(self):
        # Assign
        metadata = Metadata(url="", title="Yolo my | title", description="", capture_date=datetime(2020, 1, 1))

        # Acts
        manifest = metadata.tomanifest()

        # Assert
        self.assertEqual("2020-01-01T00:00:00", manifest['capture_date'])

    def test_tocapture_should_convert_date_to_readable_format(self):
        # Assign
        metadata = Metadata(url="", title="Yolo my | title", description="", capture_date=datetime(2020, 1, 1))

        # Acts
        manifest = metadata.tocapture()

        # Assert
        self.assertEqual("01/01/2020", manifest['capture_date'])

if __name__ == '__main__':
    unittest.main()
