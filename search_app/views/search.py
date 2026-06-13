from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from search_app.models import FakeModel
from time import time


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

        search_field=request.POST.get('search_field')
        context = {'rows_count':FakeModel.objects.count()}

        # guess the search_field type, name, phone, national_code

        # do the search
        results = set()
        results.update(q1:=FakeModel.objects.filter(first_name__icontains=search_field))
        results.update(q2:=FakeModel.objects.exclude(last_name=(i for i in q1.all())).filter(last_name__icontains=search_field))
        results.update(q3:=FakeModel.objects.exclude(city=(j for j in q2.all())).filter(city__icontains=search_field))
        results.update(q4:=FakeModel.objects.exclude(phone_number=(k for k in q3.all())).filter(phone_number__icontains=search_field))
        results.update(FakeModel.objects.exclude(national_code=(l for l in q4.all())).filter(national_code__icontains=search_field))
        
        # searching on city will reveal all people living there !!! is it ok ??
        
        context["results"]= results
        context['results_count'] = len(results)
        context["form"]= SearchForm()

        # request.POST['search_field'] ------ how to delete ??

        
        context['search_time']= time() - start_time

        return render(
            request,
            "search_app/search.html",
            context,
        )
