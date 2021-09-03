from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView, BaseDetailView
from django.db.models import Q

class Home(ListView):
    template_name = "core/index.html"

    def get_queryset(self):
        return []

