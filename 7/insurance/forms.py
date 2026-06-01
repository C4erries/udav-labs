from django import forms

from insurance.models import Claim, Client, InsuranceProduct, Policy


DATE_INPUT = forms.DateInput(attrs={"type": "date"})
FIELD_CLASS = (
    "rounded-2xl border border-stone-200 bg-white px-4 py-3 text-brand-ink "
    "outline-none ring-brand-clay/20 transition focus:ring-4"
)


class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_class} {FIELD_CLASS}".strip()


class ClientForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ("full_name", "phone", "email", "birth_date")
        widgets = {"birth_date": DATE_INPUT}


class InsuranceProductForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = InsuranceProduct
        fields = ("name", "description", "base_rate")


class PolicyForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Policy
        fields = (
            "client",
            "product",
            "number",
            "start_date",
            "end_date",
            "premium",
            "insured_amount",
            "status",
        )
        widgets = {
            "start_date": DATE_INPUT,
            "end_date": DATE_INPUT,
        }


class ClaimForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Claim
        fields = ("policy", "claim_date", "description", "amount", "status")
        widgets = {"claim_date": DATE_INPUT}
