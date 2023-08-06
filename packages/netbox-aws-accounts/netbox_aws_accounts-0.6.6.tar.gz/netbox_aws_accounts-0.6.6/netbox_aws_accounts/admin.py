from django.contrib import admin
from .models import ou, ParamEnv, region, awsAccounts, awsRegions
from django import forms
from ipam.models import Aggregate, Prefix
@admin.register(ou)
class ouAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )

@admin.register(ParamEnv)
class ParamEnvAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        )

@admin.register(region)
class regionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

class accountForm(forms.ModelForm):
    CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    isRegulated = forms.ChoiceField(choices=CHOICES)
    dome9enabled = forms.ChoiceField(choices=CHOICES)
    cloudability9enabled = forms.ChoiceField(choices=CHOICES)
    mainregion = forms.ModelChoiceField(queryset=region.objects.all())
    drregion = forms.ModelChoiceField(queryset=region.objects.all())

@admin.register(awsAccounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = (
        'account_id',
        'ou',
        'ParamEnv',
        'isRegulated',
        'dome9enabled',
        'cloudability9enabled',
        'mainregion',
        'drregion',
        )
    fields = (
        'account_id',
        'ou',
        'ParamEnv',
        'isRegulated',
        'dome9enabled',
        'cloudability9enabled',
        'mainregion',
        'drregion',
        )
    form = accountForm

class regionForm(forms.ModelForm):
    CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    n2ws = forms.ChoiceField(choices=CHOICES)
    VPCCidr = forms.ModelChoiceField(queryset=Prefix.objects.filter(status="reserved",tenant__name="mtf"))

@admin.register(awsRegions)
class RegionsAdmin(admin.ModelAdmin):
    list_display = (
        'account_id',
        'region',
        'ParamEnv',
        'n2ws',
        'custodian',
        'VPCCidr',
        'VPCPurpose',
    )
    fields = (
        'account_id',
        'region',
        'ParamEnv',
        'n2ws',
        'VPCCidr',
        'custodian',
    )
    form = regionForm


