import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.name.field.name,
            feedback.models.Feedback.mail.field.name,
            feedback.models.Feedback.feedback_text.field.name,
        )
        textarea = django.forms.Textarea(attrs={'rows': 5})
        widgets = {feedback.models.Feedback.feedback_text.field.name: textarea}
