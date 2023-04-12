import django.contrib
import django.contrib.auth.admin

import users.forms
import users.models


class CustomUserAdmin(django.contrib.auth.admin.UserAdmin):
    list_display = (
        users.models.CustomUser.email.field.name,
        users.models.CustomUser.username.field.name,
        users.models.CustomUser.is_staff.field.name,
    )
    readonly_fields = (
        users.models.CustomUser.email.field.name,
        users.models.CustomUser.username.field.name,
        users.models.CustomUser.birthday.field.name,
    )
    fieldsets = (
        (
            'данные идентификации',
            {
                'fields': (
                    users.models.CustomUser.email.field.name,
                    users.models.CustomUser.username.field.name,
                    users.models.CustomUser.password.field.name,
                )
            },
        ),
        (
            'другие данные пользователя',
            {
                'fields': (
                    users.models.CustomUser.first_name.field.name,
                    users.models.CustomUser.last_name.field.name,
                    users.models.CustomUser.birthday.field.name,
                    users.models.CustomUser.image.field.name,
                    users.models.CustomUser.feedback_mails.field.name,
                )
            },
        ),
        (
            'разрешения',
            {
                'fields': (
                    users.models.CustomUser.is_staff.field.name,
                    users.models.CustomUser.is_active.field.name,
                )
            },
        ),
    )


django.contrib.admin.site.register(users.models.CustomUser, CustomUserAdmin)
