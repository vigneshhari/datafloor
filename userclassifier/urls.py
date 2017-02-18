from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'upload',views.upload ),
    url(r'updateclass',views.updateclass ),
    url(r'train',views.train ),
    url(r'classify',views.classify ),
    url(r'details', views.details),

]

