from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='receipts/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('receipt', models.ForeignKey(on_delete=models.CASCADE, related_name='images', to='receipts.receipt')),
            ],
        ),
    ]
