"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from .fetcher import CompaniesFetcher, PeopleFetcher
from .mappings import COMPANY_MAPPING, PEOPLE_MAPPING
from population.models import Company, Employee


class ResourceParser(object):
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
        created, updated, errors = 0, 0, 0
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
        return obj

    @classmethod
    def _save_object(cls, obj):
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
    vegetables = ['beetroot']  # this should be handled better, fine for now
    fruits = ['apples']

    @classmethod
    def _additional_processing(cls, obj):
        obj['company'] = cls._handle_company(obj.get('company'))
        obj['fruits'], obj['vegetables'] = cls._handle_food(obj.pop('food'))
        obj['friends'] = cls._handle_friends(obj['friends'])
        return obj

    @classmethod
    def _handle_food(cls, food):
        fruits, vegetables = [], []
        for i in food:
            if i in cls.fruits:
                fruits.append(i)
            elif i in cls.vegetables:
                vegetables.append(i)
        return fruits, vegetables

    @staticmethod
    def _handle_company(index):
        try:
            return Company.objects.get(index=index)
        except (Company.DoesNotExist, Company.MultipleObjectsReturned):  # what would I like to do here?
            raise PeopleParser.ParsingError("Company with index {} not found!".format(index))

    @staticmethod
    def _handle_friends(friends):
        return [p['index'] for p in friends]
