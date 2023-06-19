from django.urls import path

from pages.views import AboutView, RulesView
from pages.apps import PagesConfig

app_name = PagesConfig.name

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('rules/', RulesView.as_view(), name='rules'),
]
