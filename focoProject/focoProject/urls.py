
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from votacion.views import login_view, pase

urlpatterns = [
    path('admin/login/', login_view, name='admin_login'),
    path('votacion/',  include('votacion.urls')),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('', pase, name='index'),
   
]

# add at the last
#urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
