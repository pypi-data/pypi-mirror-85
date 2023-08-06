from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from django.contrib.auth.mixins import PermissionRequiredMixin
from utilities.views import BulkDeleteView, BulkImportView, ObjectEditView, ObjectListView

from .filters import (
    AccountsFilter,
    RegionsFilter
)
from .forms import (
    AccountsFilterForm,
    RegionsFilterForm
)
from .models import (
    awsAccounts,
    awsRegions,
)
from .tables import (
    AccountsTable,
    RegionsTable,
)

from .utilities.views import CRUDViewGenerator

accounts_generator = CRUDViewGenerator("awsAccounts")
AccountsListView = accounts_generator.list()
AccountsCreateView = accounts_generator.create()
AccountsBulkDeleteView = accounts_generator.bulk_delete()
AccountsEditView = accounts_generator.edit()

class AccountsListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'netbox_aws_accounts.view_accounts'
    queryset = awsAccounts.objects.all()
    filterset = AccountsFilter
    filterset_form = AccountsFilterForm
    table = AccountsTable
    template_name = "netbox_aws_accounts/accounts_list.html"

regions_generator = CRUDViewGenerator("awsRegions")
RegionsListView = regions_generator.list()
RegionsCreateView = regions_generator.create()
RegionsBulkDeleteView = regions_generator.bulk_delete()
RegionsEditView = regions_generator.edit()

class RegionsListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'netbox_aws_accounts.view_accounts'
    queryset = awsRegions.objects.all()
    filterset = RegionsFilter
    filterset_form = RegionsFilterForm
    table = RegionsTable
    template_name = "netbox_aws_accounts/regions_list.html"