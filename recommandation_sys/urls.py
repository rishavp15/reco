"""
URL configuration for recommandation_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    #path('netflix/', views.netflix),
    path('random_movie/', views.random_movie, name='random_movie'),
    path('familiar_suggestion/', views.f_suggestion, name='f_suggestion'),
    path('match_the_vibe/', views.match_the_vibe, name='match_the_vibe'),
    path('match_the_vibe2/', views.match_the_vibe, name='match_the_vibe2')
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

