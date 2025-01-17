"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from .views import (
    main_spa,
    register,
    user_login,
    user_logout,
    user_api,
    hobby_api,
    similar_users,
    incoming_fr_api,
    outgoing_fr_api,
    get_friends,
    remove_friend,
    delete_friend_request,
    accept_friend_request,
    send_fr_api
)

urlpatterns = [
    path('', main_spa, name='main_spa'),
    #path('admin/', admin.site.urls),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # User-related API endpoints
    path('api/user/', user_api, name='user_api'),

    # Hobby-related API endpoints
    path('api/hobbies/', hobby_api, name='hobby_api'),
    path('api/similar-users/', similar_users, name='similar_users'),

    #Friend request related API endpoints
    path('api/outgoing-fr-api/',outgoing_fr_api, name='outgoing_fr_api'),
    path('api/incoming-fr-api/',incoming_fr_api, name='incoming_fr_api'),
    path('api/get-friends/',get_friends, name='get-friends'),
    path('api/remove-friend/',remove_friend, name="remove-friend"),
    path('api/delete-friend-request/',delete_friend_request, name="delete-friend-request"),
    path('api/accept-friend-request/',accept_friend_request, name="accept-friend-request"),
    path('api/send-friend-request/', send_fr_api, name='send_friend_request'),

    re_path(r'.*', main_spa),

]