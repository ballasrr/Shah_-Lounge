# Проверка ключа iiko: что ему доступно и как выглядят данные.
#   python -m app.discover
# Печатает организации, группы терминалов, залы и столы — ID оттуда кладутся в .env.
import asyncio
import json
from datetime import datetime, timedelta

from .config import load_settings
from .iiko import IikoClient


async def main() -> None:
    s = load_settings()
    if s.demo:
        print("IIKO_API_LOGIN не задан в backend/.env — проверять нечего.")
        return
    client = IikoClient(s.api_login)
    try:
        orgs = await client.organizations()
        print(f"Организаций: {len(orgs)}")
        for org in orgs:
            print(f"\n=== {org.get('name')}  IIKO_ORGANIZATION_ID={org['id']}")
            for tg in await client.terminal_groups(org["id"]):
                print(f"  группа терминалов: {tg.get('name')}  IIKO_TERMINAL_GROUP_ID={tg['id']}")
                sections = await client.sections(tg["id"])
                for sec in sections:
                    tables = [t for t in sec.get("tables") or [] if not t.get("isDeleted")]
                    print(f"    зал «{sec.get('name')}»: {len(tables)} столов")
                    for t in tables:
                        print(f"      №{t.get('number')} {t.get('name') or ''} — мест: {t.get('seatingCapacity')}")
                if sections:
                    now = datetime.now(s.tz).replace(tzinfo=None)
                    ids = [sec["id"] for sec in sections]
                    reserves = await client.reserves(ids, now - timedelta(hours=6), now + timedelta(hours=12))
                    table_ids = [t["id"] for sec in sections for t in sec.get("tables") or []]
                    orders = await client.open_orders(org["id"], table_ids)
                    print(f"    броней сегодня: {len(reserves)}, открытых заказов на столах: {len(orders)}")
                    if reserves:
                        print("    пример брони:", json.dumps(reserves[0], ensure_ascii=False)[:400])
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
