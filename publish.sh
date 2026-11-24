#!/usr/bin/env bash
# Publish a reviewed release from the current remote main, never force push.
set -euo pipefail
cd "$(dirname "$0")"
[[ "$(git branch --show-current)" == main ]] || { echo 'Checkout main first' >&2; exit 2; }
[[ -z "$(git status --porcelain)" ]] || { echo 'Working tree must be clean' >&2; exit 2; }
python3 trellis.py validate
python3 -m unittest discover -s tests -v
git fetch origin main
[[ "$(git rev-parse HEAD)" == "$(git rev-parse origin/main)" ]] || { echo 'HEAD must match remote main; review and push changes first' >&2; exit 2; }
tag="v$(cat VERSION)"
if git rev-parse "$tag" >/dev/null 2>&1; then
  [[ "$(git rev-parse "$tag^{commit}")" == "$(git rev-parse HEAD)" ]] || { echo 'Existing local tag differs' >&2; exit 2; }
else
  git tag -a "$tag" -m "Trellis $tag"
fi
git push origin "refs/tags/$tag"
