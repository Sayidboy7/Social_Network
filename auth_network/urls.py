from django.urls import path
from auth_network import views

urlpatterns = [
	path('login/', views.login_clearly, name='login'),
	path('register/', views.register, name='register'),
	path('logout/', views.logout, name='logout')
]