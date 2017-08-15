"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from rest_framework.serializers import SerializerMethodField
from rest_framework_mongoengine.serializers import DocumentSerializer

from population.models import Company, Employee


class CompanySerializer(DocumentSerializer):
    """
    General Company Serializer.
    Note: includes all employees that work for the company.
    """
    employees = SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_employees(self, obj):
        """
        Method handling `employees` field in serialized data.
        :param obj: Company instance
        :return: List of all employees that work for company
        :rtype: list
        """
        query = Employee.objects.filter(company=obj)
        if query.count() == 0:
            return "This company has 0 employees."
        return EmployeePairSerializer(query, many=True).data


class EmployeeSerializer(DocumentSerializer):
    """
    General Employee serializer including all fields.
    """
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeDetailSerializer(EmployeeSerializer):
    """
    Serializer for `api/employee/<index>` detail endpoint.
    """
    class Meta:
        model = Employee
        fields = ('username', 'age', 'vegetables', 'fruits')


class EmployeePairSerializer(EmployeeSerializer):
    """
    Serializer for `api/employee/pair/` endpoint.
    """
    class Meta:
        model = Employee
        fields = ('username', 'age', 'address', 'phone')
