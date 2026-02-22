# Generated manually for title/description and nullable language fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('language_archive', '0006_languagerecord_youtube_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='languagerecord',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='タイトル'),
        ),
        migrations.AddField(
            model_name='languagerecord',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='説明'),
        ),
        migrations.AlterField(
            model_name='languagerecord',
            name='onomatopoeia_text',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='オノマトペ'),
        ),
        migrations.AlterField(
            model_name='languagerecord',
            name='meaning',
            field=models.TextField(blank=True, null=True, verbose_name='意味'),
        ),
        migrations.AlterField(
            model_name='languagerecord',
            name='usage_example',
            field=models.TextField(blank=True, null=True, verbose_name='用例'),
        ),
        migrations.AlterField(
            model_name='languagerecord',
            name='phonetic_notation',
            field=models.TextField(blank=True, null=True, verbose_name='音声記号'),
        ),
        migrations.AlterField(
            model_name='languagerecord',
            name='language_frequency',
            field=models.CharField(blank=True, choices=[('', '未選択'), ('daily', '日常的に使用'), ('often', 'よく使用'), ('sometimes', 'たまに使用'), ('rarely', 'ほとんど使用しない')], default='', max_length=20, null=True, verbose_name='言語使用頻度'),
        ),
    ]
