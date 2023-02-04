import string

from django.forms import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ArtistNameValidator:
    def __call__(self, artist_name):
        if len(artist_name.split(' ')) != 3:
            raise ValidationError('Введите фамилию, имя и отчество через пробел')
        return artist_name


@deconstructible
class ArtistYearsValidator:
    def __call__(self, artist_years):
        available_symbols = string.digits + '-'
        for sym in list(artist_years):
            if sym not in available_symbols:
                raise ValidationError('Используйте только цифры и тире')
        if '-' not in artist_years:
            raise ValidationError('Введите годы через тире')
        years = artist_years.split('-')
        if len(years) > 2:
            raise ValidationError('Введите 2 года через тире')
        for year in years:
            if len(year) > 4:
                raise ValidationError('Введите реальный год')
        return artist_years


@deconstructible
class PaintingSize:
    def __call__(self, painting_size):
        available_symbols = string.digits + 'x'
        for sym in list(painting_size):
            if sym not in available_symbols:
                raise ValidationError('Используйте только цифры и x')
        if 'x' not in painting_size:
            raise ValidationError('Введите размер через x')
        size = painting_size.split('-')
        if len(size) > 2:
            raise ValidationError('Введите 2 размера через x')
        return painting_size
