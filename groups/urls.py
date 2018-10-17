from django.urls import path
from groups import views

app_name = 'groups'

urlpatterns = [
    path('', views.ListGroup.as_view(), name='list'),
    path('new/', views.CreateGroup.as_view(), name='create'),
    path('posts/in/<slug>/', views.DetailGroup.as_view(), name='detail'),
    path('delete/<slug>/', views.DeleteGroup.as_view(), name='delete'),
]
