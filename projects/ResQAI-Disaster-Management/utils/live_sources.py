"""Live X posts and related news-source lookup for ResQAI.

X data is fetched from the official X API v2 Recent Search endpoint when
X_BEARER_TOKEN is configured. Related coverage is discovered through Google
News search results (RSS), and each returned item links to the publisher page.
"""

import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

X_ENDPOINT = "https://api.x.com/2/tweets/search/recent"
DEFAULT_X_QUERY = '(disaster OR earthquake OR flood OR wildfire OR emergency) lang:en -is:retweet -is:reply'


def _token():
    return os.getenv("X_BEARER_TOKEN", "").strip()


def x_configured():
    return bool(_token())


def _google_news_url(query):
    params = urllib.parse.urlencode({"q": query, "hl": "en-IN", "gl": "IN", "ceid": "IN:en"})
    return f"https://news.google.com/rss/search?{params}"


def google_news_sources(query, limit=5):
    """Return up to `limit` Google News results with original publisher links.

    This is a discovery/corroboration layer, not a claim that the stories
    independently verify a specific X post.
    """
    query = (query or "").strip()
    if not query:
        return []
    try:
        req = urllib.request.Request(
            _google_news_url(query),
            headers={"User-Agent": "ResQAI/1.0 (news-source-discovery)"},
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
    except Exception:
        return []

    items = []
    for item in root.findall("./channel/item")[: max(1, min(limit, 10))]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_date = (item.findtext("pubDate") or "").strip()
        source_el = item.find("source")
        publisher = (source_el.text or "").strip() if source_el is not None else "Google News"
        source_url = source_el.get("url", "") if source_el is not None else ""
        items.append({
            "title": title,
            "link": link,
            "publisher": publisher,
            "publisher_url": source_url,
            "published": pub_date,
        })
    return items


def search_x_posts(query=DEFAULT_X_QUERY, count=25):
    """Fetch real public X posts from the last seven days via official X API."""
    token = _token()
    if not token:
        raise RuntimeError(
            "Live X posts require X_BEARER_TOKEN. Add your official X API bearer token "
            "to the environment and restart the app."
        )

    count = max(10, min(int(count), 100))
    params = {
        "query": query.strip() or DEFAULT_X_QUERY,
        "max_results": count,
        "tweet.fields": "created_at,author_id,public_metrics,lang,source",
        "expansions": "author_id",
        "user.fields": "id,name,username,verified",
    }
    res = requests.get(
        X_ENDPOINT,
        params=params,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    if not res.ok:
        try:
            detail = res.json().get("detail") or res.json().get("title") or res.text
        except Exception:
            detail = res.text
        raise RuntimeError(f"X API request failed ({res.status_code}): {detail}")

    data = res.json()
    users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
    posts = []
    for p in data.get("data", []):
        user = users.get(p.get("author_id"), {})
        username = user.get("username")
        post_id = p.get("id")
        posts.append({
            "id": post_id,
            "text": p.get("text", ""),
            "created_at": p.get("created_at"),
            "author_name": user.get("name") or "Unknown account",
            "username": username or "",
            "verified": bool(user.get("verified")),
            "url": f"https://x.com/{username}/status/{post_id}" if username and post_id else "",
            "public_metrics": p.get("public_metrics", {}),
            "source": p.get("source"),
            "lang": p.get("lang"),
        })
    return posts
