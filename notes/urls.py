from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('create/', views.create_note, name='create_note'),
    path('edit_note/<uuid:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<uuid:note_id>/', views.delete_note, name='delete_note'),

]
