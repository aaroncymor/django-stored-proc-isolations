from django.urls import path
from . import views

urlpatterns = [
    path('place_order_snapshot/<int:product_id>/', views.place_order_snapshot, name='place_order_snapshot'),
    path('order_success/<int:product_id>/', views.order_success, name='order_success'),
    path('product/detail/committed/<int:product_id>/', views.product_detail_read_committed, name='product_detail_committed'),
    path('product/detail/default/<int:product_id>/', views.product_detail_default, name='product_detail_default'),
    path('product/detail/risky/<int:product_id>/', views.potentially_risky_view_read_uncommitted, name='product_detail_risky'),
]
