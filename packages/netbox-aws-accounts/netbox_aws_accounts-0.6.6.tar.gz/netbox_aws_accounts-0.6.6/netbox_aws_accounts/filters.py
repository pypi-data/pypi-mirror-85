import django_filters
from django.db.models import Q

from dcim.models import Site

from utilities.filters import (
    BaseFilterSet,
    MultiValueCharFilter,
    MultiValueMACAddressFilter,
    MultiValueNumberFilter,
    NameSlugSearchFilterSet,
    TagFilter,
    TreeNodeMultipleChoiceFilter,
)

from extras.filters import CustomFieldFilterSet, LocalConfigContextFilterSet, CreatedUpdatedFilterSet

from .models import awsAccounts, awsRegions

class AccountsFilter(BaseFilterSet):
    q = django_filters.CharFilter(method="search", label="Search")

    class Meta:
        model = awsAccounts
        fields = ["id", "account_id"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(name__icontains=value)
            | Q(full_name__icontains=value)
        )
        return queryset.filter(qs_filter)


class RegionsFilter(BaseFilterSet):
    q = django_filters.CharFilter(method="search", label="Search")

    class Meta:
        model = awsRegions
        fields = ["id", "region"]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(id__icontains=value)
            | Q(name__icontains=value)
        )
        return queryset.filter(qs_filter)

