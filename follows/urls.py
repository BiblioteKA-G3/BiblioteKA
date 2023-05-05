from django.urls import path
from . import views


urlpatterns = [
    path("follows/<int:pk>/", views.FollowsCreateDestroyView.as_view())
]
