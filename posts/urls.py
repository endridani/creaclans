from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.ListPost.as_view(), name='list'),
    path('new/', views.CreatePost.as_view(), name='create'),
    path('details/<int:pk>/', views.DetailPost.as_view(), name='detail'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete'),
    path('drafts/', views.ListDraftPost.as_view(), name='draft'),
    path('update/<int:pk>/', views.UpdatePost.as_view(), name='update'),
    path('<int:pk>/publish/', views.publish_post, name='publish_post')
]
