from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_product_discount_percentage_product_original_price'),
    ]

    operations = [
        # Index on Order.created_at (db_index=True on the field)
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        # Compound index on (status, -created_at) for filtered order listings
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status', '-created_at'], name='order_status_created_idx'),
        ),
    ]
