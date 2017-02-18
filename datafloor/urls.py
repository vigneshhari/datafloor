from django.contrib import admin
from django.conf.urls import include, url
from .view import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/' , home ),
    url(r'^', include('account.urls')),
    url(r'^', include('userclassifier.urls')),
    url(r'^', include('mlmarket.urls')),

]
