from django.urls import path

from . import views

urlpatterns = [
    path('battle/<int:event_id>/submit/', views.submit_solution, name='submit_solution'),
    path('battle/<int:event_id>/host/', views.host_dashboard, name='host_dashboard'),
    path('battle/<int:event_id>/results/', views.results_fragment, name='results_fragment'),
    path('battle/<int:event_id>/vote/', views.vote_page, name='vote_page'),
    path('vote/<int:submission_id>/', views.cast_vote, name='cast_vote'),
]