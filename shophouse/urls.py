from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('product/<int:pk>/',views.product,name='product'),
    
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('log-out/',views.logout_user,name='logout'),
    
    path('update_user/',views.update_user,name='update_user'),
    path('search_products/',views.search_products,name='search-products'),
    path('contact/',views.contact,name='contact'),
    path('about-us/',views.about,name='about'),
    path('registerbusiness/',views.registerbusiness,name='registerbusiness'),

    path('addproduct/',views.addproduct,name='addproduct'),
    path('updateproduct/<int:pk>/',views.updateproduct,name='updateproduct'),
    path('deleteproduct/<int:pk>/',views.deleteproduct,name='deleteproduct'),

    path('cart/',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('cart/',views.cart,name='cart'),

    path('business/',views.business,name='business'),

]