import os
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, FormView

from dotenv import load_dotenv

import users

from .forms import (
    CustomUserChangeForm,
    CustomUserCreationForm,
    PasswordResetEmailForm,
)
from .models import CustomUser

load_dotenv()


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/sign_up.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users:profile')

    def get_form(self):
        return self.form_class(
            self.request.POST or None,
            self.request.FILES,
            instance=self.request.user,
        )

    def form_valid(self, form):
        old_image = CustomUser.objects.get(id=self.request.user.id).image
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


class PasswordReset(FormView):
    template_name = 'users/password_reset.html'
    # model = PasswordResetEmail
    form_class = PasswordResetEmailForm

    @staticmethod
    def send_mail_for_reset_password(msg, from_mail, to_mail):
        password = os.environ.get('gmail_password', 'gmail_data')
        server = SMTP('smtp.gmail.com', port=587)
        server.starttls()

        try:
            server.login(from_mail, password)
            msg = MIMEText(msg)
            msg['Subject'] = 'Сброс пароля'
            server.sendmail(from_mail, to_mail, msg.as_string())

        except SMTPException:
            pass

    def form_valid(self, form):
        user_email = form.cleaned_data['user_email']
        try:
            user = CustomUser.objects.get(email=user_email)
        except users.models.CustomUser.DoesNotExist:
            messages.error(
                self.request,
                'Введите почту, которую вводили при регистрации на сайте.',
            )
            return redirect(reverse_lazy('users:password_reset'))
        msg_data = {
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }

        message = (
            f'Здравствуйте, {user.username}.\n'
            f'Ссылка перейдите по ссылке для сброса пароля ниже.\n'
            f'{msg_data["protocol"]}://{msg_data["domain"]}/users/'
            f'password_reset/confirm/{msg_data["uid"]}/{msg_data["token"]}'
            f' Если вы не запрашивали сброс пароля, напишите нам.'
            f'С уважением от команды Artina'
        )
        from_mail = 'artina.djangoproject@gmail.com'
        self.send_mail_for_reset_password(message, from_mail, user.email)
        return redirect(reverse_lazy('users:password_reset_done'))
