from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("message", "0001_initial"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(model_name="message", name="receiver", field=models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE, related_name="received_messages", to="user.user", ), ),
        migrations.AddField(model_name="message", name="sender", field=models.ForeignKey(
            on_delete=django.db.models.deletion.CASCADE, related_name="sent_messages", to="user.user", ), ),
    ]
