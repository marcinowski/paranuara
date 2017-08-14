"""
:created on: 2017-08-14

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

import json
import os
from unittest import TestCase

from population.data_source.fetcher import ResourceFetcher


class TestResourceFetcher(TestCase):
    test_file_path = os.path.join(ResourceFetcher.base_dir, 'test.json')

    def tearDown(self):
        if os.path.isfile(self.test_file_path):
            os.remove(self.test_file_path)
        super().tearDown()

    def test_filename_not_provided(self):
        """ This method tests if class raises ParsingError when `file` param is not present """
        class TestFetcher(ResourceFetcher):
            """"""

        with self.assertRaises(TestFetcher.ParsingError):
            TestFetcher._get_data_from_json()

    def test_error_handling(self):
        """ This method tests error handling for non existing files """
        class TestFetcher(ResourceFetcher):
            file = 'test.json'  # non existing file

        with self.assertRaises(TestFetcher.InvalidResourceError):
            TestFetcher._get_data_from_json()

    def test_wrong_json_file(self):
        """ This method tests error handling in case of badly formed resource file """
        class TestFetcher(ResourceFetcher):
            file = 'test.json'
        with open(self.test_file_path, 'w') as f:
            f.write('')
        with self.assertRaises(TestFetcher.InvalidResourceError):
            TestFetcher._get_data_from_json()

    def test_data_format(self):
        """ This method tests proper return data format """
        class TestFetcher(ResourceFetcher):
            file = 'test.json'

        data = {'test': 'test'}
        with open(self.test_file_path, 'w') as f:
            f.write(json.dumps(data))
        result = TestFetcher._get_data_from_json()
        self.assertIsInstance(result, list)
