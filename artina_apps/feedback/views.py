import django.conf
import django.contrib
import django.core.files.storage
import django.template.loader
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
        message = django.template.loader.render_to_string(
            'feedback/feedback_mail.html', feedback_form.cleaned_data
        )
        core.views.send_mail_user(message, mail, msg_subj='Спасибо за отзыв')
        django.contrib.messages.success(
            self.request, 'Ваше сообщение отправлено'
        )
        return super().forms_valid(forms)

    # def form_invalid(self, form):
    #     django.contrib.messages.success(
    #         self.request, 'Форма заполнена с ошибками'
    #     )
    #     return super().form_invalid(form)
