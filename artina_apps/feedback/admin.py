import django.contrib

import feedback.models


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.feedback_text.field.name,
        feedback.models.Feedback.created_on.field.name,
    )
    fields = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.feedback_text.field.name,
        feedback.models.Feedback.created_on.field.name,
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False
