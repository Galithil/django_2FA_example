"""auth_webapp URL Configuration

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
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('', views.index, name='index'),
path('homepage', views.homepage, name='homepage'),
path('api/createusers', views.create_users),
path('api/fetchallusers', views.fetch_all_users),
path('api/fetchuser', views.fetch_user),
path('api/checktfa', views.check_tfa),
path('api/settfa', views.setup_tfa),
path('api/deltfa', views.delete_tfa),
path('api/logout', views.logout_user),
path('api/getqrcode', views.get_qr_code),
    path('admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

