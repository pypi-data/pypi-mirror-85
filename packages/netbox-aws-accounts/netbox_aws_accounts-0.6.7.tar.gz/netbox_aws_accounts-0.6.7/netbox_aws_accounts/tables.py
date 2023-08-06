import django_tables2 as tables
from utilities.tables import BaseTable, ToggleColumn

from .models import awsAccounts, awsRegions, region, ParamEnv, ou

SOFTWARE_PROVIDER_ACTIONS = """
{% if perms.plugins.change_software_provider %}
    <a href="{% url 'plugins:netbox_aws_accounts:accounts_edit' pk=record.pk %}?return_url={{ request.path }}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

class ouTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = ou
        fields = (
            "name",
        )

class ParamEnvTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = ParamEnv
        fields = (
            "name",
        )

class regionTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = ParamEnv
        fields = (
            "name",
        )

class AccountsTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = awsAccounts
        fields = (
            "account_id",
            "ou",
            "ParamEnv",
            "isRegulated",
            "dome9enabled",
            "cloudability9enabled",
            "mainregion",
            "drregion"
        )

class RegionsTable(BaseTable):
    class Meta(BaseTable.Meta):
        model = awsRegions
        fields = (
            "account_id",
            "region",
            "ParamEnv",
            "n2ws",
            "custodian",
            "VPCCidr",
            "VPCPurpose",
        )