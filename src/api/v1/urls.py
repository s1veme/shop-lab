from django.urls import include, path

urlpatterns = [
    path('products/', include('api.v1.products.urls')),
    path('orders/', include('api.v1.orders.urls')),
    path('users/', include('api.v1.users.urls')),
]
