from django.urls import include, path

urlpatterns = [
    path('products/', include('api.v1.products.urls')),
]
