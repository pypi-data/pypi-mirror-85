import io
import os
import unittest
from unittest.mock import Mock

from booknot.crawler.http_crawler import HttpCrawler
from booknot_tests.fixtures import clone_fixture


class TestHttpCrawler(unittest.TestCase):
    def setUp(self):
        self.session_mock = Mock()
        self._tested = HttpCrawler(self.session_mock)

    def test_fetch_should_parse_og_description(self):
        with clone_fixture("webpages") as directory:
            with io.open(os.path.join(directory, 'classic.html')) as filep:
                content = filep.read()

            # Assign
            request = Mock()
            request.content = content
            self.session_mock.get = Mock(return_value=request)

            # Acts
            result = self._tested.fetch("http://mock")

            # Assert
            self.assertEqual('Avant 10 JVMs, maintenant 300 microservices avec des runtimes transients. Le nombre de service à assembler pour construire nos applications augmente.Le SI se...', result.description)

    def test_fetch_should_parse_old_description(self):
        with clone_fixture("webpages") as directory:
            with io.open(os.path.join(directory, 'legacy.html')) as filep:
                content = filep.read()

            # Assign
            request = Mock()
            request.content = content
            self.session_mock.get = Mock(return_value=request)

            # Acts
            result = self._tested.fetch("http://mock")

            # Assert
            self.assertEqual('Avant 10 JVMs, maintenant 300 microservices avec des runtimes transients. Le nombre de service à assembler pour construire nos applications augmente.Le SI se...', result.description)

if __name__ == '__main__':
    unittest.main()
