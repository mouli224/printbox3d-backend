# Generated migration for adding image_url to Category model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_product_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_url',
            field=models.URLField(blank=True, help_text='Category image — paste the full S3 URL here (preferred over file upload)', max_length=500),
        ),
    ]
