import email.mime.text
import os
import smtplib

import django.contrib
import django.core.files.storage
import django.core.mail
import django.urls
import django.views.generic
import dotenv
import multi_form_view.base

import feedback.forms
import feedback.models

dotenv.load_dotenv()


class FeedbackView(multi_form_view.base.MultiFormView):
    template_name = 'feedback/feedback.html'
    form_classes = {
        'feedback': feedback.forms.FeedbackForm,
        'feedback_files': feedback.forms.FeedbackFilesForm,
    }
    success_url = django.urls.reverse_lazy('feedback:feedback')

    @classmethod
    def send_mail_user(cls, msg, from_mail, to_mail):
        password = os.environ.get('gmail_password', 'gmail_data')
        server = smtplib.SMTP('smtp.gmail.com', port=587)
        server.starttls()

        try:
            server.login(from_mail, password)
            msg = email.mime.text.MIMEText(msg)
            msg['Subject'] = 'Спасибо за отзыв'
            server.sendmail(from_mail, to_mail, msg.as_string())

        except smtplib.SMTPException:
            pass

    def forms_valid(self, forms):
        from_mail = 'artina.djangoproject@gmail.com'
        feedback_form = forms['feedback']
        name = feedback_form.cleaned_data[
            feedback.models.Feedback.name.field.name
        ]
        mail = feedback_form.cleaned_data[
            feedback.models.Feedback.mail.field.name
        ]
        feedback_text = feedback_form.cleaned_data[
            feedback.models.Feedback.feedback_text.field.name
        ]
        feedback_item = feedback.models.Feedback.objects.create(
            **feedback_form.cleaned_data
        )
        feedback_item.save()

        for file in self.request.FILES.getlist(
            feedback.models.FeedbackFiles.file.field.name,
        ):
            feedback.models.FeedbackFiles.objects.create(
                file=file,
                feedback=feedback_item,
            )
        message = (
            f'Здравствуйте, {name}.\nСпасибо что оставили свой feedback.\n '
            f'Ваша отзывчивость помогает нам развиваться\n'
            f'Ваш отзыв: {feedback_text}\n'
            f'Спасибо от команды Artina.'
        )
        self.send_mail_user(message, from_mail, mail)
        django.core.mail.send_mail(
            'Спасибо за отзыв',
            message=message,
            from_email=from_mail,
            recipient_list=[mail],
            fail_silently=False,
        )
        django.contrib.messages.success(
            self.request, 'Ваше сообщение отправлено'
        )
        return super().forms_valid(forms)
