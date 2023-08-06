from rest_framework.serializers import ModelSerializer
from netbox_aws_accounts.models import awsAccounts, awsRegions


class RegionsSerializer(ModelSerializer):
    class Meta:
        model = awsRegions
        fields = ('id', 'account_id', 'region', 'ParamEnv', 'n2ws', 'VPCCidr', 'custodian')

class AccountsSerializer(ModelSerializer):
    class Meta:
        model = awsAccounts
        fields = ('id', 'account_id', 'ou', 'ParamEnv', 'isRegulated', 'dome9enabled', 'cloudability9enabled', 'mainregion', 'drregion')
