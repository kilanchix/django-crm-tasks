
app_name = 'main'
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('clients/', views.clients, name='clients'),
    path('deals/', views.deals, name='deals'),
    path('add-deal/', views.add_deal, name='add_deal'),
    # удалены add-client и add-deal, теперь только через JS-модалки
    # удалён edit_client, теперь только через JS-модалки
    path('client/<int:client_id>/delete/', views.delete_client, name='delete_client'),
    # удалён edit_deal, теперь только через JS-модалки
    path('deal/<int:deal_id>/delete/', views.delete_deal, name='delete_deal'),
    path('deal/<int:deal_id>/edit/', views.edit_deal, name='edit_deal'),
]
