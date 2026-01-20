

from django.db import migrations


def populate_breeds(apps, schema_editor):
    """Create Breed objects from existing pet breed strings"""
    Pet = apps.get_model('app', 'Pet')
    Breed = apps.get_model('app', 'Breed')
    

    unique_breeds = set()
    for pet in Pet.objects.values('breed').distinct():
        if pet['breed']:
            unique_breeds.add(pet['breed'])
    

    breed_objects = {}
    for breed_name in unique_breeds:
        breed_obj, created = Breed.objects.get_or_create(name=breed_name)
        breed_objects[breed_name] = breed_obj
    

    for pet in Pet.objects.all():
        if pet.breed and hasattr(pet, 'breed'):
    
            pass


def reverse_populate_breeds(apps, schema_editor):
    """Delete created Breed objects"""
    Breed = apps.get_model('app', 'Breed')
    Breed.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_breed_alter_pet_breed'),
    ]

    operations = [
        migrations.RunPython(populate_breeds, reverse_populate_breeds),
    ]
