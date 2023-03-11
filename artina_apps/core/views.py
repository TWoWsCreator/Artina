def searching_paintings(paintings, result_search):
    if result_search:
        try:
            return (
                paintings.filter(painting_creation_year=result_search)
                | paintings.filter(painting_size__iregex=result_search)
                | paintings.filter(painting_description__iregex=result_search)
            )
        except ValueError:
            return (
                paintings.filter(painting_description__iregex=result_search)
                | paintings.filter(painting_size__iregex=result_search)
                | paintings.filter(painting_name__iregex=result_search)
                | paintings.filter(
                    painting_gallery__gallery_name__iregex=result_search
                )
            )
    else:
        return paintings
