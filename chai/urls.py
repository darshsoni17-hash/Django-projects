
from django.urls import path
from personal_blog.views import home, About, contact
from . import views


# local host:8000/chai/
# local host:8000/chai/order
urlpatterns = [
    path('', views.all_chai, name='all_chai'),
    path('order/', views.all_chai, name='order_chai'),
]