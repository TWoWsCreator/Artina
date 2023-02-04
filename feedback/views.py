import os
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException

from dotenv import load_dotenv

from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import FeedbackForm
from .models import Feedback

load_dotenv()


class FeedbackView(FormView):
    template_name = 'feedback/feedback.html'
    form_class = FeedbackForm
    model = Feedback
    success_url = reverse_lazy('feedback:feedback')

    @classmethod
    def send_mail_user(cls, msg, from_mail, to_mail):
        password = os.environ.get('gmail_password', 'gmail_data')
        server = SMTP('smtp.gmail.com', port=587)
        server.starttls()

        try:
            server.login(from_mail, password)
            msg = MIMEText(msg)
            msg["Subject"] = 'Спасибо за отзыв'
            server.sendmail(from_mail, to_mail, msg.as_string())

        except SMTPException:
            pass

    def form_valid(self, form):
        from_mail = 'artina.djangoproject@gmail.com'
        name = form.cleaned_data['name']
        mail = form.cleaned_data['mail']
        feedback_text = form.cleaned_data['feedback_text']
        message = f'Здравствуйте, {name}.\nСпасибо что оставили свой feedback.\n ' \
                  f'Ваша отзывчивость помогает нам развиваться\n' \
                  f'Ваш отзыв: {feedback_text}\n' \
                  f'Спасибо от команды Artina.'
        self.send_mail_user(message, from_mail, mail)
        send_mail(
            'Спасибо за отзыв',
            message=message,
            from_email=from_mail,
            recipient_list=[mail],
            fail_silently=False
        )
        self.model.objects.create(
            **form.cleaned_data
        )
        messages.success(self.request, 'Ваше сообщение отправлено')
        return super().form_valid(form)
