from django.urls import path
from .views import DealsView

urlpatterns = [
    path('', DealsView.as_view()),
]
