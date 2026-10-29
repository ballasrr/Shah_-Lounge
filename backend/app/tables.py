# Статусы столов для сайта: свободен / занят / забронирован.
# Наружу отдаём только номер, зал, места и статус — ни имён гостей, ни сумм.
import asyncio
import random
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Literal

from .config import Settings
from .iiko import IikoClient, IikoError

Status = Literal["free", "busy", "reserved"]

SECTIONS_TTL = 10 * 60  # залы и столы меняются редко


@dataclass
class Table:
    id: str
    number: int
    name: str
    seats: int
    section: str
    status: Status
    reserved_at: str | None = None  # «20:00», если стол забронирован


def parse_time(value: str) -> datetime:
    """iiko отдаёт «2026-10-28 20:00:00.000», иногда через «T»."""
    return datetime.fromisoformat(value.replace(" ", "T"))


def build_tables(sections: list[dict], orders: list[dict], reserves: list[dict], now: datetime, ahead_minutes: int) -> list[Table]:
    """Сводит залы, открытые заказы и брони в список столов со статусами. now — местное время без зоны."""
    busy: set[str] = set()
    for o in orders:
        busy.update((o.get("order") or o).get("tableIds") or [])

    # ближайшая бронь на каждый стол: идёт сейчас или начнётся в ближайшие ahead_minutes
    reserved: dict[str, datetime] = {}
    horizon = now + timedelta(minutes=ahead_minutes)
    for r in reserves:
        start_raw = r.get("estimatedStartTime")
        if not start_raw:
            continue
        start = parse_time(start_raw)
        end = start + timedelta(minutes=r.get("durationInMinutes") or 120)
        if start <= horizon and end > now:
            for tid in r.get("tableIds") or []:
                if tid not in reserved or start < reserved[tid]:
                    reserved[tid] = start

    tables: list[Table] = []
    for s in sections:
        for t in s.get("tables") or []:
            if t.get("isDeleted"):
                continue
            tid = t["id"]
            status: Status = "busy" if tid in busy else "reserved" if tid in reserved else "free"
            tables.append(Table(
                id=tid,
                number=t.get("number") or 0,
                name=t.get("name") or f"Стол {t.get('number')}",
                seats=t.get("seatingCapacity") or 0,
                section=s.get("name") or "",
                status=status,
                reserved_at=reserved[tid].strftime("%H:%M") if status == "reserved" else None,
            ))
    tables.sort(key=lambda t: (t.section, t.number))
    return tables


def demo_tables(now: datetime) -> list[Table]:
    """Тестовый зал. Статусы меняются раз в 5 минут, чтобы на сайте было видно обновление."""
    layout = [("Зал", n, 4) for n in range(1, 7)] + [("Кабинки", n, 6) for n in range(7, 11)] + [("VIP", 11, 8), ("VIP", 12, 10)]
    rnd = random.Random(now.strftime("%Y%m%d%H") + str(now.minute // 5))
    tables = []
    for section, number, seats in layout:
        status: Status = rnd.choices(["free", "busy", "reserved"], weights=[5, 3, 2])[0]
        at = (now + timedelta(minutes=rnd.choice([30, 60, 90]))).strftime("%H:00") if status == "reserved" else None
        tables.append(Table(f"demo-{number}", number, f"Стол {number}", seats, section, status, at))
    return tables


class TablesService:
    def __init__(self, settings: Settings, client: IikoClient | None = None):
        self.s = settings
        self.client = client or (None if settings.demo else IikoClient(settings.api_login, app_id=settings.app_id, client_secret=settings.client_secret))
        self._lock = asyncio.Lock()
        self._cache: dict | None = None
        self._cache_at = 0.0
        self._sections: list[dict] = []
        self._sections_at = 0.0
        self._org_id = settings.organization_id
        self._tg_id = settings.terminal_group_id

    async def close(self) -> None:
        if self.client:
            await self.client.close()

    def _now(self) -> datetime:
        return datetime.now(self.s.tz).replace(tzinfo=None)

    async def _ids(self) -> tuple[str, str]:
        """Организация и группа терминалов: из настроек или первые доступные ключу."""
        assert self.client
        if not self._org_id:
            orgs = await self.client.organizations()
            if not orgs:
                raise IikoError("Ключу не доступна ни одна организация")
            self._org_id = orgs[0]["id"]
        if not self._tg_id:
            groups = await self.client.terminal_groups(self._org_id)
            if not groups:
                raise IikoError("В организации нет групп терминалов")
            self._tg_id = groups[0]["id"]
        return self._org_id, self._tg_id

    async def _fetch(self) -> list[Table]:
        now = self._now()
        if self.s.demo:
            return demo_tables(now)
        assert self.client
        org_id, tg_id = await self._ids()
        if not self._sections or time.monotonic() - self._sections_at > SECTIONS_TTL:
            hidden = self.s.hide_sections
            self._sections = [s for s in await self.client.sections(tg_id) if (s.get("name") or "").strip().lower() not in hidden]
            self._sections_at = time.monotonic()
        section_ids = [s["id"] for s in self._sections]
        table_ids = [t["id"] for s in self._sections for t in s.get("tables") or []]
        orders, reserves = await asyncio.gather(
            self.client.open_orders(org_id, table_ids) if table_ids else asyncio.sleep(0, []),
            self.client.reserves(section_ids, now - timedelta(hours=6), now + timedelta(hours=12)) if section_ids else asyncio.sleep(0, []),
        )
        return build_tables(self._sections, orders, reserves, now, self.s.reserve_ahead_minutes)

    async def get(self) -> dict:
        """Ответ для сайта. Кешируется, чтобы не дёргать iiko на каждого посетителя.
        Если iiko не ответил — отдаём последние данные с пометкой stale."""
        async with self._lock:
            if self._cache and time.monotonic() - self._cache_at < self.s.cache_seconds:
                return self._cache
            try:
                tables = await self._fetch()
            except Exception as e:  # noqa: BLE001 — сайт не должен падать из-за iiko
                if self._cache:
                    return {**self._cache, "stale": True}
                raise IikoError(str(e)) from e
            self._cache = {
                "updatedAt": self._now().strftime("%H:%M"),
                "demo": self.s.demo,
                "stale": False,
                "tables": [asdict(t) for t in tables],
            }
            self._cache_at = time.monotonic()
            return self._cache
