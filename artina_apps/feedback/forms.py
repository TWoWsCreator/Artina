import django.forms

import feedback.models


class BootstrapControlForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class FeedbackForm(BootstrapControlForm):
    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.name.field.name,
            feedback.models.Feedback.mail.field.name,
            feedback.models.Feedback.feedback_text.field.name,
            feedback.models.Feedback.files.field.name,
        )
        textarea = django.forms.Textarea(attrs={'rows': 5})
        widgets = {
            feedback.models.Feedback.feedback_text.field.name: textarea,
            feedback.models.Feedback.files.field.name: (
                django.forms.ClearableFileInput(
                    attrs={
                        'class': 'form-control',
                        'type': 'file',
                        'multiple': True,
                    },
                )
            ),
        }
