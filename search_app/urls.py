from django.http import HttpResponse
from django.urls import path

from search_app.views.search import SearchView

app_name = "search_app"
urlpatterns = [
    path("", SearchView.as_view(), name="search"),
]
