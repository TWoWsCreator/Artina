import string

import django.forms
import django.utils.deconstruct


@django.utils.deconstruct.deconstructible
class ArtistNameValidator:
    def __call__(self, artist_name):
        if len(artist_name.split(' ')) != 3:
            raise django.forms.ValidationError(
                'Введите фамилию, имя и отчество через пробел'
            )
        return artist_name


@django.utils.deconstruct.deconstructible
class ArtistYearsValidator:
    def __call__(self, artist_years):
        available_symbols = string.digits + '-'
        for sym in list(artist_years):
            if sym not in available_symbols:
                raise django.forms.ValidationError(
                    'Используйте только цифры и тире'
                )
        if '-' not in artist_years:
            raise django.forms.ValidationError('Введите годы через тире')
        years = artist_years.split('-')
        if len(years) != 2:
            raise django.forms.ValidationError('Введите 2 года через тире')
        for year in years:
            if len(year) > 4 or year == '':
                raise django.forms.ValidationError('Введите реальный год')
        return artist_years
