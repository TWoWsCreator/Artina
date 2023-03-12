import django.db.models


class Feedback(django.db.models.Model):
    name = django.db.models.CharField(
        'введите свое имя', max_length=150, help_text='Максимум 150 символов'
    )
    mail = django.db.models.EmailField(
        'введите свою почту', max_length=150, help_text='Максимум 150 символов'
    )
    feedback_text = django.db.models.CharField(
        'ваш отзыв', max_length=1000, help_text='Максимум 1000 символов'
    )
    created_on = django.db.models.DateTimeField(
        'дата создания', auto_now_add=True
    )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.feedback_text[:20]
