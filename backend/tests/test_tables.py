import asyncio
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx

from app.config import Settings
from app.iiko import IikoClient
from app.tables import TablesService, build_tables, demo_tables

NOW = datetime(2026, 10, 28, 19, 0)

SECTIONS = [{
    "id": "sec-1", "name": "Зал",
    "tables": [
        {"id": "t1", "number": 1, "name": "Стол 1", "seatingCapacity": 4},
        {"id": "t2", "number": 2, "name": "Стол 2", "seatingCapacity": 4},
        {"id": "t3", "number": 3, "name": "Стол 3", "seatingCapacity": 6},
        {"id": "t4", "number": 4, "name": "Стол 4", "seatingCapacity": 2},
        {"id": "t5", "number": 5, "seatingCapacity": 2, "isDeleted": True},
    ],
}]


def settings(**kw) -> Settings:
    base = dict(api_login="", app_id="", client_secret="", organization_id="", terminal_group_id="", tz=ZoneInfo("Europe/Moscow"),
                reserve_ahead_minutes=120, cache_seconds=30, cors_origins=[])
    return Settings(**{**base, **kw})


def by_number(tables):
    return {t.number: t for t in tables}


def test_statuses():
    orders = [{"id": "o1", "order": {"tableIds": ["t1"], "status": "New"}}]
    reserves = [
        {"id": "r1", "tableIds": ["t2"], "estimatedStartTime": "2026-10-28 20:30:00.000", "durationInMinutes": 120},
        {"id": "r2", "tableIds": ["t3"], "estimatedStartTime": "2026-10-28 23:30:00.000", "durationInMinutes": 120},  # позже горизонта
        {"id": "r3", "tableIds": ["t1"], "estimatedStartTime": "2026-10-28 19:30:00.000", "durationInMinutes": 60},
    ]
    t = by_number(build_tables(SECTIONS, orders, reserves, NOW, 120))
    assert t[1].status == "busy"  # заказ важнее брони
    assert t[2].status == "reserved" and t[2].reserved_at == "20:30"
    assert t[3].status == "free"
    assert t[4].status == "free"
    assert 5 not in t  # удалённые столы не показываем


def test_reserve_in_progress_and_finished():
    reserves = [
        {"tableIds": ["t1"], "estimatedStartTime": "2026-10-28T18:00:00", "durationInMinutes": 120},  # идёт сейчас
        {"tableIds": ["t2"], "estimatedStartTime": "2026-10-28 16:00:00.000", "durationInMinutes": 120},  # уже закончилась
    ]
    t = by_number(build_tables(SECTIONS, [], reserves, NOW, 120))
    assert t[1].status == "reserved"
    assert t[2].status == "free"


def test_demo_has_all_statuses_shape():
    tables = demo_tables(NOW)
    assert len(tables) == 12
    assert {t.status for t in tables} <= {"free", "busy", "reserved"}
    assert all(t.reserved_at for t in tables if t.status == "reserved")


def fake_iiko(calls: list[str], fail: bool = False) -> httpx.AsyncClient:
    """Подменяет iiko: отвечает на нужные методы, считает вызовы."""
    def handler(req: httpx.Request) -> httpx.Response:
        path = req.url.path
        calls.append(path)
        if fail and path != "/api/1/access_token":
            return httpx.Response(500, text="boom")
        body = json.loads(req.content or b"{}")
        match path:
            case "/api/1/access_token":
                assert body == {"apiLogin": "key"}
                return httpx.Response(200, json={"token": "tok"})
            case "/api/v2/access_token":
                assert body == {"apiKey": "key", "appId": "app", "clientSecret": "secret"}
                return httpx.Response(200, json={"token": "tok"})
            case "/api/1/organizations":
                return httpx.Response(200, json={"organizations": [{"id": "org", "name": "Шах"}]})
            case "/api/1/terminal_groups":
                return httpx.Response(200, json={"terminalGroups": [{"organizationId": "org", "items": [{"id": "tg"}]}]})
            case "/api/1/reserve/available_restaurant_sections":
                assert body["terminalGroupIds"] == ["tg"]
                return httpx.Response(200, json={"restaurantSections": SECTIONS})
            case "/api/1/order/by_table":
                assert req.headers["Authorization"] == "Bearer tok"
                return httpx.Response(200, json={"orders": [{"order": {"tableIds": ["t3"]}}]})
            case "/api/1/reserve/restaurant_sections_workload":
                return httpx.Response(200, json={"reserves": []})
        return httpx.Response(404)
    return httpx.AsyncClient(base_url="https://iiko.test", transport=httpx.MockTransport(handler))


def test_service_with_iiko_and_cache():
    async def run():
        calls: list[str] = []
        svc = TablesService(settings(api_login="key"), IikoClient("key", fake_iiko(calls)))
        first = await svc.get()
        second = await svc.get()
        await svc.close()
        return first, second, calls

    first, second, calls = asyncio.run(run())
    assert first["demo"] is False
    assert {t["number"]: t["status"] for t in first["tables"]} == {1: "free", 2: "free", 3: "busy", 4: "free"}
    assert second is first  # второй запрос из кеша
    assert calls.count("/api/1/access_token") == 1
    assert calls.count("/api/1/order/by_table") == 1


def test_service_keeps_last_data_when_iiko_fails():
    async def run():
        calls: list[str] = []
        svc = TablesService(settings(api_login="key", cache_seconds=0), IikoClient("key", fake_iiko(calls)))
        ok = await svc.get()
        svc.client.http = fake_iiko(calls, fail=True)
        again = await svc.get()
        await svc.close()
        return ok, again

    ok, again = asyncio.run(run())
    assert again["stale"] is True
    assert again["tables"] == ok["tables"]


def test_v2_auth_with_app_credentials():
    async def run():
        calls: list[str] = []
        client = IikoClient("key", fake_iiko(calls), app_id="app", client_secret="secret")
        orgs = await client.organizations()
        await client.close()
        return orgs, calls

    orgs, calls = asyncio.run(run())
    assert orgs[0]["id"] == "org"
    assert "/api/v2/access_token" in calls and "/api/1/access_token" not in calls
