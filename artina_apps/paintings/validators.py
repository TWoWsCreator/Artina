import django.forms
import django.utils.deconstruct


@django.utils.deconstruct.deconstructible
class SizeValidation:
    def __call__(self, painting_size):
        if 'x' not in painting_size:
            raise django.forms.ValidationError(
                'Введите размер картины через x'
            )
        sizes = painting_size.split('x')
        if len(sizes) != 2:
            raise django.forms.ValidationError(
                'Введите 2 числа - длину и ширину картины через x'
            )
        for size in sizes:
            if size == '':
                raise django.forms.ValidationError(
                    'Введите заполненный размер картины'
                )
        return painting_size
