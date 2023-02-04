from django.db.models import Q


def searching_paintings(paintings, result_search):
    if result_search:
        try:
            return paintings.filter(Q(painting_creation_year=result_search) |
                                    Q(painting_size__iregex=result_search) |
                                    Q(painting_description__iregex=result_search))
        except ValueError:
            return paintings.filter(Q(painting_description__iregex=result_search) |
                                    Q(painting_size__iregex=result_search) |
                                    Q(painting_name__iregex=result_search) |
                                    Q(painting_gallery__gallery_name__iregex=result_search))
    else:
        return paintings
