import os

import django.contrib
import django.contrib.auth
import django.contrib.auth.mixins
import django.contrib.auth.tokens
import django.shortcuts
import django.template.loader
import django.urls
import django.utils.encoding
import django.utils.http
import django.views.generic
import dotenv

import core.views
import users.forms
import users.models

dotenv.load_dotenv()


class SignUpView(django.views.generic.CreateView):
    form_class = users.forms.CustomUserCreationForm
    success_url = django.urls.reverse_lazy('users:login')
    template_name = 'users/sign_up.html'

    def form_valid(self, form):
        user = form.save()
        django.contrib.auth.login(self.request, user)
        return super().form_valid(form)


class ProfileView(
    django.contrib.auth.mixins.LoginRequiredMixin,
    django.views.generic.FormView,
):
    template_name = 'users/profile.html'
    model = users.models.CustomUser
    form_class = users.forms.CustomUserChangeForm
    success_url = django.urls.reverse_lazy('users:profile')

    def get_form(self):
        return self.form_class(
            self.request.POST or None,
            self.request.FILES,
            instance=self.request.user,
        )

    def form_valid(self, form):
        old_image = users.models.CustomUser.objects.get(
            id=self.request.user.id
        ).image
        if old_image:
            image_path = old_image.path
            if os.path.exists(image_path):
                os.remove(image_path)
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(
            initial=self.initial,
            instance=self.request.user,
        )
        return context


class PasswordReset(django.views.generic.FormView):
    template_name = 'users/password_reset.html'
    model = users.models.PasswordResetEmail
    form_class = users.forms.PasswordResetEmailForm

    def form_valid(self, form):
        user_email = form.cleaned_data['user_email']
        try:
            user = users.models.CustomUser.objects.get(email=user_email)
        except users.models.CustomUser.DoesNotExist:
            django.contrib.messages.error(
                self.request,
                'Введите почту, которую вводили при регистрации на сайте.',
            )
            return django.shortcuts.redirect(
                django.urls.reverse_lazy('users:password_reset')
            )
        token = django.contrib.auth.tokens.default_token_generator.make_token(
            user
        )
        msg_data = {
            'user': user.username,
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
            'uid': django.utils.http.urlsafe_base64_encode(
                django.utils.encoding.force_bytes(user.pk)
            ),
            'token': token,
        }
        message = django.template.loader.render_to_string(
            'users/password_reset_mail.html', msg_data
        )
        core.views.send_mail_user(message, user_email, msg_subj='Сброс пароля')
        return django.shortcuts.redirect(
            django.urls.reverse_lazy('users:password_reset_done')
        )
