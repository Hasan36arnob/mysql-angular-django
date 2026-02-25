from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.create_item, name='create_item'),
    path('items/<int:item_id>/', views.update_item, name='update_item'),
    path('items/<int:item_id>/delete/', views.delete_item, name='delete_item'),
    # auth
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/me/', views.me, name='me'),
    # projects
    path('projects/', views.projects, name='projects'),
    path('projects/create/', views.create_project, name='create_project'),
    # tasks
    path('projects/<int:project_id>/tasks/', views.tasks, name='tasks'),
    path('projects/<int:project_id>/tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    # comments
    path('tasks/<int:task_id>/comments/', views.comments, name='comments'),
    path('tasks/<int:task_id>/comments/create/', views.create_comment, name='create_comment'),
]
