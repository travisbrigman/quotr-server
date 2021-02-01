# Generated by Django 3.1.4 on 2020-12-10 15:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=55)),
                ('last_name', models.CharField(max_length=55)),
                ('organization', models.CharField(max_length=75)),
                ('email', models.EmailField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=55)),
                ('model', models.CharField(max_length=75)),
                ('cost', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(25500.0)])),
                ('margin', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.99)])),
                ('description', models.CharField(max_length=300)),
                ('image_url', models.CharField(max_length=256)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('export_date', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='proposals', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='proposals', to='quotrapi.customer')),
            ],
        ),
        migrations.CreateModel(
            name='QuotrUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image_url', models.CharField(max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProposalPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category', to='quotrapi.category')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package', to='quotrapi.package')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposal', to='quotrapi.proposal')),
            ],
        ),
        migrations.CreateModel(
            name='ProposalItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposalItem_category', to='quotrapi.category')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposalItem_item', to='quotrapi.item')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposItem_proposal', to='quotrapi.proposal')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemPackage_item', to='quotrapi.item')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemPackage_package', to='quotrapi.package')),
            ],
        ),
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessory_accessory', to='quotrapi.accessory')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accessory_item', to='quotrapi.item')),
            ],
        ),
    ]
