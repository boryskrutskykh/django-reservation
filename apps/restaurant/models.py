from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator


class Hall(models.Model):
    name = models.CharField(unique=True, max_length=255, verbose_name='Название зала')
    hall_slug = AutoSlugField(populate_from='name', allow_unicode=True, always_update=True, verbose_name='Ссылка')
    width = models.PositiveSmallIntegerField(default=0, verbose_name='Ширина зала %', validators=[MinValueValidator(
        1), MaxValueValidator(100)])
    height = models.PositiveSmallIntegerField(default=0, verbose_name='Длина зала %', validators=[MinValueValidator(
        1), MaxValueValidator(100)])

    def __str__(self):
        return f'Зал {self.name}'

    class Meta:
        verbose_name_plural = 'Залы'


class Table(models.Model):
    SHAPE_CHOICES = (
        (1, 'Прямоугольный'),
        (2, 'Овальный'),
    )

    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='Зал')
    shape = models.IntegerField(choices=SHAPE_CHOICES, verbose_name='Тип стола')
    number = models.IntegerField(verbose_name='Номер стола', unique=True)
    seats = models.IntegerField(verbose_name='Количество мест', validators=[MinValueValidator(
        1), MaxValueValidator(100)])
    width = models.FloatField(default=0, verbose_name='Ширина стола (м)', validators=[MinValueValidator(
        1), MaxValueValidator(100)])
    height = models.FloatField(default=0, verbose_name='Длина стола (м)', validators=[MinValueValidator(
        1), MaxValueValidator(100)])
    coordinate_x = models.PositiveSmallIntegerField(default=0, verbose_name='Расположение по оси X')
    coordinate_y = models.PositiveSmallIntegerField(default=0, verbose_name='Расположение по оси Y')

    def __str__(self):
        return f'{self.number}'

    class Meta:
        verbose_name_plural = 'Столы'


class Order(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, verbose_name='Зал', related_name='tables')
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='order_table', verbose_name='Столик')
    date = models.DateField(verbose_name='Дата заказа')

    class Meta:
        verbose_name_plural = 'Заказы'
        unique_together = 'table', 'date'
