from django.db import models
from django.urls import reverse


class Client(models.Model):
    full_name = models.CharField("ФИО", max_length=160)
    phone = models.CharField("Телефон", max_length=32)
    email = models.EmailField("Email", unique=True)
    birth_date = models.DateField("Дата рождения")

    class Meta:
        ordering = ["full_name"]
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self) -> str:
        return reverse("insurance:clients")


class InsuranceProduct(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    description = models.TextField("Описание", blank=True)
    base_rate = models.DecimalField("Базовая ставка, %", max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["name"]
        verbose_name = "страховой продукт"
        verbose_name_plural = "страховые продукты"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("insurance:products")


class Policy(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Активен"
        EXPIRED = "expired", "Истек"
        CANCELLED = "cancelled", "Расторгнут"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="policies",
        verbose_name="Клиент",
    )
    product = models.ForeignKey(
        InsuranceProduct,
        on_delete=models.PROTECT,
        related_name="policies",
        verbose_name="Продукт",
    )
    number = models.CharField("Номер полиса", max_length=40, unique=True)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата окончания")
    premium = models.DecimalField("Страховая премия", max_digits=12, decimal_places=2)
    insured_amount = models.DecimalField("Страховая сумма", max_digits=14, decimal_places=2)
    status = models.CharField(
        "Статус",
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "number"]
        verbose_name = "полис"
        verbose_name_plural = "полисы"

    def __str__(self) -> str:
        return f"{self.number} - {self.client}"

    def get_absolute_url(self) -> str:
        return reverse("insurance:policy-detail", kwargs={"pk": self.pk})


class Claim(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        IN_REVIEW = "in_review", "На рассмотрении"
        APPROVED = "approved", "Одобрен"
        REJECTED = "rejected", "Отклонен"
        PAID = "paid", "Выплачен"

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name="claims",
        verbose_name="Полис",
    )
    claim_date = models.DateField("Дата случая")
    description = models.TextField("Описание")
    amount = models.DecimalField("Сумма ущерба", max_digits=12, decimal_places=2)
    status = models.CharField(
        "Статус",
        max_length=16,
        choices=Status.choices,
        default=Status.NEW,
    )

    class Meta:
        ordering = ["-claim_date"]
        verbose_name = "страховой случай"
        verbose_name_plural = "страховые случаи"

    def __str__(self) -> str:
        return f"{self.policy.number}: {self.amount}"

    def get_absolute_url(self) -> str:
        return reverse("insurance:claims")

# Create your models here.
