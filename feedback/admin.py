from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'feedback_text', 'created_on')
    fields = ('name', 'mail', 'feedback_text', 'created_on')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
