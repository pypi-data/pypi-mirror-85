from django.db import migrations,models

class Migration(migrations.Migration):

    initial = True
    operations = [
        migrations.CreateModel(
            name='ou',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
            ]
        ),
        migrations.CreateModel(
            name='ParamEnv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
            ]
        ),
        migrations.CreateModel(
            name='region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=50)),
            ]
        ),
        migrations.CreateModel(
            name='awsAccounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('account_id', models.CharField(unique=True, max_length=50)),
                ('ou', models.ForeignKey(on_delete=models.deletion.CASCADE,to='ou')),
                ('ParamEnv', models.ForeignKey(on_delete=models.deletion.CASCADE,to='ParamEnv')),
                ('isRegulated', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('dome9enabled', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('cloudability9enabled',models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], max_length=5)),
                ('mainregion', models.CharField(max_length=10)),
                ('drregion', models.CharField(max_length=10)),
            ],
            options = {
                'ordering': ['account_id']
            }
        ),
        migrations.CreateModel(
            name='awsRegions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('account_id', models.ForeignKey(on_delete=models.deletion.CASCADE,to='awsAccounts')),
                ('region', models.ForeignKey(on_delete=models.deletion.CASCADE,to='region')),
                ('ParamEnv', models.ForeignKey(on_delete=models.deletion.CASCADE,to='ParamEnv')),
                ('n2ws', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=5)),
                ('VPCCidr', models.CharField(max_length=50)),
                ('custodian', models.CharField(max_length=50)),
            ],
            options = {
                'ordering': ['region']
            },
        ),
    ]