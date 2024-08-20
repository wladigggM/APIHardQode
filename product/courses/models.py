from django.db import models

from users.models import CustomUser


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоймость',
        null=True,
        blank=True
    )

    # TODO

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(
        Course,
        related_name='Lessons',
        on_delete=models.CASCADE
    )

    # TODO

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    # TODO

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)


class UserProductAccess(models.Model):
    """Модель доступа пользователя к продукту"""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    product = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Продукт'
    )
    is_access = models.BooleanField(
        default=False,
        verbose_name='Доступ'
    )

    class Meta:
        verbose_name = 'Доступ к продукту'
        verbose_name_plural = 'Доступы к продуктам'
        ordering = ('-id',)
