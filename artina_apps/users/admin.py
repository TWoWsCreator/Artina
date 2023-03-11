import django.contrib
import django.contrib.auth.admin

import users.forms
import users.models


class CustomUserAdmin(django.contrib.auth.admin.UserAdmin):
    add_form = users.forms.CustomUserCreationForm
    form = users.forms.CustomUserChangeForm
    model = users.models.CustomUser
    list_display = ('email', 'username', 'is_staff')
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'username',
                    'password',
                    'first_name',
                    'last_name',
                    'image',
                )
            },
        ),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


django.contrib.admin.site.register(users.models.CustomUser, CustomUserAdmin)
