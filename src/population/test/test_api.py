"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from django.shortcuts import reverse
from paranuara.tests import NoSQLTestCase


class TestAPIEndpoints(NoSQLTestCase):
    """ Class for testing 200 on list endpoints """
    def test_companies_list(self):
        url = reverse('api:company-list')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

    def test_employees_list(self):
        url = reverse('api:employee-list')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
