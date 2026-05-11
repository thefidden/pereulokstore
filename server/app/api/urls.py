from django.urls import path

from api.views.ProductViewSet import ProductViewSet
from api.views.CartsViewSet import CartsViewSet
from api.views.OrderViewSet import OrderViewSet
from api.views.AuthenticationTokenViewSet import AuthenticationTokenViewSet
from api.views.AuthenticationRequestViewSet import AuthenticationRequestView
from api.views.UserViewSet import UserViewSet
from api.views.UserMethodsViewSet import UserMethodsViewSet

urlpatterns = [
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'})),
    path(
        'products/<uuid:pk>/',
        ProductViewSet.as_view({'get': 'retrieve', 'delete': 'delete', 'patch': 'partial_update'}),
        name = 'product-detail'
    ),

    path('carts/', CartsViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('carts/<uuid:pk>/', CartsViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'delete'})),

    path('orders/', OrderViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('orders/<uuid:pk>/', OrderViewSet.as_view({'get': 'retrieve', 'delete': 'delete'})),
    path('orders/<uuid:pk>/payment/check/', OrderViewSet.as_view({'get': 'check_payment_status'})),

    path('auth-token/', AuthenticationTokenViewSet.as_view({'post': 'create'})),
    path('request-authentication/', AuthenticationRequestView.as_view({'post': 'create'})),

    path('user/', UserViewSet.as_view({'get': 'retrieve'})),
    path('user/authenticate/', UserMethodsViewSet.as_view({'post': 'authenticate'})),
    path('user/deauthenticate/', UserMethodsViewSet.as_view({'get': 'deauthenticate'})),
    path('user/empty-cart/', UserMethodsViewSet.as_view({'get': 'empty_user_cart'}))
]
