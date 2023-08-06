# THIS IS A ONE WAY MIGRATION FOR 1.1.0, BACKUP DATABASE BEFORE APPLYING

from django.db import migrations, models
import django.db.models.deletion

def clean_all_fittings(apps, schema_editor):
    EveDoctrine = apps.get_model('django_eveonline_doctrine_manager', 'EveDoctrine')
    EveFitting = apps.get_model('django_eveonline_doctrine_manager', 'EveFitting')
    EveSkillPlan = apps.get_model('django_eveonline_doctrine_manager', 'EveSkillPlan')
    EveDoctrine.objects.all().delete()
    EveFitting.objects.all().delete()
    EveSkillPlan.objects.all().delete()

def generate_default_roles(apps, schema_editor):
    EveDoctrineRole = apps.get_model(
        'django_eveonline_doctrine_manager', 'EveDoctrineRole')
    starter_roles = [
        {"name": "DPS", "icon": "https://wiki.eveuniversity.org/images/thumb/9/9e/Icon_turret_autocannon_large.png/32px-Icon_turret_autocannon_large.png"},
        {"name": "Logistics", "icon": "https://wiki.eveuniversity.org/images/thumb/b/b9/Icon_remote_armor_repair_i.png/32px-Icon_remote_armor_repair_i.png"},
        {"name": "Utility", "icon": "https://wiki.eveuniversity.org/images/thumb/7/76/Icon_energy_neutralizer_i.png/32px-Icon_energy_neutralizer_i.png"},
        {"name": "Command", "icon": "https://wiki.eveuniversity.org/images/thumb/1/1d/Warfare-links.png/32px-Warfare-links.png"},
        {"name": "Tackle", "icon": "https://wiki.eveuniversity.org/images/thumb/2/27/Icon_stasis_webifier_i.png/32px-Icon_stasis_webifier_i.png"},
    ]
    for role in starter_roles:
        EveDoctrineRole.objects.create(name=role['name'], icon=role['icon'])

class Migration(migrations.Migration):

    dependencies = [
        ('django_eveonline_doctrine_manager', '0003_auto_20191217_2241'),
    ]

    operations = [
        migrations.RunPython(clean_all_fittings,
                             reverse_code=migrations.RunPython.noop),
        migrations.CreateModel(
            name='EveDoctrineManagerTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='EveRequiredSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('level', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='evedoctrine',
            name='fittings',
        ),
        migrations.RemoveField(
            model_name='evefitting',
            name='category',
        ),
        migrations.RemoveField(
            model_name='evefitting',
            name='description',
        ),
        migrations.RemoveField(
            model_name='evefitting',
            name='id',
        ),
        migrations.RemoveField(
            model_name='evefitting',
            name='name',
        ),
        migrations.RemoveField(
            model_name='eveskillplan',
            name='effective_skills',
        ),
        migrations.RemoveField(
            model_name='eveskillplan',
            name='fitting',
        ),
        migrations.RemoveField(
            model_name='eveskillplan',
            name='id',
        ),
        migrations.RemoveField(
            model_name='eveskillplan',
            name='minimum_skills',
        ),
        migrations.AddField(
            model_name='evefitting',
            name='refit_of',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='django_eveonline_doctrine_manager.EveFitting'),
        ),
        migrations.RenameModel(
            old_name='EveFitCategory',
            new_name='EveDoctrineRole',
        ),
        migrations.CreateModel(
            name='EveDoctrineManagerBaseObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, null=True)),
                ('doctrines', models.ManyToManyField(blank=True, to='django_eveonline_doctrine_manager.EveDoctrine')),
                ('required_skills', models.ManyToManyField(blank=True, to='django_eveonline_doctrine_manager.EveRequiredSkill')),
                ('roles', models.ManyToManyField(blank=True, to='django_eveonline_doctrine_manager.EveDoctrineRole')),
                ('tags', models.ManyToManyField(blank=True, to='django_eveonline_doctrine_manager.EveDoctrineManagerTag')),
            ],
        ),
        migrations.AddField(
            model_name='evedoctrine',
            name='tags',
            field=models.ManyToManyField(blank=True, to='django_eveonline_doctrine_manager.EveDoctrineManagerTag'),
        ),
        migrations.AddField(
            model_name='evefitting',
            name='evedoctrinemanagerbaseobject_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_eveonline_doctrine_manager.EveDoctrineManagerBaseObject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eveskillplan',
            name='evedoctrinemanagerbaseobject_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='django_eveonline_doctrine_manager.EveDoctrineManagerBaseObject'),
            preserve_default=False,
        ),
        migrations.RunPython(generate_default_roles,
                             reverse_code=migrations.RunPython.noop),
    ]
