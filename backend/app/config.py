# Настройки берутся из переменных окружения или файла backend/.env
import os
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# сайт при разработке; на сервере сайт и API на одном домене, CORS там не нужен
DEV_ORIGINS = "http://localhost:3000,http://127.0.0.1:3000"


@dataclass(frozen=True)
class Settings:
    api_login: str
    app_id: str
    client_secret: str
    organization_id: str
    terminal_group_id: str
    tz: ZoneInfo
    reserve_ahead_minutes: int
    cache_seconds: int
    cors_origins: list[str]
    force_demo: bool = False
    # залы из iiko, которые гостям не показываем (виртуальные «На вынос», «Доставка»)
    hide_sections: tuple[str, ...] = ()

    @property
    def demo(self) -> bool:
        """Без ключа iiko (или с DEMO=1) отдаём тестовые данные, чтобы можно было делать сайт."""
        return self.force_demo or not self.api_login


def load_settings() -> Settings:
    env = os.environ.get
    return Settings(
        api_login=env("IIKO_API_LOGIN", "").strip(),
        app_id=env("IIKO_APP_ID", "").strip(),
        client_secret=env("IIKO_CLIENT_SECRET", "").strip(),
        organization_id=env("IIKO_ORGANIZATION_ID", "").strip(),
        terminal_group_id=env("IIKO_TERMINAL_GROUP_ID", "").strip(),
        tz=ZoneInfo(env("TIMEZONE", "Europe/Moscow")),
        reserve_ahead_minutes=int(env("RESERVE_AHEAD_MINUTES", "120")),
        cache_seconds=int(env("CACHE_SECONDS", "10")),
        cors_origins=[o.strip() for o in env("CORS_ORIGINS", DEV_ORIGINS).split(",") if o.strip()],
        force_demo=env("DEMO", "") == "1",
        hide_sections=tuple(n.strip().lower() for n in env("IIKO_HIDE_SECTIONS", "На вынос,Доставка").split(",") if n.strip()),
    )
