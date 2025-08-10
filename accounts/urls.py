from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve 

urlpatterns = [ 
    path('',views.home,name="home"),        
    path('home/',views.home,name="home"),     
    path('contact/',views.appointments,name='contact'),
    path('impact_initiatives/',views.impact_initiatives,name='impact_initiatives'),
    path('partnerships/',views.partnerships,name='partnerships'),
    path('donate/', views.donation_form, name='donation_form'),
    path('donation/callback/', views.payment_callback, name='payment_callback'),
    path('donation/success/', views.donation_success, name='donation_success'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]