from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from insurance.models import Claim, Client, InsuranceProduct, Policy


class Command(BaseCommand):
    help = "Заполнить базу демонстрационными данными страховой компании."

    def handle(self, *args, **options):
        clients = {
            "ivanov@example.ru": Client.objects.update_or_create(
                email="ivanov@example.ru",
                defaults={
                    "full_name": "Иванов Иван Сергеевич",
                    "phone": "+7 900 111-22-33",
                    "birth_date": date(1987, 3, 14),
                },
            )[0],
            "petrova@example.ru": Client.objects.update_or_create(
                email="petrova@example.ru",
                defaults={
                    "full_name": "Петрова Анна Викторовна",
                    "phone": "+7 901 222-33-44",
                    "birth_date": date(1992, 8, 20),
                },
            )[0],
            "sidorov@example.ru": Client.objects.update_or_create(
                email="sidorov@example.ru",
                defaults={
                    "full_name": "Сидоров Павел Андреевич",
                    "phone": "+7 902 333-44-55",
                    "birth_date": date(1979, 11, 2),
                },
            )[0],
        }

        products = {
            "Автострахование": InsuranceProduct.objects.update_or_create(
                name="Автострахование",
                defaults={
                    "description": "ОСАГО и КАСКО для физических лиц.",
                    "base_rate": Decimal("4.80"),
                },
            )[0],
            "Имущество": InsuranceProduct.objects.update_or_create(
                name="Имущество",
                defaults={
                    "description": "Защита квартиры, дома и домашнего имущества.",
                    "base_rate": Decimal("1.35"),
                },
            )[0],
            "Здоровье": InsuranceProduct.objects.update_or_create(
                name="Здоровье",
                defaults={
                    "description": "Добровольное медицинское страхование.",
                    "base_rate": Decimal("3.20"),
                },
            )[0],
        }

        policies = {
            "OSAGO-2026-001": Policy.objects.update_or_create(
                number="OSAGO-2026-001",
                defaults={
                    "client": clients["ivanov@example.ru"],
                    "product": products["Автострахование"],
                    "start_date": date(2026, 1, 1),
                    "end_date": date(2026, 12, 31),
                    "premium": Decimal("14500.00"),
                    "insured_amount": Decimal("500000.00"),
                    "status": Policy.Status.ACTIVE,
                },
            )[0],
            "HOME-2026-014": Policy.objects.update_or_create(
                number="HOME-2026-014",
                defaults={
                    "client": clients["ivanov@example.ru"],
                    "product": products["Имущество"],
                    "start_date": date(2026, 2, 10),
                    "end_date": date(2027, 2, 9),
                    "premium": Decimal("22000.00"),
                    "insured_amount": Decimal("2500000.00"),
                    "status": Policy.Status.ACTIVE,
                },
            )[0],
            "HEALTH-2026-019": Policy.objects.update_or_create(
                number="HEALTH-2026-019",
                defaults={
                    "client": clients["petrova@example.ru"],
                    "product": products["Здоровье"],
                    "start_date": date(2026, 1, 15),
                    "end_date": date(2027, 1, 14),
                    "premium": Decimal("38000.00"),
                    "insured_amount": Decimal("1200000.00"),
                    "status": Policy.Status.ACTIVE,
                },
            )[0],
            "TRAVEL-OLD-009": Policy.objects.update_or_create(
                number="TRAVEL-OLD-009",
                defaults={
                    "client": clients["sidorov@example.ru"],
                    "product": products["Автострахование"],
                    "start_date": date(2025, 1, 1),
                    "end_date": date(2025, 12, 31),
                    "premium": Decimal("17200.00"),
                    "insured_amount": Decimal("700000.00"),
                    "status": Policy.Status.EXPIRED,
                },
            )[0],
        }

        Claim.objects.update_or_create(
            policy=policies["OSAGO-2026-001"],
            claim_date=date(2026, 2, 12),
            defaults={
                "description": "Повреждение бампера после ДТП.",
                "amount": Decimal("47000.00"),
                "status": Claim.Status.PAID,
            },
        )
        Claim.objects.update_or_create(
            policy=policies["HOME-2026-014"],
            claim_date=date(2026, 3, 22),
            defaults={
                "description": "Затопление кухни.",
                "amount": Decimal("135000.00"),
                "status": Claim.Status.APPROVED,
            },
        )
        Claim.objects.update_or_create(
            policy=policies["HEALTH-2026-019"],
            claim_date=date(2026, 4, 2),
            defaults={
                "description": "Амбулаторное лечение.",
                "amount": Decimal("27000.00"),
                "status": Claim.Status.IN_REVIEW,
            },
        )

        self.stdout.write(self.style.SUCCESS("Демонстрационные данные загружены."))

