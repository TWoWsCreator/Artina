from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/sign_up.html'


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    model = CustomUser
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('profile')

    def get_form(self, form_class=None):
        if form_class:
            return self.form_class(
                self.request.POST or None,
                instance=self.request.user
            )

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(
            initial=self.initial,
            instance=self.request.user,
            )
        return context

