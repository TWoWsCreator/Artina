import django.views.generic


class HomepageView(django.views.generic.TemplateView):
    template_name = 'homepage/index.html'
