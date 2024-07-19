from factory import Iterator, SubFactory, django, fuzzy

from house.models import (Apartment, House, Tariff, WaterMeter,
                          WaterMeterReading)


class HouseFactory(django.DjangoModelFactory):

    class Meta:
        model = House

    city = Iterator(
        (
            'Санкт-Петербург',
            'Москва',
            'Калининград',
        ),
    )

    street = Iterator(
        (
            'пр Мира',
            'ул Ленина',
            'пл Победы',
        ),
    )

    house_number = fuzzy.FuzzyInteger(1, 300)


class ApartmentFactory(django.DjangoModelFactory):

    class Meta:
        model = Apartment

    house = SubFactory(HouseFactory)
    number = fuzzy.FuzzyInteger(1, 100)
    area = fuzzy.FuzzyInteger(25, 100)


class TariffFactory(django.DjangoModelFactory):

    class Meta:
        model = Tariff

    name = Iterator(
        (
            'Водоснабжение',
            'Содержание общего имущества',
        ),
    )
    price_per_unit = Iterator(
        (
            37,
            100,
        ),
    )
    is_water_tariff = Iterator(
        (
            True,
            False,
        ),
    )
    is_area_tariff = Iterator(
        (
            False,
            True,
        ),
    )


class WaterMeterFactory(django.DjangoModelFactory):

    class Meta:
        model = WaterMeter

    name = Iterator(
        (
            'Кухня',
            'Санузел_1',
            'Санузел_2',
        ),
    )
    serial_number = fuzzy.FuzzyInteger(10000, 99999)
    apartment = SubFactory(ApartmentFactory)


class WaterMeterReadingFactory(django.DjangoModelFactory):

    class Meta:
        model = WaterMeterReading

    water_meter = fuzzy.FuzzyChoice(WaterMeter.objects.filter(name='Кухня'))

    reading_date = Iterator(
        (
            '2024-05-05',
            '2024-06-05',
            '2024-07-05',
        ),
    )
    value = Iterator(
        (
            1453,
            1457,
            1465,
        ),
    )
