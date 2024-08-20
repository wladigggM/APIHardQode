from django.db import models


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
        auto_now_add=True,
        verbose_name='Дата и время начала курса'
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоймость',
        null=True,
        blank=True
    )
    is_available = models.BooleanField(
        default=True
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
        related_name='lessons',
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

    group_name = models.CharField(max_length=50, unique=True, null=True)
    course = models.ForeignKey(Course, related_name='student_groups', on_delete=models.CASCADE, null=True)
    is_full = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    @staticmethod
    def get_or_create_group(course):
        """Получить группу с минимальным кол-вом студентов / Создать 10 групп"""
        from users.models import Subscription
        from django.db import transaction

        max_students_in_group = 30
        num_groups_required = 10

        with transaction.atomic():
            # Получить или создать группы
            groups = Group.objects.filter(course=course)

            # Если групп меньше необходимого количества, создаем недостающие
            if groups.count() < num_groups_required:
                groups_to_create = num_groups_required - groups.count()
                for i in range(groups_to_create):
                    Group.objects.create(course=course, group_name=f'{course} Group: {groups.count() + 1}')
                groups = Group.objects.filter(course=course)

            # Получаем список групп с количеством студентов в каждой
            group_student_counts = {
                group: Subscription.objects.filter(course=course, group=group).count()
                for group in groups
            }

            # Фильтруем группы, которые еще не заполнены
            available_groups = [
                group for group, count in group_student_counts.items()
                if count < max_students_in_group
            ]

            if available_groups:
                # Выбираем группу с наименьшим количеством студентов
                selected_group = min(available_groups, key=lambda g: group_student_counts[g])
                return selected_group

    @staticmethod
    def get_student_count_in_group(course, group_id):
        from users.models import Subscription

        return Subscription.objects.filter(course=course, group=group_id).count()

    def update_is_full_status(self):
        """Обновить статус группы, если количество студентов достигло максимума."""
        max_students_in_group = 30
        student_count = self.subscription_set.count()  # Подсчет текущего количества студентов в группе

        # Если количество студентов равно или больше 30, устанавливаем is_full в True
        if student_count >= max_students_in_group:
            self.is_full = True
        else:
            self.is_full = False

        self.save()
