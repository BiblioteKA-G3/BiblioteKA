from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.


class BookView(ListCreateAPIView):
    ...


class RetriveBookView(RetrieveUpdateDestroyAPIView):
    ...
