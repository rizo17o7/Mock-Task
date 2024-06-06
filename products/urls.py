from django.urls import path
from .views import ProductMaterialsAPIView, MultipleProductsMaterialsAPIView

urlpatterns = [
    path('product-materials/<int:product_id>/<int:quantity>/', ProductMaterialsAPIView.as_view(), name='product-materials'),
    path('multiple-products-materials/', MultipleProductsMaterialsAPIView.as_view(), name='multiple-products-materials'),
]