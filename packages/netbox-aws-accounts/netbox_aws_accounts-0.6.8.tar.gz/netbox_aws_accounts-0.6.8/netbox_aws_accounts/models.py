from django.db import models
from django.urls import reverse

class ou(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Organizational Unit'

    def __str__(self):
        return str(self.name)

class region(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Region'

    def __str__(self):
        return str(self.name)


class ParamEnv(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'ParamEnv'

    def __str__(self):
        return str(self.name)

class awsRegions(models.Model):
    account_id = models.ForeignKey(verbose_name="Account Id", on_delete=models.deletion.CASCADE,to='awsAccounts')
    region = models.ForeignKey(verbose_name="Region",on_delete=models.deletion.CASCADE,to='region')
    ParamEnv = models.ForeignKey(verbose_name="Environment",on_delete=models.deletion.CASCADE,to='ParamEnv')
    n2ws = models.CharField(verbose_name="N2WS ?",max_length=50)
    custodian = models.CharField(verbose_name="Custodian ?",max_length=50)
    VPCCidr = models.CharField(verbose_name="VPC CIDR",max_length=50)
    VPCPurpose = models.CharField(verbose_name="VPC Purpose",max_length=50)
    class Meta:
        verbose_name = "Regions"
        verbose_name_plural = 'Regions'
        ordering = [ 'region' ]

class awsAccounts(models.Model):
    account_id = models.CharField("Account Id",unique=True, max_length=50)
    ou = models.ForeignKey(verbose_name="Organizational Unit",on_delete=models.deletion.CASCADE,to='ou')
    ParamEnv = models.ForeignKey(verbose_name="Environment",on_delete=models.deletion.CASCADE,to='ParamEnv')
    isRegulated = models.CharField(verbose_name="Has Regulated Data ?",max_length=50)
    dome9enabled = models.CharField(verbose_name="DOME9 Enabled ?",max_length=50)
    cloudability9enabled = models.CharField(verbose_name="Cloudability ?",max_length=50)
    mainregion = models.CharField(verbose_name="Main Region",max_length=50)
    drregion = models.CharField(verbose_name="DR Region",max_length=50)

    class Meta:
        verbose_name_plural = 'Accounts'
        ordering = [ 'account_id' ]

    def __str__(self):
        return str(self.account_id)
