from rest_framework.viewsets import ModelViewSet
from netbox_aws_accounts.models import *
from .serializers import *
from netbox_aws_accounts.filters import *
from netbox_aws_accounts.utilities.views import CRUDViewGenerator

AccountsViewSet = CRUDViewGenerator("awsAccounts").view_set()
RegionsViewSet = CRUDViewGenerator("awsRegions").view_set()

class AccountsViewSet(ModelViewSet):
    queryset = awsAccounts.objects.all()
    serializer_class = AccountsSerializer

