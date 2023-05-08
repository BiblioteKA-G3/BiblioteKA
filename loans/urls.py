from django.urls import path
from loans.views import LoanView, LoanDetailView


urlpatterns = [
    path("loans/", LoanView.as_view()),
    path("loans/<str:username>/<int:pk>/", LoanDetailView.as_view()),
]
