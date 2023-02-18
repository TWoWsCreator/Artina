from django.db import models


class Feedback(models.Model):
    name = models.CharField(
        'введите свое имя', max_length=150, help_text='Максимум 150 символов'
    )
    mail = models.EmailField(
        'введите свою почту', max_length=150, help_text='Максимум 150 символов'
    )
    feedback_text = models.CharField(
        'ваш отзыв', max_length=1000, help_text='Максимум 1000 символов'
    )
    created_on = models.DateTimeField('дата создания', auto_now_add=True)

    def __str__(self):
        return self.feedback_text[:20]

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
