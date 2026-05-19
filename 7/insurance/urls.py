from django.urls import path

from insurance import views


app_name = "insurance"

urlpatterns = [
    path("", views.PolicyListView.as_view(), name="policy-list"),
    path("policies/new/", views.PolicyCreateView.as_view(), name="policy-create"),
    path("policies/<int:pk>/", views.PolicyDetailView.as_view(), name="policy-detail"),
    path("policies/<int:pk>/edit/", views.PolicyUpdateView.as_view(), name="policy-update"),
    path("clients/", views.ClientListView.as_view(), name="clients"),
    path("clients/new/", views.ClientCreateView.as_view(), name="client-create"),
    path("clients/<int:pk>/edit/", views.ClientUpdateView.as_view(), name="client-update"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/new/", views.ProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product-update"),
    path("claims/", views.ClaimListView.as_view(), name="claims"),
    path("claims/new/", views.ClaimCreateView.as_view(), name="claim-create"),
    path("claims/<int:pk>/edit/", views.ClaimUpdateView.as_view(), name="claim-update"),
]
