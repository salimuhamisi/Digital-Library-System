from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('administration/', views.administration, name='administration'),
    path('students/', views.students, name='students'),
    path('contact/', views.contact, name='contact'),
    path('aborrowed/', views.aborrowed, name='aborrowed'),
    path('snotifications/', views.snotifications, name='snotifications'),
    path('staffs/', views.staffs, name='staffs'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('sborrowed/', views.sborrowed, name='sborrowed'),
    path('signout/', views.signout, name='signout'),
    path('orders/', views.orders, name='orders'),
    path('videos/', views.videos, name='videos'),
    path('invoices/', views.invoices, name='invoices'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('reaches/', views.reaches, name='reaches'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)