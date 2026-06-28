from __future__ import annotations

import time
import requests
from typing import Any
from config import INSTAGRAM_GRAPH_BASE_URL, INSTAGRAM_TOKEN, INSTAGRAM_USER_ID


class InstagramAPI:
    """Instagram API with Instagram Login (graph.instagram.com).

    Uses an Instagram-scoped access token (starts with "IGAA") and the
    Instagram user id directly — no Facebook Page required. Publishing is the
    standard two-step Content Publishing flow:
      1. Create a media container on /{ig_user_id}/media.
      2. Publish it on /{ig_user_id}/media_publish with the returned creation_id.
    Video/Reels containers must finish processing (status_code == FINISHED)
    before they can be published, so those paths poll the container first.

    Requires the token to carry instagram_business_content_publish and the
    account to be a professional (Business/Creator) account. Media must be a
    publicly reachable URL.
    """

    def __init__(self, access_token: str | None = None, ig_user_id: str | None = None):
        self.access_token = access_token or INSTAGRAM_TOKEN
        self.ig_user_id = ig_user_id or INSTAGRAM_USER_ID

    def _request(self, method: str, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{INSTAGRAM_GRAPH_BASE_URL}/{endpoint}"
        request_params = {**params, "access_token": self.access_token}
        try:
            response = requests.request(method, url, params=request_params, timeout=60)
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

    def _ig(self, ig_user_id: str | None) -> str:
        return ig_user_id or self.ig_user_id

    # --- account --------------------------------------------------------------
    def get_account_info(self) -> dict[str, Any]:
        """Return basic info for the configured Instagram account."""
        return self._request(
            "GET",
            "me",
            {"fields": "user_id,username,name,account_type,media_count,followers_count,profile_picture_url"},
        )

    def get_content_publishing_limit(self, ig_user_id: str | None = None) -> dict[str, Any]:
        """Return the 24h content-publishing quota usage."""
        return self._request("GET", f"{self._ig(ig_user_id)}/content_publishing_limit", {"fields": "config,quota_usage"})

    # --- container creation ---------------------------------------------------
    def create_image_container(self, image_url: str, caption: str = "", ig_user_id: str | None = None) -> dict[str, Any]:
        return self._request("POST", f"{self._ig(ig_user_id)}/media", {"image_url": image_url, "caption": caption})

    def create_carousel_item(self, image_url: str, ig_user_id: str | None = None) -> dict[str, Any]:
        return self._request("POST", f"{self._ig(ig_user_id)}/media", {"image_url": image_url, "is_carousel_item": True})

    def create_carousel_container(self, children: list[str], caption: str = "", ig_user_id: str | None = None) -> dict[str, Any]:
        return self._request("POST", f"{self._ig(ig_user_id)}/media", {"media_type": "CAROUSEL", "children": ",".join(children), "caption": caption})

    def create_reel_container(self, video_url: str, caption: str = "", cover_url: str | None = None, ig_user_id: str | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"media_type": "REELS", "video_url": video_url, "caption": caption}
        if cover_url:
            params["cover_url"] = cover_url
        return self._request("POST", f"{self._ig(ig_user_id)}/media", params)

    # --- status + publish -----------------------------------------------------
    def get_container_status(self, container_id: str) -> dict[str, Any]:
        return self._request("GET", f"{container_id}", {"fields": "status_code,status"})

    def wait_until_ready(self, container_id: str, attempts: int = 30, delay: int = 3) -> dict[str, Any]:
        """Poll a container until FINISHED. Returns {} when ready, else an error dict."""
        for _ in range(attempts):
            status = self.get_container_status(container_id)
            if "error" in status:
                return status
            code = status.get("status_code")
            if code == "FINISHED":
                return {}
            if code == "ERROR":
                return {"error": {"message": f"Media processing failed: {status.get('status')}", "type": "MediaProcessingError"}}
            time.sleep(delay)
        return {"error": {"message": "Timed out waiting for media to finish processing", "type": "MediaProcessingTimeout", "container_id": container_id}}

    def publish_container(self, creation_id: str, ig_user_id: str | None = None) -> dict[str, Any]:
        return self._request("POST", f"{self._ig(ig_user_id)}/media_publish", {"creation_id": creation_id})

    def get_media_permalink(self, media_id: str) -> dict[str, Any]:
        return self._request("GET", f"{media_id}", {"fields": "permalink"})

    # --- high-level one-shot helpers -----------------------------------------
    def post_image(self, image_url: str, caption: str = "", ig_user_id: str | None = None) -> dict[str, Any]:
        container = self.create_image_container(image_url, caption, ig_user_id=ig_user_id)
        if "error" in container:
            return container
        creation_id = container.get("id")
        if not creation_id:
            return {"error": {"message": "No container id returned", "type": "ContainerError", "raw": container}}
        return self.publish_container(creation_id, ig_user_id=ig_user_id)

    def post_carousel(self, image_urls: list[str], caption: str = "", ig_user_id: str | None = None) -> dict[str, Any]:
        if not (2 <= len(image_urls) <= 10):
            return {"error": {"message": "Carousel requires 2-10 images", "type": "ValidationError"}}
        children: list[str] = []
        for url in image_urls:
            item = self.create_carousel_item(url, ig_user_id=ig_user_id)
            if "error" in item:
                return item
            children.append(item["id"])
        container = self.create_carousel_container(children, caption, ig_user_id=ig_user_id)
        if "error" in container:
            return container
        return self.publish_container(container["id"], ig_user_id=ig_user_id)

    def post_reel(self, video_url: str, caption: str = "", cover_url: str | None = None, ig_user_id: str | None = None) -> dict[str, Any]:
        container = self.create_reel_container(video_url, caption, cover_url, ig_user_id=ig_user_id)
        if "error" in container:
            return container
        creation_id = container.get("id")
        if not creation_id:
            return {"error": {"message": "No container id returned", "type": "ContainerError", "raw": container}}
        ready = self.wait_until_ready(creation_id)
        if "error" in ready:
            return ready
        return self.publish_container(creation_id, ig_user_id=ig_user_id)
