from django.urls import path
from copies.views import (
    CreateCopyView,
    ListCopies
)


urlpatterns = [
    path("copies/<int:id>/", CreateCopyView.as_view()),
    path("copies/", ListCopies.as_view()),

]
