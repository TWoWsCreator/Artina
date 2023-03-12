import django.contrib
import django.contrib.auth.admin

import users.forms
import users.models


class CustomUserAdmin(django.contrib.auth.admin.UserAdmin):
    add_form = users.forms.CustomUserCreationForm
    form = users.forms.CustomUserChangeForm
    model = users.models.CustomUser
    list_display = (
        users.models.CustomUser.email.field.name,
        users.models.CustomUser.username.field.name,
        users.models.CustomUser.is_staff.field.name,
    )
    fieldsets = (
        (
            'данные пользователя',
            {
                'fields': (
                    users.models.CustomUser.email.field.name,
                    users.models.CustomUser.username.field.name,
                    users.models.CustomUser.password.field.name,
                    users.models.CustomUser.first_name.field.name,
                    users.models.CustomUser.last_name.field.name,
                    users.models.CustomUser.image.field.name,
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
