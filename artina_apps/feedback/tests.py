import tempfile

import django.core.files.uploadedfile
import django.test
import django.urls

import feedback.forms
import feedback.models


class StaticURLTests(django.test.TestCase):
    def test_feedback_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        self.assertEqual(
            response.status_code,
            200,
            'Страница обратной связи не октрывается',
        )


class FeedbackContextTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.form = feedback.forms.FeedbackForm()
        return super().setUpClass()

    def test_feedback_in_context(self):
        response = django.test.Client().get(
            django.urls.reverse('feedback:feedback')
        )
        self.assertIn(
            'form',
            response.context,
            'Форма не передается в context',
        )

    def test_feedback_name_label(self):
        name_label = self.form.fields[
            feedback.models.Feedback.name.field.name
        ].label
        self.assertEqual(
            name_label,
            'Введите свое имя',
            'У поля name label не соответствует заданному',
        )

    def test_feedback_name_help_text(self):
        name_help_text = self.form.fields[
            feedback.models.Feedback.name.field.name
        ].help_text
        self.assertEqual(
            name_help_text,
            'Максимум 150 символов',
            'У поля name help_text не соответствует заданному',
        )

    def test_feedback_mail_label(self):
        mail_label = self.form.fields[
            feedback.models.Feedback.mail.field.name
        ].label
        self.assertEqual(
            mail_label,
            'Введите свою почту',
            'У поля mail label не соответствует заданному',
        )

    def test_feedback_mail_help_text(self):
        mail_help_text = self.form.fields[
            feedback.models.Feedback.mail.field.name
        ].help_text
        self.assertEqual(
            mail_help_text,
            'Максимум 150 символов',
            'У поля mail help_text не соответствует заданному',
        )

    def test_feedback_feedback_text_label(self):
        feedback_text_label = self.form.fields[
            feedback.models.Feedback.feedback_text.field.name
        ].label
        text_fail = 'У поля feedback_text label не соответствует заданному'
        self.assertEqual(
            feedback_text_label,
            'Ваш отзыв',
            text_fail,
        )

    def test_feedback_feedback_text_help_text(self):
        feedback_text_label = self.form.fields[
            feedback.models.Feedback.feedback_text.field.name
        ].help_text
        text_fail = 'У поля feedback_text help_text не соответствует заданному'
        self.assertEqual(
            feedback_text_label,
            'Максимум 1000 символов',
            text_fail,
        )

    @staticmethod
    def feedback_form_create(mail='ss@ya.ru'):
        form_data = {
            feedback.models.Feedback.name.field.name: 'Имя',
            feedback.models.Feedback.mail.field.name: mail,
            feedback.models.Feedback.feedback_text.field.name: 'Текст отзыва',
        }
        response = django.test.Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )
        return response

    def test_feedback_form_error_mail(self):
        response = self.feedback_form_create(mail='ssya.ru')
        self.assertTrue(
            response.context['form'].has_error('mail'),
            'У невалидного поле mail не возникает ошибка',
        )

    def test_feedback_form_create_negative(self):
        feedback_count = feedback.models.Feedback.objects.count()
        self.feedback_form_create(mail='ssya.ru')
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            feedback_count,
            'Создается объект не невалидными данными',
        )

    @staticmethod
    def create_feedback_request(files):
        form_data = {
            'name': 'Имя',
            'feedback_text': 'текст отзыва',
            'mail': 's@ya.ru',
            'files': files,
        }
        django.test.Client().post(
            django.urls.reverse('feedback:feedback'),
            data=form_data,
            follow=True,
        )

    @django.test.override_settings(
        MEDIA_ROOT=tempfile.TemporaryDirectory().name
    )
    def test_amount_feedback_files(self):
        files = [
            django.core.files.base.ContentFile(
                f'file_{index}'.encode(),
            )
            for index in range(10)
        ]
        self.create_feedback_request(files)
        self.assertEqual(
            feedback.models.FeedbackFiles.objects.filter(
                feedback=feedback.models.Feedback.objects.get(
                    name='Имя',
                )
            ).count(),
            10,
        )
