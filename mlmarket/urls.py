from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'market',views.market ),
    url(r'mview' , views.mview , name="mview"),
    url(r'addclass' , views.addclass),

]

