#!/usr/bin/env bash
# Publish the tested remote main commit; never move an existing tag or release.
set -euo pipefail
cd "$(dirname "$0")"
[[ "$(git branch --show-current)" == main ]] || { echo 'Checkout main first' >&2; exit 2; }
[[ -z "$(git status --porcelain)" ]] || { echo 'Working tree must be clean' >&2; exit 2; }
command -v gh >/dev/null || { echo 'GitHub CLI (gh) is required' >&2; exit 2; }
if [[ "${1:-}" == --verified ]]; then
  [[ "${GITHUB_ACTIONS:-}" == true ]] || { echo '--verified is reserved for the tested release workflow' >&2; exit 2; }
else
  [[ $# == 0 ]] || { echo 'Usage: ./publish.sh' >&2; exit 2; }
  python3 trellis.py validate
  python3 -m unittest discover -s tests -v
fi
git fetch origin main
commit="$(git rev-parse HEAD)"
[[ "$commit" == "$(git rev-parse origin/main)" ]] || { echo 'HEAD must match remote main; review and push changes first' >&2; exit 2; }
version="$(cat VERSION)"
[[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo 'Invalid VERSION' >&2; exit 2; }
tag="v$version"
repo=datanger/Trellis
refs="$(git ls-remote --tags origin "refs/tags/$tag" "refs/tags/$tag^{}")"
if [[ -n "$refs" ]]; then
  tagged_commit="$(printf '%s\n' "$refs" | awk '/\^\{\}$/ {print $1; found=1} END {if (!found) exit 1}')" || tagged_commit="$(printf '%s\n' "$refs" | awk 'NR==1 {print $1}')"
  [[ "$tagged_commit" == "$commit" ]] || { echo 'Existing remote tag points to another commit; refusing to move it' >&2; exit 2; }
fi
if gh release view "$tag" --repo "$repo" >/dev/null 2>&1; then
  echo "Release $tag already exists; leaving it unchanged."
  exit 0
fi
notes="$(mktemp)"; trap 'rm -f -- "$notes"' EXIT
awk -v tag="$tag" '$0 ~ "^## " tag "( |$)" {found=1; print; next} found && /^## / {exit} found {print}' CHANGELOG.md > "$notes"
[[ -s "$notes" ]] || { echo 'Missing version section in CHANGELOG.md' >&2; exit 2; }
args=(--repo "$repo" --target "$commit" --title "Trellis $tag" --notes-file "$notes" --latest)
[[ -z "$refs" ]] || args+=(--verify-tag)
gh release create "$tag" "${args[@]}"
