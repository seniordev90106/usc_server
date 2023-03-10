# Generated by Django 4.1.2 on 2022-11-23 16:02

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import utils.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200, validators=[utils.validators.validate_collection_code])),
                ('name', models.CharField(default='', editable=False, max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Collections',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug_id', models.CharField(max_length=1024, unique=True)),
                ('package_id', models.CharField(blank=True, max_length=200, null=True)),
                ('granule_id', models.CharField(blank=True, max_length=200, null=True)),
                ('selected_year_from', models.IntegerField(blank=True, null=True)),
                ('root_node', models.BooleanField()),
                ('title', models.CharField(max_length=1024)),
                ('title_number', models.IntegerField(blank=True, null=True)),
                ('heading', models.CharField(max_length=1024)),
                ('section', models.CharField(choices=[('TOC', 'TOC'), ('FRONTMATTER', 'FRONTMATTER'), ('TOPPARENT', 'TOPPARENT'), ('LEAF', 'LEAF')], max_length=20)),
                ('textfile', models.CharField(max_length=1024)),
                ('htmlfile', models.CharField(max_length=1024)),
                ('pdffile', models.CharField(max_length=1024)),
                ('level', models.IntegerField()),
                ('browse_path', models.CharField(max_length=1024)),
                ('browse_path_alias', models.CharField(max_length=1024)),
                ('node_type', models.CharField(choices=[('node', 'node'), ('leaf', 'leaf')], max_length=4)),
                ('this_node', models.CharField(max_length=1024)),
                ('leaf_number_from', models.CharField(blank=True, max_length=20, null=True)),
                ('leaf_number_to', models.CharField(blank=True, max_length=20, null=True)),
                ('content', models.CharField(blank=True, max_length=1000000, null=True)),
                ('vector_column', django.contrib.postgres.search.SearchVectorField(null=True)),
                ('collection', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='USCODE.collection')),
                ('collection_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collectionCode', to='USCODE.collection')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='USCODE.node')),
            ],
            options={
                'verbose_name_plural': 'Nodes',
                'db_table': 'uscode_node',
            },
        ),
        migrations.AddIndex(
            model_name='node',
            index=django.contrib.postgres.indexes.GinIndex(fields=['vector_column'], name='uscode_node_vector__5fb865_gin'),
        ),
    ]
