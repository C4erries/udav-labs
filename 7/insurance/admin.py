from django.contrib import admin

from insurance.models import Claim, Client, InsuranceProduct, Policy


admin.site.site_header = "Страховая компания"
admin.site.site_title = "Страховая компания"
admin.site.index_title = "Панель управления страховой компанией"


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email", "birth_date")
    list_filter = ("birth_date",)
    search_fields = ("full_name", "phone", "email")
    date_hierarchy = "birth_date"


@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = ("name", "base_rate")
    search_fields = ("name", "description")


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "client",
        "product",
        "status",
        "start_date",
        "end_date",
        "premium",
        "insured_amount",
    )
    list_filter = ("status", "product", "start_date", "end_date")
    list_select_related = ("client", "product")
    search_fields = ("number", "client__full_name", "client__email", "product__name")
    date_hierarchy = "start_date"


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        "policy",
        "client_name",
        "status",
        "claim_date",
        "amount",
    )
    list_filter = ("status", "claim_date", "policy__product")
    list_select_related = ("policy", "policy__client", "policy__product")
    search_fields = ("policy__number", "policy__client__full_name", "description")
    date_hierarchy = "claim_date"

    @admin.display(description="Клиент")
    def client_name(self, obj: Claim) -> str:
        return obj.policy.client.full_name
