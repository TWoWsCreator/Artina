import django.test


class CheckFieldsTestCase(django.test.TestCase):
    def check_content_value(
        self,
        item,
        exists,
        prefetched=(),
        not_loaded=(),
    ):
        check_dict = item.__dict__

        for value in exists:
            self.assertIn(value, check_dict)

        for value in prefetched:
            self.assertIn(value, check_dict['_prefetched_objects_cache'])

        for value in not_loaded:
            self.assertNotIn(value, check_dict)
