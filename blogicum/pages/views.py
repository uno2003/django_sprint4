from http import HTTPStatus

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    return render(request, 'pages/404.html',
                  status=HTTPStatus.NOT_FOUND)


def csrf_failure(request: HttpRequest, reason: str = '') -> HttpResponse:
    return render(request, 'pages/403csrf.html',
                  status=HTTPStatus.FORBIDDEN)


def internal_server_error(request: HttpRequest) -> HttpResponse:
    return render(request, 'pages/500.html',
                  status=HTTPStatus.INTERNAL_SERVER_ERROR)


class AboutView(TemplateView):
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    template_name = 'pages/rules.html'
