# Facebook MCP Server

This project is a **MCP server** for automating and managing interactions on a Facebook Page using the Facebook Graph API. It exposes tools to create posts, moderate comments, fetch post insights, and filter negative feedback — ready to plug into Claude, or other LLM-based agents.

[![Trust Score](https://archestra.ai/mcp-catalog/api/badge/quality/HagaiHen/facebook-mcp-server)](https://archestra.ai/mcp-catalog/hagaihen__facebook-mcp-server)
<a href="https://glama.ai/mcp/servers/@HagaiHen/facebook-mcp-server">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@HagaiHen/facebook-mcp-server/badge" />
</a>

---

## 🤖 What Is This?

This MCP provides a suite of AI-callable tools that connect directly to a Facebook Page, abstracting common API operations as LLM-friendly functions.

### ✅ Benefits

- Empowers **social media managers** to automate moderation and analytics.
- Seamlessly integrates with **Claude Desktop or any Agent client**.
- Enables fine-grained control over Facebook content from natural language.

---

## 📦 Features

| Tool                             | Description                                                         |
|----------------------------------|---------------------------------------------------------------------|
| `post_to_facebook`               | Create a new Facebook post with a message.                          |
| `reply_to_comment`               | Reply to a specific comment on a post.                              |
| `get_page_posts`                 | Retrieve recent posts from the Page.                                |
| `get_post_comments`              | Fetch comments on a given post.                                     |
| `delete_post`                    | Delete a specific post by ID.                                       |
| `delete_comment`                 | Delete a specific comment by ID.                                    |
| `hide_comment`                   | Hide a comment from public view.                         |
| `unhide_comment`                 | Unhide a previously hidden comment.                      |
| `delete_comment_from_post`       | Alias for deleting a comment from a specific post.                  |
| `filter_negative_comments`       | Filter out comments with negative sentiment keywords.               |
| `get_number_of_comments`         | Count the number of comments on a post.                             |
| `get_number_of_likes`            | Count the number of likes on a post.                                |
| `get_post_impressions`           | Get total impressions on a post.                                    |
| `get_post_impressions_unique`    | Get number of unique users who saw the post.                        |
| `get_post_impressions_paid`      | Get number of paid impressions on the post.                         |
| `get_post_impressions_organic`   | Get number of organic impressions on the post.                      |
| `get_post_engaged_users`         | Get number of users who engaged with the post.                      |
| `get_post_clicks`                | Get number of clicks on the post.                                   |
| `get_post_reactions_like_total`  | Get total number of 'Like' reactions.                               |
| `get_post_top_commenters`        | Get the top commenters on a post.                                   |
| `post_image_to_facebook`         | Post an image with a caption to the Facebook page.                  |
| `send_dm_to_user`                | Send a direct message to a user.                                    |
| `update_post`                    | Updates an existing post's message.                                 |
| `schedule_post`                  | Schedule a post for future publication.                     |
| `get_page_fan_count`             | Retrieve the total number of Page fans.                     |
| `get_post_share_count`           | Get the number of shares on a post.                         |
| `get_post_reactions_breakdown`   | Get all reaction counts for a post in one call.              |
| `bulk_delete_comments`           | Delete multiple comments by ID.                              |
| `bulk_hide_comments`             | Hide multiple comments by ID.                               |
| `bulk_unhide_comments`           | Unhide multiple comments by ID.                             |
| `get_comment_replies`            | Get all replies to a specific comment.                      |
| `get_post_permalink`             | Get the permalink URL of a post.                            |
| `get_scheduled_posts`            | List all scheduled (unpublished) posts on the Page.         |
| `get_page_info`                  | Get extended Page details (name, about, category, website). |
| `draft_facebook_post`            | Create a local post draft in your configured writing style. |
| `draft_image_post`               | Create a local image post draft for review.                 |
| `list_post_drafts`               | List local drafts by status.                                |
| `approve_post_draft`             | Mark a draft as approved after human review.                |
| `publish_approved_post`          | Publish an approved draft to Facebook.                      |
| `schedule_approved_post`         | Schedule an approved text draft.                            |
| `upload_image_for_review`        | Upload unpublished image media for review.                  |
| `list_recent_posts`              | Retrieve recent posts for planning.                         |
| `check_topic_overlap`            | Compare a planned topic with recent posts.                  |
| `analyze_recent_post_performance`| Analyze recent engagement and store a local snapshot.       |
| `list_publishable_pages`         | List locally configured Pages without exposing tokens.      |
| `set_draft_target_page`          | Choose which Page a draft should publish to.                |

---

## 🚀 Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/facebook-mcp-server.git
cd facebook-mcp-server
```

### 2. 🛠️ Installation

Install dependencies using uv, a fast Python package manager:
If uv is not already installed, run:
```bash
curl -Ls https://astral.sh/uv/install.sh | bash
```

Once uv is installed, install the project dependencies:
```bash
uv pip install -r requirements.txt
```

### 3. Set Up Environment

Create a .env file in the root directory and add your Facebook Page credentials. 
You can obtain these from  https://developers.facebook.com/tools/explorer

```bash
FACEBOOK_ACCESS_TOKEN=your_facebook_page_access_token
FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_APPROVAL_TOKEN=choose_a_local_human_approval_secret
FACEBOOK_TOKEN_FILE=/Users/chrishsu/.env/.fbtoken
FACEBOOK_TOKEN_JSON_FILE=/Users/chrishsu/.env/fbtoken.json
CONTENT_STORE_PATH=content_store.json
DEFAULT_POST_STYLE="Write in Traditional Chinese for an AI technology audience in Taiwan. Use a direct, analytical tone, start with a concrete hook, explain why it matters, add practical implications, and end with a clear takeaway."
```

`FACEBOOK_TOKEN_FILE` can point to either a normal dotenv file or a file containing only the raw Facebook access token. The default path is `/Users/chrishsu/.env/.fbtoken`.

`FACEBOOK_TOKEN_JSON_FILE` can point to a Graph API `/me/accounts?fields=id,name,tasks,access_token` response. Tokens from this file stay internal; MCP tools only expose Page IDs, names, tasks, and publishability.

## 🧑‍💼 Custom Creator Workflow

This fork adds a safer creator workflow for running a Facebook Page with an AI agent.

Recommended flow:

```text
draft_facebook_post
  -> list_publishable_pages
  -> set_draft_target_page
  -> list_post_drafts / get_post_draft
  -> approve_post_draft
  -> publish_approved_post or schedule_approved_post
```

The publish and schedule tools require `FACEBOOK_APPROVAL_TOKEN`. This keeps AI-assisted drafting separate from real Facebook publishing.

For image posts:

```text
draft_image_post
  -> review draft and image URL
  -> approve_post_draft
  -> publish_approved_post
```

For planning and analytics:

```text
check_topic_overlap
  -> avoid repeating recent topics

analyze_recent_post_performance
  -> rank recent posts by comments, shares, likes, and reactions
```

Local drafts and performance snapshots are stored in `CONTENT_STORE_PATH`. The default `content_store.json` is ignored by git because it may contain unpublished content.

## 🧩 Using with Claude Desktop
To set up the FacebookMCP in Clade:

1.	Open Clade.
2.	Go to Settings → Developer → Edit Config.
3.	In the config file that opens, add the following entry:

```bash
"FacebookMCP": {
  "command": "uv",
  "args": [
    "run",
    "--with",
    "mcp[cli]",
    "--with",
    "requests",
    "mcp",
    "run",
    "/path/to/facebook-mcp-server/server.py"
  ]
}
```

---

## ✅ You’re Ready to Go!

That’s it — your Facebook MCP server is now fully configured and ready to power Claude Desktop. You can now post, moderate, and measure engagement all through natural language prompts!

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to fork the repo and submit a pull request.

- Create a branch: `git checkout -b feature/YourFeature`
- Commit your changes: `git commit -m 'feat: add new feature'`
- Push to the branch: `git push origin feature/YourFeature`
- Open a pull request 🎉
