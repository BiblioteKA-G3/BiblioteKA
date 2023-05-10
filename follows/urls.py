from django.urls import path
from follows.views import FollowsCreateDestroyView


urlpatterns = [
    path("follows/<int:pk>/", FollowsCreateDestroyView.as_view())
]
