#!/bin/zsh
# Rebuild sitemap.xml and push it when the post list changed. Run daily by launchd.
# Always pushes as the owenmakers GitHub account, whichever gh account is active.
set -eu
cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
export GH_TOKEN="$(gh auth token --user owenmakers)"
GIT=(git -c credential.helper= -c 'credential.helper=!gh auth git-credential')
echo "== $(date '+%F %T')"
"${GIT[@]}" pull -q --rebase origin main
python3 generate_sitemap.py
if git diff --quiet -- sitemap.xml; then
  echo "sitemap unchanged"
  exit 0
fi
git add sitemap.xml
git commit -q -m "Update sitemap"
"${GIT[@]}" push -q origin main
echo "pushed"
