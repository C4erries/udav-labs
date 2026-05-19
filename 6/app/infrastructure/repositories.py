from typing import Any

from app.infrastructure.database import get_connection


ALLOWED_TABLES = {"clients", "policies", "claims"}


class InsuranceRepository:
    def list_clients(self) -> list[dict[str, Any]]:
        query = """
            SELECT id, full_name, phone, email, birth_date
            FROM clients
            ORDER BY id
        """
        return self._fetch_all(query)

    def list_policies(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                p.id,
                p.client_id,
                c.full_name AS client_name,
                p.policy_number,
                p.product_type,
                p.start_date,
                p.end_date,
                p.premium,
                p.insured_amount
            FROM policies p
            JOIN clients c ON c.id = p.client_id
            ORDER BY p.id
        """
        return self._fetch_all(query)

    def list_claims(self) -> list[dict[str, Any]]:
        query = """
            SELECT
                cl.id,
                cl.policy_id,
                p.policy_number,
                c.full_name AS client_name,
                cl.claim_date,
                cl.description,
                cl.amount,
                cl.status
            FROM claims cl
            JOIN policies p ON p.id = cl.policy_id
            JOIN clients c ON c.id = p.client_id
            ORDER BY cl.id
        """
        return self._fetch_all(query)

    def create_client(self, data: dict[str, Any]) -> dict[str, Any]:
        query = """
            INSERT INTO clients (full_name, phone, email, birth_date)
            VALUES (:full_name, :phone, :email, :birth_date)
        """
        client_id = self._insert(query, data)
        return self._fetch_one("SELECT * FROM clients WHERE id = ?", (client_id,))

    def create_policy(self, data: dict[str, Any]) -> dict[str, Any]:
        query = """
            INSERT INTO policies (
                client_id,
                policy_number,
                product_type,
                start_date,
                end_date,
                premium,
                insured_amount
            )
            VALUES (
                :client_id,
                :policy_number,
                :product_type,
                :start_date,
                :end_date,
                :premium,
                :insured_amount
            )
        """
        policy_id = self._insert(query, data)
        return self._fetch_one("SELECT * FROM policies WHERE id = ?", (policy_id,))

    def create_claim(self, data: dict[str, Any]) -> dict[str, Any]:
        query = """
            INSERT INTO claims (
                policy_id,
                claim_date,
                description,
                amount,
                status
            )
            VALUES (
                :policy_id,
                :claim_date,
                :description,
                :amount,
                :status
            )
        """
        claim_id = self._insert(query, data)
        return self._fetch_one("SELECT * FROM claims WHERE id = ?", (claim_id,))

    def get_statistics(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "policies_by_product": self._fetch_all(
                """
                SELECT
                    product_type,
                    COUNT(*) AS policies_count,
                    ROUND(SUM(premium), 2) AS total_premium,
                    ROUND(SUM(insured_amount), 2) AS total_insured_amount
                FROM policies
                GROUP BY product_type
                ORDER BY total_premium DESC
                """
            ),
            "client_portfolio": self._fetch_all(
                """
                SELECT
                    c.id,
                    c.full_name,
                    COUNT(p.id) AS policies_count,
                    COALESCE(ROUND(SUM(p.premium), 2), 0) AS total_premium
                FROM clients c
                LEFT JOIN policies p ON p.client_id = c.id
                GROUP BY c.id, c.full_name
                ORDER BY total_premium DESC
                """
            ),
            "claims_by_status": self._fetch_all(
                """
                SELECT
                    status,
                    COUNT(*) AS claims_count,
                    ROUND(SUM(amount), 2) AS total_claim_amount
                FROM claims
                GROUP BY status
                ORDER BY total_claim_amount DESC
                """
            ),
            "loss_ratio_by_product": self._fetch_all(
                """
                SELECT
                    p.product_type,
                    ROUND(SUM(COALESCE(policy_claims.total_claims, 0)), 2) AS total_claims,
                    ROUND(SUM(p.premium), 2) AS total_premium,
                    ROUND(
                        SUM(COALESCE(policy_claims.total_claims, 0)) * 100.0 / SUM(p.premium),
                        2
                    ) AS loss_ratio_percent
                FROM policies p
                LEFT JOIN (
                    SELECT policy_id, SUM(amount) AS total_claims
                    FROM claims
                    GROUP BY policy_id
                ) policy_claims ON policy_claims.policy_id = p.id
                GROUP BY p.product_type
                ORDER BY loss_ratio_percent DESC
                """
            ),
        }

    def export_table(self, table_name: str) -> list[dict[str, Any]]:
        self._validate_table_name(table_name)
        return self._fetch_all(f"SELECT * FROM {table_name} ORDER BY id")

    def import_table(self, table_name: str, rows: list[dict[str, Any]]) -> int:
        self._validate_table_name(table_name)
        creators = {
            "clients": self.create_client,
            "policies": self.create_policy,
            "claims": self.create_claim,
        }

        inserted = 0
        for row in rows:
            clean_row = {key: value for key, value in row.items() if key != "id"}
            creators[table_name](clean_row)
            inserted += 1
        return inserted

    def _validate_table_name(self, table_name: str) -> None:
        if table_name not in ALLOWED_TABLES:
            allowed = ", ".join(sorted(ALLOWED_TABLES))
            raise ValueError(f"Неизвестная таблица '{table_name}'. Доступны: {allowed}.")

    def _fetch_all(
        self,
        query: str,
        parameters: tuple[Any, ...] | dict[str, Any] = (),
    ) -> list[dict[str, Any]]:
        with get_connection() as connection:
            rows = connection.execute(query, parameters).fetchall()
            return [dict(row) for row in rows]

    def _fetch_one(
        self,
        query: str,
        parameters: tuple[Any, ...] | dict[str, Any] = (),
    ) -> dict[str, Any]:
        with get_connection() as connection:
            row = connection.execute(query, parameters).fetchone()
            if row is None:
                raise LookupError("Запись не найдена.")
            return dict(row)

    def _insert(self, query: str, data: dict[str, Any]) -> int:
        with get_connection() as connection:
            cursor = connection.execute(query, data)
            connection.commit()
            return int(cursor.lastrowid)
