from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0002_receiptimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_id', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=512, blank=True)),
                ('types', models.JSONField(default=list, blank=True)),
                ('cuisine', models.CharField(max_length=255, blank=True, null=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('raw', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
