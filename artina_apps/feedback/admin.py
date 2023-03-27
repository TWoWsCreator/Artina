import django.contrib

import feedback.models


class FeedbackFilesAdmin(django.contrib.admin.TabularInline):
    model = feedback.models.FeedbackFiles
    fields = (feedback.models.FeedbackFiles.file.field.name,)


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
    inlines = (FeedbackFilesAdmin,)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
