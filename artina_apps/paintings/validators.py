from django.forms import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class SizeValidation:
    def __call__(self, painting_size):
        if 'x' not in painting_size:
            raise ValidationError('Введите размер картины через x')
        sizes = painting_size.split('x')
        if len(sizes) != 2:
            raise ValidationError(
                'Введите 2 числа - длину и ширину картины через x'
            )
        for size in sizes:
            if size == '':
                raise ValidationError('Введите заполненный размер картины')
        return painting_size
