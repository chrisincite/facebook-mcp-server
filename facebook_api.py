from __future__ import annotations

import requests
from typing import Any
from config import GRAPH_API_BASE_URL, PAGE_ID, PAGE_ACCESS_TOKEN


class FacebookAPI:
    # Generic Graph API request method
    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any],
        json: dict[str, Any] = None,
        access_token: str | None = None,
    ) -> dict[str, Any]:
        url = f"{GRAPH_API_BASE_URL}/{endpoint}"
        request_params = {**params, "access_token": access_token or PAGE_ACCESS_TOKEN}
        try:
            response = requests.request(method, url, params=request_params, json=json, timeout=30)
            try:
                payload = response.json()
            except ValueError:
                payload = {}

            if response.ok:
                return payload

            graph_error = payload.get("error", {})
            return {
                "error": {
                    "message": graph_error.get("message", f"HTTP {response.status_code}"),
                    "type": graph_error.get("type", "HTTPError"),
                    "code": graph_error.get("code"),
                    "status_code": response.status_code,
                    "endpoint": endpoint,
                    "method": method,
                }
            }
        except requests.RequestException as exc:
            return {
                "error": {
                    "message": "Network request failed",
                    "type": exc.__class__.__name__,
                    "endpoint": endpoint,
                    "method": method,
                }
            }

    def post_message(self, message: str, page_id: str | None = None, access_token: str | None = None) -> dict[str, Any]:
        return self._request("POST", f"{page_id or PAGE_ID}/feed", {"message": message}, access_token=access_token)

    def reply_to_comment(self, comment_id: str, message: str) -> dict[str, Any]:
        return self._request("POST", f"{comment_id}/comments", {"message": message})

    def get_posts(self, limit: int = 25, page_id: str | None = None, access_token: str | None = None) -> dict[str, Any]:
        return self._request("GET", f"{page_id or PAGE_ID}/posts", {"fields": "id,message,created_time,permalink_url", "limit": limit}, access_token=access_token)

    def get_comments(self, post_id: str) -> dict[str, Any]:
        return self._request("GET", f"{post_id}/comments", {"fields": "id,message,from,created_time"})

    def delete_post(self, post_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"{post_id}", {})

    def delete_comment(self, comment_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"{comment_id}", {})

    def hide_comment(self, comment_id: str) -> dict[str, Any]:
        """Hide a comment from the Page."""
        return self._request("POST", f"{comment_id}", {"is_hidden": True})

    def unhide_comment(self, comment_id: str) -> dict[str, Any]:
        """Unhide a previously hidden comment."""
        return self._request("POST", f"{comment_id}", {"is_hidden": False})

    def get_insights(self, post_id: str, metric: str, period: str = "lifetime") -> dict[str, Any]:
        return self._request("GET", f"{post_id}/insights", {"metric": metric, "period": period})

    def get_bulk_insights(self, post_id: str, metrics: list[str], period: str = "lifetime") -> dict[str, Any]:
        metric_str = ",".join(metrics)
        return self.get_insights(post_id, metric_str, period)

    def post_image_to_facebook(self, image_url: str, caption: str, page_id: str | None = None, access_token: str | None = None) -> dict[str, Any]:
        params = {
            "url": image_url,
            "caption": caption
        }
        return self._request("POST", f"{page_id or PAGE_ID}/photos", params, access_token=access_token)

    def upload_unpublished_photo(self, image_url: str, caption: str = "", page_id: str | None = None, access_token: str | None = None) -> dict[str, Any]:
        params = {
            "url": image_url,
            "caption": caption,
            "published": False,
        }
        return self._request("POST", f"{page_id or PAGE_ID}/photos", params, access_token=access_token)
    
    def send_dm_to_user(self, user_id: str, message: str) -> dict[str, Any]:
        payload = {
            "recipient": {"id": user_id},
            "message": {"text": message},
            "messaging_type": "RESPONSE"
        }
        return self._request("POST", "me/messages", {}, json=payload)
    
    def update_post(self, post_id: str, new_message: str) -> dict[str, Any]:
        return self._request("POST", f"{post_id}", {"message": new_message})

    def schedule_post(self, message: str, publish_time: int, page_id: str | None = None, access_token: str | None = None) -> dict[str, Any]:
        params = {
            "message": message,
            "published": False,
            "scheduled_publish_time": publish_time,
        }
        return self._request("POST", f"{page_id or PAGE_ID}/feed", params, access_token=access_token)

    def get_page_fan_count(self) -> int:
        data = self._request("GET", f"{PAGE_ID}", {"fields": "fan_count"})
        return data.get("fan_count", 0)

    def get_post_share_count(self, post_id: str) -> int:
        data = self._request("GET", f"{post_id}", {"fields": "shares"})
        return data.get("shares", {}).get("count", 0)

    def get_comment_replies(self, comment_id: str) -> dict[str, Any]:
        return self._request("GET", f"{comment_id}/comments", {"fields": "id,message,from,created_time"})

    def get_post_permalink(self, post_id: str) -> dict[str, Any]:
        return self._request("GET", f"{post_id}", {"fields": "permalink_url"})

    def get_scheduled_posts(self) -> dict[str, Any]:
        return self._request("GET", f"{PAGE_ID}/scheduled_posts", {"fields": "id,message,scheduled_publish_time"})

    def get_page_info(self, page_id: str | None = None, access_token: str | None = None) -> dict[str, Any]:
        fields = "name,about,category,website,emails,phone,description,location"
        return self._request("GET", f"{page_id or PAGE_ID}", {"fields": fields}, access_token=access_token)
