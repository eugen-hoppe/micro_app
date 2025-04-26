from __future__ import annotations

DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"
PREFIX = "/api"
CORS_ORIGINS: list[str] = ["*"]  # adjust for production
