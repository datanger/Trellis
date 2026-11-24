#!/usr/bin/env bash
# Publish a verified local Git checkout. Never overwrites an existing remote.
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
if [[ $# -ne 1 || ( "$1" != "--public" && "$1" != "--private" ) ]]; then
  echo 'Usage: ./publish.sh --public|--private (choose visibility explicitly)' >&2; exit 2
fi
visibility="$1"
command -v gh >/dev/null || { echo 'Install GitHub CLI (gh), then run gh auth login.' >&2; exit 2; }
[[ "$(gh api user --jq .login)" == 'datanger' ]] || { echo 'Expected authenticated GitHub account datanger.' >&2; exit 2; }
[[ -d .git ]] || { echo 'Clone the supplied Git bundle first to preserve commit and tag.' >&2; exit 2; }
[[ "$(git branch --show-current)" == 'main' ]] || { echo 'Checkout main before publishing.' >&2; exit 2; }
[[ -z "$(git status --porcelain)" ]] || { echo 'Working tree must be clean.' >&2; exit 2; }
tag="v$(cat VERSION)"
[[ "$(git rev-parse "$tag^{commit}")" == "$(git rev-parse HEAD)" ]] || { echo 'Version tag must point to current main.' >&2; exit 2; }
python3 trellis.py validate
python3 -m unittest discover -s tests -v
# A bundle clone has a local origin; remove it only if it is a local bundle file.
if git remote get-url origin >/dev/null 2>&1; then
  remote=$(git remote get-url origin)
  if [[ "$remote" == *.bundle ]]; then git remote remove origin
  elif [[ "$remote" != 'https://github.com/datanger/Trellis.git' && "$remote" != 'git@github.com:datanger/Trellis.git' ]]; then
    echo "Unexpected origin: $remote" >&2; exit 2
  fi
fi
if gh repo view datanger/Trellis >/dev/null 2>&1; then
  echo 'Repository already exists. Refusing to publish automatically over existing content. Inspect it first.' >&2; exit 2
fi
if git remote get-url origin >/dev/null 2>&1; then
  gh repo create datanger/Trellis "$visibility" --description 'Grow with structure. Human-in-control workflows for AI coding agents.'
  git push -u origin main
else
  gh repo create datanger/Trellis "$visibility" --description 'Grow with structure. Human-in-control workflows for AI coding agents.' --source . --remote origin --push
fi
git push origin "refs/tags/$tag"
gh repo view datanger/Trellis --json url,visibility
printf 'Published %s\n' "$tag"
