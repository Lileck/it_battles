from django.urls import path

from . import views

urlpatterns = [
    path('battle/<int:event_id>/submit/', views.submit_solution, name='submit_solution'),
]