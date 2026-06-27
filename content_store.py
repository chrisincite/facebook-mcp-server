from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


class ContentStore:
    def __init__(self, path: str):
        self.path = Path(path)

    def create_draft(self, draft: dict[str, Any]) -> dict[str, Any]:
        data = self._load()
        now = self._now()
        draft_id = f"draft_{uuid4().hex[:12]}"
        record = {
            "id": draft_id,
            "status": "draft",
            "created_at": now,
            "updated_at": now,
            "approved_at": None,
            "published_at": None,
            **draft,
        }
        data["drafts"].append(record)
        self._save(data)
        return record

    def list_drafts(self, status: str | None = None) -> list[dict[str, Any]]:
        drafts = self._load()["drafts"]
        if status:
            drafts = [draft for draft in drafts if draft.get("status") == status]
        return sorted(drafts, key=lambda draft: draft.get("updated_at", ""), reverse=True)

    def get_draft(self, draft_id: str) -> dict[str, Any] | None:
        for draft in self._load()["drafts"]:
            if draft.get("id") == draft_id:
                return draft
        return None

    def update_draft(self, draft_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        data = self._load()
        for draft in data["drafts"]:
            if draft.get("id") == draft_id:
                draft.update(updates)
                draft["updated_at"] = self._now()
                self._save(data)
                return draft
        raise ValueError(f"Draft not found: {draft_id}")

    def add_performance_snapshot(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        data = self._load()
        record = {
            "id": f"perf_{uuid4().hex[:12]}",
            "created_at": self._now(),
            **snapshot,
        }
        data["performance_snapshots"].append(record)
        self._save(data)
        return record

    def list_performance_snapshots(self) -> list[dict[str, Any]]:
        snapshots = self._load()["performance_snapshots"]
        return sorted(snapshots, key=lambda item: item.get("created_at", ""), reverse=True)

    def _load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"drafts": [], "performance_snapshots": []}

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        data.setdefault("drafts", [])
        data.setdefault("performance_snapshots", [])
        return data

    def _save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write("\n")

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
