"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from .fetcher import CompaniesFetcher, PeopleFetcher
from .mappings import COMPANY_MAPPING, PEOPLE_MAPPING
from population.models import Company, Employee


class ResourceParser(object):
    """
    Base class for parsing resources fetched data.
    """
    fetcher = None
    model = None
    mapping = None
    status_msg = 'Created - {c}, updated - {up}, errors - {err}.'

    class ParsingError(Exception):
        """ Main exception class for parsing """

    @classmethod
    def parse(cls):
        """
        Main parsing method following the workflow:
            - fetch data with cls.fetcher
            - clean data with cls.mapping
            - additional processing
            - save data using cls.model
            - return status
        """
        data = cls.fetcher.fetch()
        created, updated, errors = 0, 0, 0  # fixme: this is super weak, but holds for now
        for obj in data:
            try:
                obj_t = cls._parse_single_object(obj)
                obj_p = cls._additional_processing(obj_t)
                c, u, e = cls._save_object(obj_p)
            except cls.ParsingError:
                c, u, e = 0, 0, 1
            created += c
            updated += u
            errors += e
        return cls.status_msg.format(c=created, up=updated, err=errors)

    @classmethod
    def _parse_single_object(cls, obj):
        """
        Cleans the object and translates keys if necessary.
        :param obj: single dict to be translated
        :return: translated dictionary
        :rtype: dict
        """
        result = {}
        for key, value in obj.items():
            if key in cls.model._fields:
                result[key] = value
            elif key in cls.mapping:
                key_t = cls.mapping[key]
                result[key_t] = value
        return result

    @classmethod
    def _additional_processing(cls, obj):
        """ Override this method if some additional obj parsing is needed """
        return obj

    @classmethod
    def _save_object(cls, obj):
        """ Saves object including status of the operation. """
        try:
            index = obj.get('index', None)
            cls.model.objects.get(index=index)
        except cls.model.DoesNotExist:
            cls.model.objects.create(**obj).save()
            return 1, 0, 0
        except cls.model.MultipleObjectsReturned:
            return 0, 0, 1
        else:
            cls.model.objects.update(**obj)
            return 0, 1, 0


class CompanyParser(ResourceParser):
    fetcher = CompaniesFetcher
    model = Company
    mapping = COMPANY_MAPPING


class PeopleParser(ResourceParser):
    fetcher = PeopleFetcher
    model = Employee
    mapping = PEOPLE_MAPPING
    vegetables = ['beetroot', 'cucumber', 'carrot', 'celery']  # this should be handled better, fine for now
    fruits = ['banana', 'strawberry', 'apple', 'orange']

    @classmethod
    def _additional_processing(cls, obj):
        """ Additional processing for people resource """
        obj['company'] = cls._handle_company(obj.get('company', -1))
        obj['fruits'], obj['vegetables'] = cls._handle_food(obj.pop('food', []))
        obj['friends'] = cls._handle_friends(obj.get('friends', []), obj.get('index', -1))
        return obj

    @classmethod
    def _handle_food(cls, food):
        """ Split food between fruits and vegies """
        fruits, vegetables = [], []
        for i in food:
            if i in cls.fruits:
                fruits.append(i)
            elif i in cls.vegetables:
                vegetables.append(i)
        return fruits, vegetables

    @classmethod
    def _handle_company(cls, index):
        """ Fetches company from db and returns Company instance """
        try:
            return Company.objects.get(index=index)
        except (Company.DoesNotExist, Company.MultipleObjectsReturned):  # what would I like to do here?
            raise cls.ParsingError("Company with index {} not found!".format(index))

    @staticmethod
    def _handle_friends(friends, self_index):
        """ [{'index': 1}, {'index': 2}] -> [1, 2] """
        return [p['index'] for p in friends if p['index'] != self_index]
