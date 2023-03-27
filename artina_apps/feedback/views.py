import email.mime.text
import os
import smtplib
import time

import django.contrib
import django.core.files.storage
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
        name = form.cleaned_data[
            feedback.models.Feedback.name.field.name
        ]
        mail = form.cleaned_data[
            feedback.models.Feedback.mail.field.name
        ]
        feedback_text = form.cleaned_data[
            feedback.models.Feedback.feedback_text.field.name
        ]
        user_feedback = feedback.models.Feedback(
            name=name, feedback_text=feedback_text, mail=mail
        )
        user_feedback.save()
        if self.request.FILES.getlist(
            feedback.models.Feedback.files.field.name
        ):
            for file in self.request.FILES.getlist(
                feedback.models.Feedback.files.field.name
            ):
                media_feedback_path = f'media/feedback/{user_feedback.pk}'
                feedback_dir = os.path.join(
                    f'{media_feedback_path}/{time.time()}_{file.name}')
                os.makedirs(feedback_dir)
                file_system = django.core.files.storage.FileSystemStorage(
                    location=feedback_dir)
                filename = file_system.save(file.name, file)
                feedback_file = feedback.models.FeedbackFiles(
                    feedback=user_feedback,
                    file=filename,
                )
                feedback_file.save()
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
        return super().form_valid(form)
