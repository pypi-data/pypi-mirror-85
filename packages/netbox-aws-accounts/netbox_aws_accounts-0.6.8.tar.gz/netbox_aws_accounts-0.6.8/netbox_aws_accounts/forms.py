from django import forms
from django_rq import get_queue

from .models import (
    awsAccounts,
    awsRegions,
)
from mptt.forms import TreeNodeChoiceField

from utilities.forms import (
    APISelectMultiple,
    APISelect,
    DynamicModelMultipleChoiceField,
    DynamicModelChoiceField,
    StaticSelect2Multiple,
    BootstrapMixin,
    DatePicker
)

from dcim.models import Site

class AccountsFilterForm(BootstrapMixin, forms.ModelForm):

    q = forms.CharField(required=False, label="Search")

    class Meta:
        model = awsAccounts
        fields = [
            "q",
        ]

class RegionsFilterForm(BootstrapMixin, forms.ModelForm):
    q = forms.CharField(required=False, label="Search")

    class Meta:
        model = awsRegions
        fields = [
            "q",
        ]