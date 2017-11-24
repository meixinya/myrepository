from django.conf.urls import include,url
from django.contrib import admin

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^myadmin/', include('myadmin.urls')), #网站后台路由
    url(r'^', include('myweb.urls')),           #网站前台路由

]
