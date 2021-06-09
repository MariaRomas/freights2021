from django.urls import path
from django.conf.urls import include
from . import views


urlpatterns = [

path('', views.index, name='index'),
path('about/', views.about, name='about'),
path('contacts/', views.contacts, name='contacts'),
path('freights/', views.FreightsView.as_view(), name='freights'),
path("filter/", views.FilterFreightsView.as_view(), name='filter'),
path("cars/", views.CarsView.as_view(), name='cars'),
path("news/", views.NewsView.as_view(), name='news'),
path("news/<str:slug>/", views.NewsDetailView.as_view(), name="news_detail"),
path("accounts/", include('accounts.urls')),
path("search/", views.Search.as_view(), name='search'),
path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
path("json-filter/", views.JsonFilterFreightsView.as_view(), name='json_filter'),
path("<slug:slug>/", views.FreightDetailView.as_view(), name="freight_detail"),
path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
path("worker/<str:slug>/", views.WorkerView.as_view(), name="worker_detail"),

]