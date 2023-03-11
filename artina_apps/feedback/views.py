import email.mime.text
import os
import smtplib

import django.contrib
import django.core.mail
import django.urls
import django.views.generic
import dotenv

import feedback.forms
import feedback.models

dotenv.load_dotenv()


class FeedbackView(django.views.generic.FormView):
    template_name = 'feedback/feedback.html'
    form_class = feedback.forms.FeedbackForm
    model = feedback.models.Feedback
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

    def form_valid(self, form):
        from_mail = 'artina.djangoproject@gmail.com'
        name = form.cleaned_data['name']
        mail = form.cleaned_data['mail']
        feedback_text = form.cleaned_data['feedback_text']
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
        self.model.objects.create(**form.cleaned_data)
        django.contrib.messages.success(
            self.request, 'Ваше сообщение отправлено'
        )
        return super().form_valid(form)
