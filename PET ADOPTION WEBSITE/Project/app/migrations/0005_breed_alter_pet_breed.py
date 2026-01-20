

import django.db.models.deletion
from django.db import migrations, models


def migrate_breeds_forward(apps, schema_editor):
    """Create Breed objects from pet breed strings and update pets"""
    Pet = apps.get_model('app', 'Pet')
    Breed = apps.get_model('app', 'Breed')
    

    breed_map = {}
    for breed_name in Pet.objects.values_list('breed', flat=True).distinct():
        if breed_name:
            breed_obj, _ = Breed.objects.get_or_create(name=breed_name)
            breed_map[breed_name] = breed_obj.id
    



def migrate_breeds_backward(apps, schema_editor):
    """Reverse the migration"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_pet_category_alter_pet_breed_delete_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('size', models.CharField(blank=True, choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('extra_large', 'Extra Large')], max_length=20)),
                ('temperament', models.CharField(blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),

        migrations.AddField(
            model_name='pet',
            name='breed_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pets_temp', to='app.breed'),
        ),
        migrations.RunPython(migrate_breeds_forward, migrate_breeds_backward),
 
        migrations.RemoveField(
            model_name='pet',
            name='breed',
        ),

        migrations.RenameField(
            model_name='pet',
            old_name='breed_fk',
            new_name='breed',
        ),

        migrations.AlterField(
            model_name='pet',
            name='breed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pets', to='app.breed'),
        ),
    ]
