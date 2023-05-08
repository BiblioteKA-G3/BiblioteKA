from django.urls import path
from loans.views import LoanView, LoanDetailView, LoanHistoryStudentView


urlpatterns = [
    path("loans/", LoanView.as_view()),
    path("loans/<int:pk>/history/", LoanHistoryStudentView.as_view()),
    path("loans/<str:username>/<int:pk>/", LoanDetailView.as_view()),
]
