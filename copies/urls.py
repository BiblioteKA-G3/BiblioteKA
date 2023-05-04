from django.urls import path
from copies.views import CreateCopyView


urlpatterns = [
    path("copies/<int:id>/", CreateCopyView.as_view())
]
