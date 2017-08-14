from mongoengine import *


class Company(Document):
    """
    Document describing specific company in the database.
    Note: index field is for resource compatibility
    """
    name = StringField(required=True)
    index = IntField()


class Employee(Document):
    """
    Document describing specific employee in the database.
    Notes:
        # - it uses self reference to keep the list of friends
        - friends are referenced via list of indexes (easier solution, not perfect though)
        - index field is for resource compatibility
    """
    username = StringField(required=True)
    age = IntField()
    index = IntField()
    address = StringField()
    phone = StringField()
    friends = ListField(IntField())
    company = ReferenceField(Company)
    eye_color = StringField()
    has_died = BooleanField()
    fruits = ListField(StringField())
    vegetables = ListField(StringField())
