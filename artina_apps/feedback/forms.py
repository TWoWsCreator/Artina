import django.forms

import core.forms
import feedback.models


class FeedbackForm(core.forms.BootstrapControlForm):
    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.name.field.name,
            feedback.models.Feedback.mail.field.name,
            feedback.models.Feedback.feedback_text.field.name,
        )
        textarea = django.forms.Textarea(attrs={'rows': 5})
        widgets = {
            feedback.models.Feedback.feedback_text.field.name: textarea,
        }


class FeedbackFilesForm(core.forms.BootstrapControlForm):
    class Meta:
        model = feedback.models.FeedbackFiles

        fields = (feedback.models.FeedbackFiles.file.field.name,)
        help_texts = {
            feedback.models.FeedbackFiles.file.field.name: (
                'При необходимости прикрепите файлы'
            ),
        }
        widgets = {
            feedback.models.FeedbackFiles.file.field.name: (
                django.forms.FileInput(
                    attrs={
                        'class': 'form-control',
                        'type': 'file',
                        'multiple': True,
                    },
                )
            ),
        }
