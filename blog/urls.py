from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomeView, SignUpView, PostUpdateView



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>/', HomeView.as_view(), name='post_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='edit_post'),

]