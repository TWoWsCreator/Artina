import os

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView, FormView
from dotenv import load_dotenv

from .forms import CustomUserCreationForm, CustomUserChangeForm, PasswordResetEmailForm
from .models import CustomUser, PasswordResetEmail

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
            instance=self.request.user
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
    model = PasswordResetEmail
    form_class = PasswordResetEmailForm

    def form_valid(self, form):
        user_email = form.cleaned_data['user_email']
        try:
            user = CustomUser.objects.get(email=user_email)
        except Exception as e:
            print(e)
            return redirect(reverse_lazy('users:password_reset'))
        print(user_email, user.email)
        msg_data = {'protocol': 'http',
                    'domain': '127.0.0.1:8000',
                    'name': user.username,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)}
        msg_html = render_to_string('users/password_reset_email.html', msg_data)
        from_mail = 'artina.djangoproject@gmail.com'

        send_mail('Сброс пароля',
                  'ссылка',
                  from_email=from_mail,
                  recipient_list=[user.email],
                  fail_silently=True,
                  html_message=msg_html
                  )

        return redirect(reverse_lazy('users:password_reset_done'))

    # def get_context_data(self, **kwargs):
    #     self.form_class
