"""
:created on: 2017-08-14

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
from django.core.management import BaseCommand

from population.data_source.parser import CompanyParser, PeopleParser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """
        Main method for triggering database population.
        :return: None
        """
        self.stdout.write('Populating database.')
        self.stdout.write('Populating companies.')
        status = CompanyParser.parse()
        self.stdout.write(status)
        self.stdout.write('Populating employees.')
        status = PeopleParser.parse()
        self.stdout.write(status)
        self.stdout.write('Database populated successfully!')
