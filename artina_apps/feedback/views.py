import django.conf
import django.contrib
import django.core.files.storage
import django.core.mail
import django.urls
import django.views.generic
import multi_form_view.base

import core.views
import feedback.forms
import feedback.models


class FeedbackView(multi_form_view.base.MultiFormView):
    template_name = 'feedback/feedback.html'
    form_classes = {
        'feedback': feedback.forms.FeedbackForm,
        'feedback_files': feedback.forms.FeedbackFilesForm,
    }
    success_url = django.urls.reverse_lazy('feedback:feedback')

    def forms_valid(self, forms):
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
        core.views.send_mail_user(message, mail, msg_subj='Спасибо за отзыв')
        django.core.mail.send_mail(
            'Спасибо за отзыв',
            message=message,
            from_email=django.conf.settings.APP_MAIL,
            recipient_list=[mail],
            fail_silently=False,
        )
        django.contrib.messages.success(
            self.request, 'Ваше сообщение отправлено'
        )
        return super().forms_valid(forms)
