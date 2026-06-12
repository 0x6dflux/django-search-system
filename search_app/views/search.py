from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View


class SearchForm(forms.Form):
    search_field = forms.CharField(label="Search", max_length=100)


@method_decorator(login_required, name="get")
@method_decorator(login_required, name="post")  # is it necessary ??
class SearchView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            "search_app/search.html",
            {"form": SearchForm()},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        results = ["test1", "test2"]

        context = {"form": SearchForm(), "results": results}

        return render(
            request,
            "search_app/search.html",
            context,
        )
