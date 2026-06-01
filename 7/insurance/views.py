from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from insurance.forms import ClaimForm, ClientForm, InsuranceProductForm, PolicyForm
from insurance.models import Claim, Client, InsuranceProduct, Policy


class SuccessMessageMixin:
    success_message = "Изменения сохранены."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class PolicyListView(ListView):
    model = Policy
    template_name = "insurance/policy_list.html"
    context_object_name = "policies"
    paginate_by = 20

    def get_queryset(self):
        return (
            Policy.objects.select_related("client", "product")
            .prefetch_related("claims")
            .order_by("-created_at")
        )


class PolicyDetailView(DetailView):
    model = Policy
    template_name = "insurance/policy_detail.html"
    context_object_name = "policy"

    def get_queryset(self):
        return Policy.objects.select_related("client", "product").prefetch_related("claims")


class PolicyCreateView(SuccessMessageMixin, CreateView):
    model = Policy
    form_class = PolicyForm
    template_name = "insurance/model_form.html"
    success_message = "Полис добавлен."
    extra_context = {"title": "Добавить полис", "submit_label": "Создать полис"}


class PolicyUpdateView(SuccessMessageMixin, UpdateView):
    model = Policy
    form_class = PolicyForm
    template_name = "insurance/model_form.html"
    success_message = "Полис обновлен."
    extra_context = {"title": "Редактировать полис", "submit_label": "Сохранить"}


class ClientListView(ListView):
    model = Client
    template_name = "insurance/client_list.html"
    context_object_name = "clients"


class ClientCreateView(SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "insurance/model_form.html"
    success_url = reverse_lazy("insurance:clients")
    success_message = "Клиент добавлен."
    extra_context = {"title": "Добавить клиента", "submit_label": "Создать клиента"}


class ClientUpdateView(SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "insurance/model_form.html"
    success_url = reverse_lazy("insurance:clients")
    success_message = "Клиент обновлен."
    extra_context = {"title": "Редактировать клиента", "submit_label": "Сохранить"}


class ProductListView(ListView):
    model = InsuranceProduct
    template_name = "insurance/product_list.html"
    context_object_name = "products"


class ProductCreateView(SuccessMessageMixin, CreateView):
    model = InsuranceProduct
    form_class = InsuranceProductForm
    template_name = "insurance/model_form.html"
    success_url = reverse_lazy("insurance:products")
    success_message = "Страховой продукт добавлен."
    extra_context = {"title": "Добавить продукт", "submit_label": "Создать продукт"}


class ProductUpdateView(SuccessMessageMixin, UpdateView):
    model = InsuranceProduct
    form_class = InsuranceProductForm
    template_name = "insurance/model_form.html"
    success_url = reverse_lazy("insurance:products")
    success_message = "Страховой продукт обновлен."
    extra_context = {"title": "Редактировать продукт", "submit_label": "Сохранить"}


class ClaimListView(ListView):
    model = Claim
    template_name = "insurance/claim_list.html"
    context_object_name = "claims"

    def get_queryset(self):
        return Claim.objects.select_related("policy", "policy__client", "policy__product")


class ClaimCreateView(SuccessMessageMixin, CreateView):
    model = Claim
    form_class = ClaimForm
    template_name = "insurance/model_form.html"
    success_url = reverse_lazy("insurance:claims")
    success_message = "Страховой случай добавлен."
    extra_context = {"title": "Добавить страховой случай", "submit_label": "Создать случай"}


class ClaimUpdateView(SuccessMessageMixin, UpdateView):
    model = Claim
    form_class = ClaimForm
    template_name = "insurance/model_form.html"
    success_url = reverse_lazy("insurance:claims")
    success_message = "Страховой случай обновлен."
    extra_context = {"title": "Редактировать страховой случай", "submit_label": "Сохранить"}
