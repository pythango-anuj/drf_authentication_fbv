from django.urls import path
from . import views
urlpatterns = [
    # URL for Function based view:
    path('All Users/', views.all_users),
    path('Registration API/', views.register_user),
    path('Login API/', views.login_user),
    path('Logout API/', views.logout_user)
]