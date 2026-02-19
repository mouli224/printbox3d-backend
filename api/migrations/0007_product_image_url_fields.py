from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_order_created_at_index'),
    ]

    operations = [
        # Remove old ImageFields and frontend_image CharField
        migrations.RemoveField(model_name='product', name='image'),
        migrations.RemoveField(model_name='product', name='image_2'),
        migrations.RemoveField(model_name='product', name='image_3'),
        migrations.RemoveField(model_name='product', name='frontend_image'),

        # Add new URLFields
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(
                max_length=500,
                default='',
                help_text='Primary image — paste the full S3 URL here',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='image_url_2',
            field=models.URLField(
                max_length=500,
                blank=True,
                help_text='Second image URL (optional)',
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='image_url_3',
            field=models.URLField(
                max_length=500,
                blank=True,
                help_text='Third image URL (optional)',
            ),
        ),
    ]
