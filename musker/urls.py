from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('profiles/', views.profiles, name='profiles'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/', views.register, name='register'),
    path('user_update/', views.userUpdate, name='user_update'),
    path('tweet/<int:pk>/', views.tweet_like, name='tweet_like'),
    path('detail/<int:pk>/', views.tweet_detail, name='tweet_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)