"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from rest_framework.serializers import SerializerMethodField
from rest_framework_mongoengine.serializers import DocumentSerializer

from population.models import Company, Employee


class CompanySerializer(DocumentSerializer):
    employees = SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_employees(self, obj):
        query = Employee.objects.filter(company=obj)
        if query.count() == 0:
            return "This company has 0 employees."
        return EmployeePairSerializer(query, many=True).data


class EmployeeSerializer(DocumentSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeDetailSerializer(EmployeeSerializer):
    class Meta:
        model = Employee
        fields = ('username', 'age', 'vegetables', 'fruits')


class EmployeePairSerializer(EmployeeSerializer):
    class Meta:
        model = Employee
        fields = ('username', 'age', 'address', 'phone')
