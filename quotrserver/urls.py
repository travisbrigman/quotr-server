"""quotrserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from quotrapi.views.proposalitem import ProposalItems
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import url, include
from quotrapi.views import *
from quotrapi.models import *


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'items', Items, 'item')
router.register(r'proposals', Proposals, 'proposals')
router.register(r'customers', Customers, 'customers')
router.register(r'users', QuotrUsers, 'users')
router.register(r'proposalitems', ProposalItems, 'proposalitems')

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
