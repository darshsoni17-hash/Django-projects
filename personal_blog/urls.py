from django.contrib import admin
from django.urls import path, include
from personal_blog.views import home, store_bill
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home/', home, name='home'),
      path('home/bill/<int:store_id>/', store_bill, name='store_bill'),
    path('admin/', admin.site.urls),
    path('chai/', include('chai.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
