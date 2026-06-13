from time import time
from typing import Any

from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from search_app.models import FakeModel


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
        start_time = time()

        search_field = request.POST.get("search_field", "")
        context: dict[str, Any] = {"rows_count": FakeModel.objects.count()}

        # guess the search_field type, name, phone, national_code
        context["message"] = ""

        results: set[FakeModel] = set()

        search_field.replace("+", "")
        if search_field.isdigit():
            if len(search_field) == 12:
                results.update(
                    FakeModel.objects.filter(phone_number__iexact=search_field)
                )
            elif len(search_field) == 10:
                results.update(
                    FakeModel.objects.filter(national_code__iexact=search_field)
                )
            else:
                context["message"] = (
                    "Please enter a valid phone number or national code !!"
                )
        else:
            results.update(
                query_set := FakeModel.objects.filter(
                    Q(first_name__iexact=search_field)
                    | Q(last_name__iexact=search_field)
                )
            )
            if not query_set:
                context["message"] = "Please enter a valid first name or last name !!"
        # searching on city will reveal all people living there !!! is it ok ??
        # results.update(FakeModel.objects.filter(city__icontains=search_field))

        # overall search
        # results.update(
        #     FakeModel.objects.filter(
        #         Q(first_name__icontains=search_field)
        #         | Q(last_name__icontains=search_field)
        #         | Q(phone_number__icontains=search_field)
        #         | Q(national_code__icontains=search_field)
        #         | Q(city__icontains=search_field)
        #     )
        # )

        context["results"] = results
        context["results_count"] = len(results)
        context["form"] = SearchForm()

        # request.POST['search_field'] ------ how to delete ??

        context["search_time"] = time() - start_time

        return render(
            request,
            "search_app/search.html",
            context,
        )
