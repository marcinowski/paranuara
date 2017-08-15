"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from django.shortcuts import reverse
from rest_framework.decorators import list_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ReadOnlyModelViewSet

from population.api.serializers import CompanySerializer, EmployeeSerializer, EmployeeDetailSerializer,\
    EmployeePairSerializer
from population.models import Company, Employee


class CompanyViewSet(ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'name'

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint to return details about the company including all employees that work for the company.
        From specification:
            Given a company, the API needs to return all their employees.
            Provide the appropriate solution if the company does not have any employees.\
        """
        return super().retrieve(request, *args, **kwargs)


class EmployeeViewSet(ReadOnlyModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'username'
    pagination_class = PageNumberPagination

    class BadPairEndpointRequest(Exception):
        """"""

    def retrieve(self, request, *args, **kwargs):
        """
        We override this method just to limit the fields in the output in the detail view by switching the serializer.
        From the specification:
            Given 1 people, provide a list of fruits and vegetables they like.
            This endpoint must respect this interface for the output:
             {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}
        """
        self.serializer_class = EmployeeDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    @list_route()
    def pair(self, request):
        """
        This endpoint provides data about two employees based on their names.
        From specification:
            Given 2 people, provide their information (Name, Age, Address, phone)
            and the list of their friends in common which have brown eyes and are still alive.
        """
        try:
            selected_employees = self._get_pair_of_employees(request)
        except self.BadPairEndpointRequest as e:
            return Response(str(e), 400)
        selected_employees_data = EmployeePairSerializer(selected_employees, many=True).data
        friends_list = selected_employees.values_list('friends')
        common_friends_ids = [i for i in friends_list[0] if i in friends_list[1]]  # list intersection fixme: a bit ugly
        friends_query = Employee.objects.filter(index__in=common_friends_ids)
        friends_query = friends_query.filter(has_died=False).filter(eye_color="brown")
        data = {
            'selected_employees': selected_employees_data,
            'common_friends_count': friends_query.count(),
            'common_friends': self.get_serializer(friends_query, many=True).data
        }
        return Response(data)

    def _get_pair_of_employees(self, request):
        """
        Private method returning two employees given by `?ids=id1,id2` in request.
        :param request:
        :return: query
        :rtype: QuerySet
        :raises: self.BadPairEndpointRequest
        """
        ids = request.GET.get('ids', None)
        if not ids:
            raise self.BadPairEndpointRequest("Please provide two ids in form of `?ids=id1,id2`.")
        ids = list(map(int, ids.strip().split(',')))
        if len(ids) != 2:
            raise self.BadPairEndpointRequest("Please provide two ids in form of `?ids=id1,id2`.")  # fixme: dry
        selected_employees = Employee.objects.filter(index__in=ids)
        if selected_employees.count() != 2:
            url = reverse('api:employee-list')
            raise self.BadPairEndpointRequest(
                "Provided ids are not valid! You can check existing employees here: {}".format(url),
            )
        return selected_employees
