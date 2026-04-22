import json
from typing import Any

from app.infrastructure.repositories import InsuranceRepository


class InsuranceService:
    """Application use-cases for the insurance company."""

    def __init__(self, repository: InsuranceRepository) -> None:
        self.repository = repository

    def list_clients(self) -> list[dict[str, Any]]:
        return self.repository.list_clients()

    def list_policies(self) -> list[dict[str, Any]]:
        return self.repository.list_policies()

    def list_claims(self) -> list[dict[str, Any]]:
        return self.repository.list_claims()

    def create_client(self, data: dict[str, Any]) -> dict[str, Any]:
        return self.repository.create_client(data)

    def create_policy(self, data: dict[str, Any]) -> dict[str, Any]:
        return self.repository.create_policy(data)

    def create_claim(self, data: dict[str, Any]) -> dict[str, Any]:
        return self.repository.create_claim(data)

    def get_statistics(self) -> dict[str, list[dict[str, Any]]]:
        return self.repository.get_statistics()

    def export_table_to_json(self, table_name: str) -> str:
        rows = self.repository.export_table(table_name)
        return json.dumps(rows, ensure_ascii=False, indent=2)

    def import_table_from_json(self, table_name: str, content: str) -> int:
        rows = json.loads(content)
        if not isinstance(rows, list):
            raise ValueError("JSON должен быть массивом объектов.")
        if not all(isinstance(row, dict) for row in rows):
            raise ValueError("Каждый элемент JSON-массива должен быть объектом.")
        return self.repository.import_table(table_name, rows)

