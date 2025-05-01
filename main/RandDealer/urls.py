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
    path('registeruser', views.registeruser, name='registeruser'),
    path('verifyemail/<uuid:token>/', views.verifyemail, name='verifyemail'),
    path('afterregister', views.afterregister, name='afterregister'),
    path('profile', views.profile, name='profile'),
    path('editprofileinfo', views.editprofileinfo, name='editprofileinfo')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)