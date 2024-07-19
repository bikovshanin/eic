from django.db import models

from house.models import Apartment


class CalculationResult(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        related_name='calculation_results',
        on_delete=models.CASCADE,
        verbose_name='Квартира',
    )
    month = models.DateField(
        auto_now=True,
        verbose_name='Расчетный период'
    )
    water_cost = models.FloatField(
        verbose_name='Стоимость воды'
    )
    maintenance_cost = models.FloatField(
        verbose_name='Стоимость содержания'
    )

    class Meta:
        verbose_name = 'Стоимость услуг'
        verbose_name_plural = 'Стоимость услуг'
        ordering = ('apartment',)

    def __str__(self):
        return (
            f'{self.apartment.house.city}, '
            f'{self.apartment.house.street} '
            f'{self.apartment.house.house_number}, '
            f'Кв {self.apartment.number} '
            f'стоимость воды: {self.water_cost}, '
            f'стоимость содержания: {self.maintenance_cost}, '
            f'общая стоимость: {self.water_cost + self.maintenance_cost}'
        )
