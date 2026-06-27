from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PageRegistry:
    def __init__(self, path: str):
        self.path = Path(path)

    def list_pages(self) -> list[dict[str, Any]]:
        return [self._public_page(page) for page in self._load_pages()]

    def get_page(self, page_id: str | None = None, page_name: str | None = None) -> dict[str, Any] | None:
        pages = self._load_pages()
        if page_id:
            for page in pages:
                if str(page.get("id")) == str(page_id):
                    return page
        if page_name:
            normalized = page_name.strip().lower()
            for page in pages:
                if str(page.get("name", "")).strip().lower() == normalized:
                    return page
        return None

    def resolve_page(
        self,
        page_id: str | None = None,
        page_name: str | None = None,
        fallback_page_id: str | None = None,
        fallback_access_token: str | None = None,
    ) -> dict[str, Any] | None:
        page = self.get_page(page_id=page_id, page_name=page_name)
        if page:
            return page
        if fallback_page_id and fallback_access_token and not page_id and not page_name:
            return {
                "id": fallback_page_id,
                "name": fallback_page_id,
                "access_token": fallback_access_token,
                "tasks": [],
            }
        return None

    def _load_pages(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            pages = data
        elif isinstance(data, dict):
            pages = data.get("pages") or data.get("data") or []
        else:
            pages = []

        return [page for page in pages if isinstance(page, dict) and page.get("id") and page.get("access_token")]

    def _public_page(self, page: dict[str, Any]) -> dict[str, Any]:
        tasks = page.get("tasks", [])
        return {
            "id": page.get("id"),
            "name": page.get("name"),
            "tasks": tasks,
            "can_publish": "CREATE_CONTENT" in tasks or "MANAGE" in tasks,
        }
