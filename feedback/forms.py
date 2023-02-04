from django.forms import ModelForm, Textarea

from .models import Feedback


class FeedbackForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Feedback
        fields = (
            Feedback.name.field.name,
            Feedback.mail.field.name,
            Feedback.feedback_text.field.name,
        )
        widgets = {
            Feedback.feedback_text.field.name: Textarea(
                attrs={'rows': 5}
            )
        }
