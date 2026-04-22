from django.urls import path

from .views import *

urlpatterns = [
    path('products/', Products.as_view({'get': 'list', 'post': 'create'})),
    path('products/<uuid:pk>/', Products.as_view({'get': 'retrieve', 'delete': 'delete', 'patch': 'partial_update'})),

    path('carts/', Carts.as_view({'get': 'list', 'post': 'create'})),
    path('carts/<uuid:pk>/', Carts.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'delete'})),

    path('orders/', Orders.as_view({'get': 'list', 'post': 'create'})),
    path('orders/<uuid:pk>/', Orders.as_view({'get': 'retrieve', 'delete': 'delete'})),
    path('orders/<uuid:pk>/payment/check/', Orders.as_view({'get': 'check_payment_status'})),

    path('auth-token/', AuthenticationTokenView.as_view({'post': 'create'})),
    path('request-authentication/', AuthenticationRequestView.as_view({'post': 'create'})),

    path('user/', UserView.as_view({'get': 'retrieve'})),
    path('user/authenticate/', UserMethods.as_view({'post': 'authenticate'})),
    path('user/deauthenticate/', UserMethods.as_view({'get': 'deauthenticate'})),
    path('user/empty-cart/', UserMethods.as_view({'get': 'empty_user_cart'}))
]
