from mongoengine import *


class Company(Document):
    """
    Document describing specific company in the database
    """
    name = StringField(required=True)


class Employee(Document):
    """
    Document describing specific employee in the database.
    Note: It uses self reference to keep the list of friends.
    """
    username = StringField(required=True)
    age = IntField()
    address = StringField()
    phone = StringField()
    friends = ListField(ReferenceField('self'))
    company = ReferenceField(Company)
    eye_color = StringField()
    has_died = BooleanField()
    fruits = ListField(StringField())
    vegetables = ListField(StringField())
