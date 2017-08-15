"""
:created on: 2017-08-15

:author: Marcin Muszynski
:contact: marcinowski007@gmail.com
"""

from django_filters.rest_framework import DjangoFilterBackend


class FilterBackend(DjangoFilterBackend):
    def get_filter_class(self, view, queryset=None):
        return None

    def filter_queryset(self, request, queryset, view):
        """ Let's assume that all fields are filterable. This works only for strings and numbers tbf. """
        queries = {q: v for q, v in request.GET.items() if q in queryset._document._fields}
        queryset = queryset.filter(**queries)
        return queryset
