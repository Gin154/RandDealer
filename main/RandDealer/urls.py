from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('base', views.base, name='base'),
    path('home', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('sell', views.sell, name='sell'),
    path('buy', views.buy, name='buy'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('car/<int:id>', views.car, name='car'),
    path('test', views.test, name='test'),
    path('confirmuser', views.confirmuser, name='confirmuser'),
    path('userconfirmed', views.userconfirmed, name='userconfirmed'),
    path('setpassword', views.setpassword, name='setpassword'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)