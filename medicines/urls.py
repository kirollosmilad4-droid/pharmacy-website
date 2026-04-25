from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.medicine_list),
    path('order/<int:id>', views.order_medicine),
    path('cart/', views.cart_view),
    path('remove/<int:id>', views.remove_from_cart),
    path('clear/', views.clear_cart),
    path('checkout/', views.checkout, name='checkout'),
    path('medicine/<int:id>/', views.medicine_detail, name='medicine_detail'),
    path('fav/<int:id>/', views.add_to_favourite, name='fav'),
    path('favourite/',views.favourite_view), 
    path('register/', views.register_view),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('orders/', views.orders_view),
]

# دي تضيفها تحت
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)