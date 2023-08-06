from django.db import migrations,models

class Migration(migrations.Migration):

    dependencies = [
        ('netbox_aws_accounts', '001_base_initial')
    ]

    operations = [
        migrations.AddField(
            'awsRegions', 'VPCPurpose', models.CharField(null=True,max_length=50)),

]