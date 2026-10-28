# Клиент iikoCloud API: https://api-ru.iiko.services/docs
# Все методы — POST с JSON, авторизация токеном, который выдаётся по apiLogin и живёт около часа.
import time
from datetime import datetime

import httpx

BASE_URL = "https://api-ru.iiko.services"
TOKEN_TTL = 45 * 60  # обновляем заранее, не дожидаясь, пока iiko его отзовёт


class IikoError(Exception):
    pass


def iiko_time(dt: datetime) -> str:
    """Формат времени, который ждёт iiko: 2026-10-28 20:00:00.000"""
    return dt.strftime("%Y-%m-%d %H:%M:%S.") + f"{dt.microsecond // 1000:03d}"


class IikoClient:
    def __init__(self, api_login: str, http: httpx.AsyncClient | None = None):
        self.api_login = api_login
        self.http = http or httpx.AsyncClient(base_url=BASE_URL, timeout=20)
        self._token = ""
        self._token_at = 0.0

    async def close(self) -> None:
        await self.http.aclose()

    async def _auth(self) -> str:
        if not self._token or time.monotonic() - self._token_at > TOKEN_TTL:
            r = await self.http.post("/api/1/access_token", json={"apiLogin": self.api_login})
            if r.status_code != 200:
                raise IikoError(f"iiko не выдал токен: {r.status_code} {r.text[:200]}")
            self._token = r.json()["token"]
            self._token_at = time.monotonic()
        return self._token

    async def call(self, path: str, body: dict) -> dict:
        for attempt in range(2):
            token = await self._auth()
            r = await self.http.post(path, json=body, headers={"Authorization": f"Bearer {token}"})
            if r.status_code == 401 and attempt == 0:
                self._token = ""  # токен протух раньше срока — берём новый и повторяем
                continue
            if r.status_code != 200:
                raise IikoError(f"{path}: {r.status_code} {r.text[:300]}")
            return r.json()
        raise IikoError(f"{path}: нет доступа")

    # --- справочники ---

    async def organizations(self) -> list[dict]:
        data = await self.call("/api/1/organizations", {"returnAdditionalInfo": False})
        return data.get("organizations", [])

    async def terminal_groups(self, organization_id: str) -> list[dict]:
        data = await self.call("/api/1/terminal_groups", {"organizationIds": [organization_id]})
        return [tg for group in data.get("terminalGroups", []) for tg in group.get("items", [])]

    async def sections(self, terminal_group_id: str) -> list[dict]:
        """Залы со столами: номер, название, количество мест."""
        data = await self.call(
            "/api/1/reserve/available_restaurant_sections",
            {"terminalGroupIds": [terminal_group_id], "returnSchema": False},
        )
        return data.get("restaurantSections", [])

    # --- что происходит сейчас ---

    async def reserves(self, section_ids: list[str], date_from: datetime, date_to: datetime) -> list[dict]:
        """Брони на столы за период (модуль резервов iiko)."""
        data = await self.call(
            "/api/1/reserve/restaurant_sections_workload",
            {"restaurantSectionIds": section_ids, "dateFrom": iiko_time(date_from), "dateTo": iiko_time(date_to)},
        )
        return data.get("reserves", [])

    async def open_orders(self, organization_id: str, table_ids: list[str]) -> list[dict]:
        """Открытые заказы на столах: если на столе есть заказ, он занят."""
        data = await self.call(
            "/api/1/order/by_table",
            {"organizationIds": [organization_id], "tableIds": table_ids, "statuses": ["New", "Bill"]},
        )
        return data.get("orders", [])
