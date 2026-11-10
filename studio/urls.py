from django.urls import path

from . import views

urlpatterns = [
    path("designs", views.DesignListView.as_view()),
    path("designs/<int:pk>", views.DesignDetailView.as_view()),
    path("masters", views.MasterListView.as_view()),
    path("masters/<int:pk>", views.MasterDetailView.as_view()),
]
