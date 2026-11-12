#!/usr/bin/env python3
"""Build sitemap.xml for owenmakers.substack.com from Substack's public archive API.

Substack does not serve a sitemap for this publication and its RSS feed only
holds the latest ~20 posts, so this file is hosted on GitHub Pages and
submitted to Google Search Console from there.
"""
import json
import sys
import time
import urllib.parse
import urllib.request
from xml.sax.saxutils import escape

SITE = "https://owenmakers.substack.com"
API = SITE + "/api/v1/archive?sort=new"
OUT = "sitemap.xml"
MAX_PAGES = 200


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; sitemap-builder)",
        "Accept": "application/json",
    })
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # retry transient failures / rate limits
            if attempt == 3:
                raise
            print(f"retry {attempt + 1}: {e}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))


def all_posts():
    posts, cursor = [], None
    for _ in range(MAX_PAGES):
        url = API + ("&cursor=" + urllib.parse.quote(cursor) if cursor else "")
        data = fetch(url)
        posts.extend(data.get("posts", []))
        cursor = data.get("nextCursor")
        if not cursor or not data.get("posts"):
            return posts
        time.sleep(1)
    raise RuntimeError("pagination did not terminate")


def main():
    seen, entries = set(), []
    for p in all_posts():
        url = p.get("canonical_url") or ""
        # only public posts on this publication's own /p/ URLs
        if p.get("audience") != "everyone" or not url.startswith(SITE + "/p/"):
            continue
        if url in seen:
            continue
        seen.add(url)
        entries.append((url, (p.get("post_date") or "")[:10]))

    if not entries:
        sys.exit("no posts found - keeping the existing sitemap")

    newest = max(d for _, d in entries)
    rows = [(SITE + "/", newest), (SITE + "/archive", newest)] + entries
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, date in rows:
        lastmod = f"<lastmod>{date}</lastmod>" if date else ""
        lines.append(f"  <url><loc>{escape(url)}</loc>{lastmod}</url>")
    lines.append("</urlset>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{len(entries)} posts written to {OUT} (newest {newest})")


if __name__ == "__main__":
    main()
