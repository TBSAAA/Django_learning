# Generated by Django 3.2.12 on 2022-11-09 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.SmallIntegerField(choices=[(1, 'active'), (0, 'delete')], default=1, verbose_name='state')),
                ('username', models.CharField(db_index=True, max_length=32, verbose_name='user_name')),
                ('password', models.CharField(max_length=64, verbose_name='password')),
                ('mobile', models.CharField(db_index=True, max_length=11, verbose_name='phone_number')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='create_date')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.SmallIntegerField(choices=[(1, 'active'), (0, 'delete')], default=1, verbose_name='state')),
                ('username', models.CharField(db_index=True, max_length=32, verbose_name='user_name')),
                ('password', models.CharField(max_length=64, verbose_name='password')),
                ('mobile', models.CharField(db_index=True, max_length=11, verbose_name='phone_number')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='balance')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='create_date')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.administrator', verbose_name='creator')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.SmallIntegerField(choices=[(1, 'active'), (0, 'delete')], default=1, verbose_name='state')),
                ('title', models.CharField(max_length=32, verbose_name='title')),
                ('percent', models.IntegerField(verbose_name='discount')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PricePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='count')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.SmallIntegerField(choices=[(1, 'active'), (0, 'delete')], default=1, verbose_name='state')),
                ('charge_type', models.SmallIntegerField(choices=[(1, 'Top up'), (2, 'Debit'), (3, 'Create Order'), (4, 'Delete order'), (5, 'Cancel')], verbose_name='charge_type')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='amount')),
                ('order_oid', models.CharField(blank=True, db_index=True, max_length=64, null=True, verbose_name='order_id')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='create_datetime')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.administrator', verbose_name='creator')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.customer', verbose_name='customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.SmallIntegerField(choices=[(1, 'active'), (0, 'delete')], default=1, verbose_name='state')),
                ('status', models.SmallIntegerField(choices=[(1, 'pending'), (2, 'is executing'), (3, 'completed'), (4, 'fail')], default=1, verbose_name='status')),
                ('oid', models.CharField(max_length=64, unique=True, verbose_name='order_id')),
                ('url', models.URLField(db_index=True, verbose_name='url')),
                ('count', models.IntegerField(verbose_name='count')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='price')),
                ('real_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='real_price')),
                ('old_view_count', models.CharField(default='0', max_length=32, verbose_name='old_view_count')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='create_datetime')),
                ('memo', models.TextField(blank=True, null=True, verbose_name='notes')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.customer', verbose_name='customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='customer',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.level', verbose_name='level'),
        ),
    ]