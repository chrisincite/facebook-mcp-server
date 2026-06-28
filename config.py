import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

FBTOKEN_PATH = Path(os.getenv("FACEBOOK_TOKEN_FILE", "/Users/chrishsu/.env/.fbtoken"))
FBTOKEN_JSON_PATH = Path(os.getenv("FACEBOOK_TOKEN_JSON_FILE", "/Users/chrishsu/.env/fbtoken.json"))
if FBTOKEN_PATH.exists():
    load_dotenv(FBTOKEN_PATH, override=False)

INSTAGRAM_TOKEN_PATH = Path(os.getenv("INSTAGRAM_TOKEN_FILE", "/Users/chrishsu/.env/.instagram_token"))
if INSTAGRAM_TOKEN_PATH.exists():
    load_dotenv(INSTAGRAM_TOKEN_PATH, override=False)

# Facebook Graph API setup
GRAPH_API_VERSION = "v22.0"
PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN") or os.getenv("FBTOKEN")
if not PAGE_ACCESS_TOKEN and FBTOKEN_PATH.exists():
    raw_token = FBTOKEN_PATH.read_text(encoding="utf-8").strip()
    if raw_token and "=" not in raw_token:
        PAGE_ACCESS_TOKEN = raw_token
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
GRAPH_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

# Instagram API with Instagram Login (graph.instagram.com). Tokens start with "IGAA".
INSTAGRAM_GRAPH_VERSION = "v22.0"
INSTAGRAM_GRAPH_BASE_URL = f"https://graph.instagram.com/{INSTAGRAM_GRAPH_VERSION}"
INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")

# Local workflow defaults for this fork.
CONTENT_STORE_PATH = os.getenv("CONTENT_STORE_PATH", "content_store.json")
FACEBOOK_APPROVAL_TOKEN = os.getenv("FACEBOOK_APPROVAL_TOKEN")
FACEBOOK_TOKEN_JSON_FILE = str(FBTOKEN_JSON_PATH)
DEFAULT_POST_STYLE = os.getenv(
    "DEFAULT_POST_STYLE",
    "Write in Traditional Chinese for an AI technology audience in Taiwan. "
    "Use a direct, analytical tone, start with a concrete hook, explain why it "
    "matters, add practical implications, and end with a clear takeaway.",
)
