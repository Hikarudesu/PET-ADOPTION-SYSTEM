from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_pet_posted_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pet',
            name='category',
        ),
        migrations.AlterField(
            model_name='pet',
            name='breed',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
