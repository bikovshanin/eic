from django.db import models
from django.utils import timezone


class House(models.Model):
    city = models.CharField(
        max_length=100,
        verbose_name='Город'
    )
    street = models.CharField(
        max_length=100,
        verbose_name='Улица'
    )
    house_number = models.PositiveIntegerField(
        verbose_name='Номер дома'
    )

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'
        ordering = ('city',)

    def __str__(self):
        return f'{self.city}, {self.street} {self.house_number}'


class Apartment(models.Model):
    house = models.ForeignKey(
        House,
        related_name='apartments',
        on_delete=models.CASCADE,
        verbose_name='Дом'
    )
    number = models.PositiveIntegerField(
        verbose_name='Номер квартиры'
    )
    area = models.FloatField(
        verbose_name='Площадь'
    )

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квартиры'
        ordering = ('number',)

    def __str__(self):
        return (
            f'{self.house.city}, '
            f'{self.house.street} '
            f'{self.house.house_number}, '
            f'Кв {self.number}'
        )


class Tariff(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название'
    )
    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    is_water_tariff = models.BooleanField(
        default=False,
        verbose_name='Тариф на воду'
    )
    is_area_tariff = models.BooleanField(
        default=False,
        verbose_name='Тариф на содержание общего имущества'
    )

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'
        ordering = ('id',)

    def __str__(self):
        return self.name


class WaterMeter(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Название(Локация)'
    )
    serial_number = models.PositiveIntegerField(
        verbose_name='Серийный номер'
    )
    apartment = models.ForeignKey(
        Apartment,
        related_name='water_meters',
        on_delete=models.CASCADE,
        verbose_name='Квартира'
    )

    class Meta:
        verbose_name = 'Счётчик'
        verbose_name_plural = 'Счётчики'
        ordering = ('id',)

    def __str__(self):
        return (
            f'{self.apartment.house.city}, '
            f'{self.apartment.house.street} '
            f'{self.apartment.house.house_number}, '
            f'Кв {self.apartment.number} '
            f'{self.name} '
            f'№ {self.serial_number}'
        )


class WaterMeterReading(models.Model):
    water_meter = models.ForeignKey(
        WaterMeter,
        related_name='readings',
        on_delete=models.CASCADE,
        verbose_name='Счётчик'
    )
    reading_date = models.DateField(
        default=timezone.now,
        verbose_name='Дата'
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Показания'
    )

    class Meta:
        verbose_name = 'Показания'
        verbose_name_plural = 'Показания'
        ordering = ('id',)

    def __str__(self):
        return (
            f'{self.water_meter.apartment.house.city}, '
            f'{self.water_meter.apartment.house.street} '
            f'{self.water_meter.apartment.house.house_number}, '
            f'Кв {self.water_meter.apartment.number} '
            f'{self.water_meter.name} '
        )
