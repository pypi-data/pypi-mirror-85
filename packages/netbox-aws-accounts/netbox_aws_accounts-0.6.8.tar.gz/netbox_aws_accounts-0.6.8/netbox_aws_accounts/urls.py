from django.urls import path
from . import views
from .utilities.urls import URLPatternGenerator

_urlpatterns_generators = [
    URLPatternGenerator("Accounts"),
    URLPatternGenerator("Regions"),
]

urlpatterns = [
    path('accounts/', views.AccountsListView.as_view(), name='account_list'),
    path('regions/', views.RegionsListView.as_view(), name='region_list'),
]

for gen in _urlpatterns_generators:
    urlpatterns.append(gen.list())
    urlpatterns.append(gen.add())
    urlpatterns.append(gen.bulkDelete())
    urlpatterns.append(gen.edit())
