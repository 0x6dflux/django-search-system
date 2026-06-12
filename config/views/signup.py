from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class SignupView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = UserCreationForm()
        return render(request, "config/signup.html", context={"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            form = UserCreationForm()

        return render(request, "config/signup.html", context={"form": form})
