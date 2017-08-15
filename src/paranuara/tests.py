"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from django.test.runner import DiscoverRunner
from django.test import TestCase


class NoSQLTestRunner(DiscoverRunner):
    """ https://staltz.com/djangoconfi-mongoengine/#/18 """
    def setup_databases(self):
        pass

    def teardown_databases(self, *args):
        pass


class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass

    def _fixture_teardown(self):
        pass
