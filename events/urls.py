from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/book/', views.book_event, name='book_event'),
    path('my_bookings/',views.my_bookings,name='my_bookings'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('cancel_booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),



]