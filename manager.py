from __future__ import annotations

from typing import Any
from facebook_api import FacebookAPI
from config import CONTENT_STORE_PATH, DEFAULT_POST_STYLE, FACEBOOK_APPROVAL_TOKEN, FACEBOOK_TOKEN_JSON_FILE, PAGE_ACCESS_TOKEN, PAGE_ID
from content_store import ContentStore
from page_registry import PageRegistry


class Manager:
    def __init__(self):
        self.api = FacebookAPI()
        self.store = ContentStore(CONTENT_STORE_PATH)
        self.pages = PageRegistry(FACEBOOK_TOKEN_JSON_FILE)

    def post_to_facebook(self, message: str) -> dict[str, Any]:
        return self.api.post_message(message)

    def reply_to_comment(self, post_id: str, comment_id: str, message: str) -> dict[str, Any]:
        return self.api.reply_to_comment(comment_id, message)

    def get_page_posts(self) -> dict[str, Any]:
        return self.api.get_posts()

    def get_post_comments(self, post_id: str) -> dict[str, Any]:
        return self.api.get_comments(post_id)

    def delete_post(self, post_id: str) -> dict[str, Any]:
        return self.api.delete_post(post_id)

    def delete_comment(self, comment_id: str) -> dict[str, Any]:
        return self.api.delete_comment(comment_id)

    def hide_comment(self, comment_id: str) -> dict[str, Any]:
        return self.api.hide_comment(comment_id)

    def unhide_comment(self, comment_id: str) -> dict[str, Any]:
        return self.api.unhide_comment(comment_id)

    def delete_comment_from_post(self, post_id: str, comment_id: str) -> dict[str, Any]:
        return self.api.delete_comment(comment_id)

    def filter_negative_comments(self, comments: dict[str, Any]) -> list[dict[str, Any]]:
        keywords = ["bad", "terrible", "awful", "hate", "dislike", "problem", "issue"]
        return [c for c in comments.get("data", []) if any(k in c.get("message", "").lower() for k in keywords)]

    def get_number_of_comments(self, post_id: str) -> int:
        return len(self.api.get_comments(post_id).get("data", []))

    def get_number_of_likes(self, post_id: str) -> int:
        return self.api._request("GET", post_id, {"fields": "likes.summary(true)"}).get("likes", {}).get("summary", {}).get("total_count", 0)

    def get_post_insights(self, post_id: str) -> dict[str, Any]:
        metrics = [
            "post_impressions", "post_impressions_unique", "post_impressions_paid",
            "post_impressions_organic", "post_engaged_users", "post_clicks",
            "post_reactions_like_total", "post_reactions_love_total", "post_reactions_wow_total",
            "post_reactions_haha_total", "post_reactions_sorry_total", "post_reactions_anger_total",
        ]
        return self.api.get_bulk_insights(post_id, metrics)
    
    def get_post_impressions(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_impressions")

    def get_post_impressions_unique(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_impressions_unique")

    def get_post_impressions_paid(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_impressions_paid")

    def get_post_impressions_organic(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_impressions_organic")

    def get_post_engaged_users(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_engaged_users")

    def get_post_clicks(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_clicks")

    def get_post_reactions_like_total(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_reactions_like_total")

    def get_post_reactions_love_total(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_reactions_love_total")

    def get_post_reactions_wow_total(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_reactions_wow_total")

    def get_post_reactions_haha_total(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_reactions_haha_total")

    def get_post_reactions_sorry_total(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_reactions_sorry_total")

    def get_post_reactions_anger_total(self, post_id: str) -> dict[str, Any]:
        return self.api.get_insights(post_id, "post_reactions_anger_total")

    def get_post_top_commenters(self, post_id: str) -> list[dict[str, Any]]:
        comments = self.get_post_comments(post_id).get("data", [])
        counter = {}
        for comment in comments:
            user_id = comment.get("from", {}).get("id")
            if user_id:
                counter[user_id] = counter.get(user_id, 0) + 1
        return sorted([{"user_id": k, "count": v} for k, v in counter.items()], key=lambda x: x["count"], reverse=True)

    def post_image_to_facebook(self, image_url: str, caption: str) -> dict[str, Any]:
        return self.api.post_image_to_facebook(image_url, caption)

    def send_dm_to_user(self, user_id: str, message: str) -> dict[str, Any]:
        return self.api.send_dm_to_user(user_id, message)
    
    def update_post(self, post_id: str, new_message: str) -> dict[str, Any]:
        return self.api.update_post(post_id, new_message)

    def schedule_post(self, message: str, publish_time: int) -> dict[str, Any]:
        return self.api.schedule_post(message, publish_time)

    def get_page_fan_count(self) -> int:
        return self.api.get_page_fan_count()

    def get_post_share_count(self, post_id: str) -> int:
        return self.api.get_post_share_count(post_id)

    def get_post_reactions_breakdown(self, post_id: str) -> dict[str, Any]:
        """Return counts for all reaction types on a post."""
        metrics = [
            "post_reactions_like_total",
            "post_reactions_love_total",
            "post_reactions_wow_total",
            "post_reactions_haha_total",
            "post_reactions_sorry_total",
            "post_reactions_anger_total",
        ]
        raw = self.api.get_bulk_insights(post_id, metrics)
        results: dict[str, Any] = {}
        for item in raw.get("data", []):
            name = item.get("name")
            value = item.get("values", [{}])[0].get("value")
            results[name] = value
        return results

    def bulk_delete_comments(self, comment_ids: list[str]) -> list[dict[str, Any]]:
        """Delete multiple comments and return their results."""
        results = []
        for cid in comment_ids:
            res = self.api.delete_comment(cid)
            results.append({"comment_id": cid, "result": res})
        return results

    def bulk_hide_comments(self, comment_ids: list[str]) -> list[dict[str, Any]]:
        """Hide multiple comments and return their results."""
        results = []
        for cid in comment_ids:
            res = self.api.hide_comment(cid)
            results.append({"comment_id": cid, "result": res})
        return results

    def bulk_unhide_comments(self, comment_ids: list[str]) -> list[dict[str, Any]]:
        """Unhide multiple comments and return their results."""
        results = []
        for cid in comment_ids:
            res = self.api.unhide_comment(cid)
            results.append({"comment_id": cid, "result": res})
        return results

    def get_comment_replies(self, comment_id: str) -> dict[str, Any]:
        return self.api.get_comment_replies(comment_id)

    def get_post_permalink(self, post_id: str) -> dict[str, Any]:
        return self.api.get_post_permalink(post_id)

    def get_scheduled_posts(self) -> dict[str, Any]:
        return self.api.get_scheduled_posts()

    def get_page_info(self, page_id: str | None = None, page_name: str | None = None) -> dict[str, Any]:
        page = self._resolve_page(page_id=page_id, page_name=page_name)
        if not page:
            return {"error": "Target page not found", "available_pages": self.list_publishable_pages()}
        return self.api.get_page_info(page_id=page["id"], access_token=page["access_token"])

    def list_publishable_pages(self) -> list[dict[str, Any]]:
        return self.pages.list_pages()

    def draft_facebook_post(
        self,
        topic: str,
        source_notes: str,
        audience: str = "AI technology followers in Taiwan",
        goal: str = "explain why this matters and drive thoughtful engagement",
        style_override: str = "",
        call_to_action: str = "你怎麼看？歡迎留言討論。",
    ) -> dict[str, Any]:
        style = style_override or DEFAULT_POST_STYLE
        message = self._compose_post(topic, source_notes, audience, goal, style, call_to_action)
        return self.store.create_draft(
            {
                "type": "text_post",
                "target_page_id": None,
                "target_page_name": None,
                "topic": topic,
                "audience": audience,
                "goal": goal,
                "style": style,
                "source_notes": source_notes,
                "message": message,
                "image_url": None,
                "scheduled_publish_time": None,
                "facebook_result": None,
            }
        )

    def draft_image_post(
        self,
        topic: str,
        image_url: str,
        source_notes: str,
        audience: str = "AI technology followers in Taiwan",
        goal: str = "explain the visual and drive engagement",
        style_override: str = "",
        call_to_action: str = "你會怎麼應用這個趨勢？",
    ) -> dict[str, Any]:
        draft = self.draft_facebook_post(topic, source_notes, audience, goal, style_override, call_to_action)
        return self.store.update_draft(draft["id"], {"type": "image_post", "image_url": image_url})

    def set_draft_target_page(
        self,
        draft_id: str,
        target_page_id: str | None = None,
        target_page_name: str | None = None,
    ) -> dict[str, Any]:
        page = self._resolve_page(page_id=target_page_id, page_name=target_page_name)
        if not page:
            return {"error": "Target page not found", "available_pages": self.list_publishable_pages()}

        draft = self.store.get_draft(draft_id)
        if not draft:
            return {"error": f"Draft not found: {draft_id}"}

        return self.store.update_draft(
            draft_id,
            {
                "target_page_id": page["id"],
                "target_page_name": page.get("name"),
            },
        )

    def list_post_drafts(self, status: str | None = None) -> list[dict[str, Any]]:
        return self.store.list_drafts(status)

    def get_post_draft(self, draft_id: str) -> dict[str, Any]:
        draft = self.store.get_draft(draft_id)
        if not draft:
            return {"error": f"Draft not found: {draft_id}"}
        return draft

    def approve_post_draft(self, draft_id: str, approval_token: str) -> dict[str, Any]:
        if not self._approval_token_matches(approval_token):
            return {"error": "Invalid approval token"}

        draft = self.store.get_draft(draft_id)
        if not draft:
            return {"error": f"Draft not found: {draft_id}"}

        return self.store.update_draft(draft_id, {"status": "approved", "approved_at": self.store._now()})

    def publish_approved_post(
        self,
        draft_id: str,
        approval_token: str,
        target_page_id: str | None = None,
        target_page_name: str | None = None,
    ) -> dict[str, Any]:
        if not self._approval_token_matches(approval_token):
            return {"error": "Invalid approval token"}

        draft = self.store.get_draft(draft_id)
        if not draft:
            return {"error": f"Draft not found: {draft_id}"}
        if draft.get("status") != "approved":
            return {"error": "Draft must be approved before publishing", "draft_status": draft.get("status")}

        page = self._target_page_for_draft(draft, target_page_id, target_page_name)
        if not page:
            return {
                "error": "Choose a target page before publishing",
                "draft_id": draft_id,
                "available_pages": self.list_publishable_pages(),
            }

        if draft.get("type") == "image_post" and draft.get("image_url"):
            result = self.api.post_image_to_facebook(draft["image_url"], draft["message"], page_id=page["id"], access_token=page["access_token"])
        else:
            result = self.api.post_message(draft["message"], page_id=page["id"], access_token=page["access_token"])

        if "error" in result:
            return self.store.update_draft(
                draft_id,
                {
                    "status": "approved",
                    "last_publish_error": result["error"],
                    "facebook_result": result,
                },
            )

        return self.store.update_draft(
            draft_id,
            {
                "status": "published",
                "target_page_id": page["id"],
                "target_page_name": page.get("name"),
                "published_at": self.store._now(),
                "facebook_result": result,
                "last_publish_error": None,
            },
        )

    def schedule_approved_post(
        self,
        draft_id: str,
        publish_time: int,
        approval_token: str,
        target_page_id: str | None = None,
        target_page_name: str | None = None,
    ) -> dict[str, Any]:
        if not self._approval_token_matches(approval_token):
            return {"error": "Invalid approval token"}

        draft = self.store.get_draft(draft_id)
        if not draft:
            return {"error": f"Draft not found: {draft_id}"}
        if draft.get("status") != "approved":
            return {"error": "Draft must be approved before scheduling", "draft_status": draft.get("status")}

        if draft.get("type") == "image_post":
            return {"error": "Image post scheduling is not implemented; schedule text posts or publish image posts manually."}

        page = self._target_page_for_draft(draft, target_page_id, target_page_name)
        if not page:
            return {
                "error": "Choose a target page before scheduling",
                "draft_id": draft_id,
                "available_pages": self.list_publishable_pages(),
            }

        result = self.api.schedule_post(draft["message"], publish_time, page_id=page["id"], access_token=page["access_token"])
        if "error" in result:
            return self.store.update_draft(
                draft_id,
                {
                    "status": "approved",
                    "last_publish_error": result["error"],
                    "facebook_result": result,
                },
            )

        return self.store.update_draft(
            draft_id,
            {
                "status": "scheduled",
                "target_page_id": page["id"],
                "target_page_name": page.get("name"),
                "scheduled_publish_time": publish_time,
                "facebook_result": result,
                "last_publish_error": None,
            },
        )

    def upload_image_for_review(
        self,
        image_url: str,
        caption: str = "",
        target_page_id: str | None = None,
        target_page_name: str | None = None,
    ) -> dict[str, Any]:
        page = self._resolve_page(page_id=target_page_id, page_name=target_page_name)
        if not page:
            return {"error": "Target page not found", "available_pages": self.list_publishable_pages()}
        return self.api.upload_unpublished_photo(image_url, caption, page_id=page["id"], access_token=page["access_token"])

    def list_recent_posts(self, limit: int = 10, target_page_id: str | None = None, target_page_name: str | None = None) -> dict[str, Any]:
        page = self._resolve_page(page_id=target_page_id, page_name=target_page_name)
        if not page:
            return {"error": "Target page not found", "available_pages": self.list_publishable_pages()}
        return self.api.get_posts(limit=limit, page_id=page["id"], access_token=page["access_token"])

    def check_topic_overlap(self, topic: str, limit: int = 20) -> dict[str, Any]:
        posts = self.list_recent_posts(limit=limit)
        topic_terms = self._keywords(topic)
        matches = []
        for post in posts.get("data", []):
            message = post.get("message", "")
            overlap = sorted(topic_terms.intersection(self._keywords(message)))
            if overlap:
                matches.append(
                    {
                        "post_id": post.get("id"),
                        "created_time": post.get("created_time"),
                        "permalink_url": post.get("permalink_url"),
                        "overlap_terms": overlap,
                        "message_preview": message[:180],
                    }
                )
        return {"topic": topic, "checked_posts": len(posts.get("data", [])), "matches": matches}

    def analyze_recent_post_performance(self, limit: int = 10) -> dict[str, Any]:
        posts = self.list_recent_posts(limit=limit).get("data", [])
        summaries = []
        for post in posts:
            post_id = post.get("id")
            if not post_id:
                continue
            reactions = self.get_post_reactions_breakdown(post_id)
            comments = self.get_number_of_comments(post_id)
            shares = self.get_post_share_count(post_id)
            likes = self.get_number_of_likes(post_id)
            engagement_score = comments * 3 + shares * 4 + likes
            summaries.append(
                {
                    "post_id": post_id,
                    "created_time": post.get("created_time"),
                    "permalink_url": post.get("permalink_url"),
                    "message_preview": post.get("message", "")[:180],
                    "comments": comments,
                    "shares": shares,
                    "likes": likes,
                    "reactions": reactions,
                    "engagement_score": engagement_score,
                }
            )

        summaries.sort(key=lambda item: item["engagement_score"], reverse=True)
        top_themes = self._extract_theme_terms([item["message_preview"] for item in summaries[:5]])
        snapshot = self.store.add_performance_snapshot(
            {
                "limit": limit,
                "top_themes": top_themes,
                "posts": summaries,
            }
        )
        return snapshot

    def _compose_post(
        self,
        topic: str,
        source_notes: str,
        audience: str,
        goal: str,
        style: str,
        call_to_action: str,
    ) -> str:
        return (
            f"{topic}\n\n"
            f"重點整理：\n{source_notes.strip()}\n\n"
            f"為什麼值得注意：這件事對 {audience} 的影響，不只在新聞本身，而是在接下來的產品、工作流程與商業判斷會怎麼改變。\n\n"
            f"我的觀察：\n"
            f"1. 先看它解決了什麼真問題，而不是只看模型或工具名稱。\n"
            f"2. 再看它會改變誰的工作流程，尤其是內容、開發、營運與決策環節。\n"
            f"3. 最後看落地成本，包括資料、權限、安全與維護。\n\n"
            f"結論：{goal}。\n\n"
            f"{call_to_action}\n\n"
            f"#AIAgent #OpenAI #Claude #生成式AI"
        )

    def _approval_token_matches(self, approval_token: str) -> bool:
        return bool(FACEBOOK_APPROVAL_TOKEN) and approval_token == FACEBOOK_APPROVAL_TOKEN

    def _resolve_page(self, page_id: str | None = None, page_name: str | None = None) -> dict[str, Any] | None:
        return self.pages.resolve_page(
            page_id=page_id,
            page_name=page_name,
            fallback_page_id=PAGE_ID,
            fallback_access_token=PAGE_ACCESS_TOKEN,
        )

    def _target_page_for_draft(
        self,
        draft: dict[str, Any],
        page_id: str | None = None,
        page_name: str | None = None,
    ) -> dict[str, Any] | None:
        selected_page_id = page_id or draft.get("target_page_id")
        selected_page_name = page_name or draft.get("target_page_name")
        if not selected_page_id and not selected_page_name and self.pages.list_pages():
            return None

        return self._resolve_page(
            page_id=selected_page_id,
            page_name=selected_page_name,
        )

    def _keywords(self, text: str) -> set[str]:
        normalized = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
        return {part for part in normalized.split() if len(part) >= 3}

    def _extract_theme_terms(self, messages: list[str]) -> list[dict[str, Any]]:
        counts: dict[str, int] = {}
        stopwords = {"the", "and", "for", "with", "this", "that", "you", "are", "but", "from"}
        for message in messages:
            for keyword in self._keywords(message):
                if keyword not in stopwords:
                    counts[keyword] = counts.get(keyword, 0) + 1
        ranked = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        return [{"term": term, "count": count} for term, count in ranked[:12]]
