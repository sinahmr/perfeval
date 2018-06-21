# Generated by Django 2.0.6 on 2018-06-21 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0003_auto_20180619_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments_as_assessed', related_query_name='assessments_as_assessed', to='authentication.Employee')),
                ('assessor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments_as_assessor', related_query_name='assessments_as_assessor', to='authentication.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='PunnishmentReward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.TextField()),
                ('type', models.NullBooleanField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='QualitativeCriterion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choices', models.CharField(max_length=20, verbose_name='انتخاب ها')),
                ('interpretation', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuantitativeCriterion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formula', models.CharField(max_length=20, verbose_name='فرمول')),
                ('interpretation', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Scale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='عنوان')),
                ('description', models.TextField()),
                ('qualitativeCriterion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assessment.QualitativeCriterion')),
                ('quantitativeCriterion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assessment.QuantitativeCriterion')),
            ],
        ),
        migrations.CreateModel(
            name='ScaleAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualitativeAnswer', models.CharField(max_length=100)),
                ('quantitativeAnswer', models.CharField(max_length=100)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scale_answers', related_query_name='scale_answers', to='assessment.Assessment')),
                ('scale', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='assessment.Scale')),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startDate', models.DateTimeField()),
                ('endDate', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='punnishmentreward',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='punishment_rewards', related_query_name='punishment_rewards', to='assessment.Season'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', related_query_name='assessments', to='assessment.Season'),
        ),
    ]
