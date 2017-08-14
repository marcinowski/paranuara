"""
:created on: 2017-08-14

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""
import json
import os

from django.conf import settings


RESOURCE_DIRECTORY = os.path.join(os.path.dirname(settings.BASE_DIR), 'resources')
assert os.path.isdir(RESOURCE_DIRECTORY)


class ResourceFetcher(object):
    """
    Base class for parsers. Overriding prefix parameter enables to parse different files with different workflow.
    """
    base_dir = RESOURCE_DIRECTORY
    file = None

    class ParsingError(Exception):
        """ Custom exception for data parsing. """

    class InvalidResourceError(ParsingError):
        """ Custom exception for reading the resource file """

    @classmethod
    def fetch(cls):
        """
        Main method for parser. Doesn't require class to be initiated.
        Note: "private" method cls._get_data_from_json is provided -> python list of dicts.
        """
        raise NotImplemented

    @classmethod
    def _get_data_from_json(cls):
        """
        Reads json from provided path defined in parser class property.
        :return: python object read from json
        :rtype: list
        :raises: cls.ParsingError, cls.InvalidResourceError
        """
        try:
            path = os.path.join(cls.base_dir, cls.file)
        except TypeError:
            raise cls.ParsingError('Class doesn\'t provide the `file` property!')
        try:
            with open(path, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            raise cls.InvalidResourceError(
                'Resourece file in {} does not exist. Make sure you\'ve provided a proper path to resource file.'
                    .format(path)
            )
        try:
            data = json.loads(content)
        except (TypeError, ValueError):
            raise cls.InvalidResourceError(
                'Resource file in path {} corrupted, doesn\'t contain a valid json'
                    .format(path)
            )
        if not isinstance(data, list):  # this assures return type - list
            data = [data]
        return data


class CompaniesFetcher(ResourceFetcher):
    file = 'companies.json'

    @classmethod
    def fetch(cls):
        return cls._get_data_from_json()


class PeopleFetcher(ResourceFetcher):
    file = 'people.json'

    @classmethod
    def fetch(cls):
        return cls._get_data_from_json()
