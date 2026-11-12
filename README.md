# owenmakers.github.io

Sitemap for [owenmakers.substack.com](https://owenmakers.substack.com/), served by GitHub Pages at
<https://owenmakers.github.io/sitemap.xml>.

Substack serves no sitemap for this publication and its RSS feed only lists the latest ~20 posts.
`generate_sitemap.py` rebuilds `sitemap.xml` from Substack's public archive API. `update.sh` runs it
and pushes when the post list changes; a launchd job on the author's Mac runs `update.sh` daily
(`~/Library/LaunchAgents/com.owenmakers.sitemap.plist`, log in `update.log`).
GitHub Actions is not used because Substack returns 403 to GitHub-hosted runners.

Keep the `google*.html` file: it is the Google Search Console ownership verification.
