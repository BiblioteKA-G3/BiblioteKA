from django.urls import path
from . import views


urlpatterns = [path("loans/username/<int:pk>/", views.LoanView.as_view())]
