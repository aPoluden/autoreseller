# Generated by Django 2.0.1 on 2019-01-02 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawler', '0023_auto_20190102_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchcriteria',
            name='city',
            field=models.CharField(blank=True, choices=[('Vilnius', 'Vilnius'), ('Kaunas', 'Kaunas'), ('Klaipėda', 'Klaipėda'), ('Šiauliai', 'Šiauliai'), ('Panevėžys', 'Panevėžys'), ('Akmenė', 'Akmenė'), ('Alytus', 'Alytus'), ('Anykščiai', 'Anykščiai'), ('Ariogala', 'Ariogala'), ('Birštonas', 'Birštonas'), ('Biržai', 'Biržai'), ('Druskininkai', 'Druskininkai'), ('Elektrėnai', 'Elektrėnai'), ('Gargždai', 'Gargždai'), ('Ignalina', 'Ignalina'), ('Jonava', 'Jonava'), ('Joniškis', 'Joniškis'), ('Juodkrantė', 'Juodkrantė'), ('Jurbarkas', 'Jurbarkas'), ('Kaišiadorys', 'Kaišiadorys'), ('Kalvarija', 'Kalvarija'), ('Karklė', 'Karklė'), ('Kazlų Rūda', 'Kazlų Rūda'), ('Kėdainiai', 'Kėdainiai'), ('Kelmė', 'Kelmė'), ('Kretinga', 'Kretinga'), ('Kupiškis', 'Kupiškis'), ('Kuršėnai', 'Kuršėnai'), ('Lazdijai', 'Lazdijai'), ('Marijampolė', 'Marijampolė'), ('Mažeikiai', 'Mažeikiai'), ('Melnragė', 'Melnragė'), ('Molėtai', 'Molėtai'), ('Naujoji Akmenė', 'Naujoji Akmenė'), ('Nemenčinė', 'Nemenčinė'), ('Neringa', 'Neringa'), ('Nida', 'Nida'), ('Pagėgiai', 'Pagėgiai'), ('Pakruojis', 'Pakruojis'), ('Palanga', 'Palanga'), ('Pasvalys', 'Pasvalys'), ('Plungė', 'Plungė'), ('Prienai', 'Prienai'), ('Radviliškis', 'Radviliškis'), ('Raseiniai', 'Raseiniai'), ('Rietavas', 'Rietavas'), ('Rokiškis', 'Rokiškis'), ('Šakiai', 'Šakiai'), ('Šalčininkai', 'Šalčininkai'), ('Šilalė', 'Šilalė'), ('Šilutė', 'Šilutė'), ('Širvintos', 'Širvintos'), ('Skaudvilė', 'Skaudvilė'), ('Skuodas', 'Skuodas'), ('Švenčionys', 'Švenčionys'), ('Šventoji', 'Šventoji'), ('Tauragė', 'Tauragė'), ('Telšiai', 'Telšiai'), ('Trakai', 'Trakai'), ('Ukmergė', 'Ukmergė'), ('Utena', 'Utena'), ('Varėna', 'Varėna'), ('Vievis', 'Vievis'), ('Vilkaviškis', 'Vilkaviškis'), ('Visaginas', 'Visaginas'), ('Zarasai', 'Zarasai')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='fuel',
            field=models.CharField(blank=True, choices=[('Dyzelinas', 'Dyzelinas'), ('Benzinas', 'Benzinas'), ('Benzinas / dujos', 'Benzinas / dujos'), ('Benzinas / elektra', 'Benzinas / elektra'), ('Elektra', 'Elektra'), ('Dyzelinas / elektra', 'Dyzelinas / elektra'), ('Dyzelinas / dujos', 'Dyzelinas / dujos'), ('Bioetanolis (E85)', 'Bioetanolis (E85)')], default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='make',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='model',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='year_from',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='searchcriteria',
            name='year_to',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
