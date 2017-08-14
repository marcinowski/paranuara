"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from unittest import TestCase

from population.data_source.parser import PeopleParser


class TestResourceParser(TestCase):
    single_object = {
        'test': 'Unwanted info',
        'name': 'Should be translated',
        'phone': 'Should stay'
    }

    def test_parse_single_object(self):
        result = PeopleParser._parse_single_object(self.single_object)
        expected_keys = ['username', 'phone']
        self.assertListEqual(list(result.keys()), expected_keys)
