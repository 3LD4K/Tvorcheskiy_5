from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("product/<int:pk>/installment/", views.InstallmentView.as_view(), name="installment_form"),
    path("customer/<int:pk>/installment_success/", views.InstallmentSuccessView.as_view(), name="installment_success"),
]
