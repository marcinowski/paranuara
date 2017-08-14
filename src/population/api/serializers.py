"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from rest_framework_mongoengine.serializers import EmbeddedDocumentSerializer, DocumentSerializer

from population.models import Company, Employee


class CompanySerializer(DocumentSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EmployeeSerializer(EmbeddedDocumentSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
