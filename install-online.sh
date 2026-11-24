#!/usr/bin/env bash
# Trellis online installer. Download a GitHub source archive; no manual git clone.
set -euo pipefail

main() {
    local ref=main expected='' tmp archive source version
    local -a args=()
    while (($#)); do
        case "$1" in
            --version)
                (($# >= 2)) || { echo 'Missing value for --version' >&2; return 2; }
                [[ "$2" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo 'Use --version vX.Y.Z' >&2; return 2; }
                ref="refs/tags/$2"; expected="${2#v}"; shift 2 ;;
            --help|-h)
                cat <<'HELP'
Trellis online installer (defaults to main, both hosts, user scope).
  --host codex|claude|both
  --scope user|project
  --target /path/to/project    Project scope; defaults to current directory.
  --version vX.Y.Z            Install an exact published tag instead of main.
  --replace                  Replace an existing managed Trellis installation.
  --offline                  Skip upstream downloads (wrapper development only).
Requires Bash, curl, tar, Git and Python 3.9+. Upstream dependencies are downloaded
by the existing installer. No manual repository checkout is required.
HELP
                return 0 ;;
            *) args+=("$1"); shift ;;
        esac
    done
    for cmd in curl tar git "${PYTHON:-python3}"; do
        command -v "$cmd" >/dev/null 2>&1 || { echo "Missing required tool: $cmd" >&2; return 2; }
    done
    "${PYTHON:-python3}" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else "Python 3.9+ required")'
    tmp="$(mktemp -d)"
    # EXIT trap runs after main returns; expand the quoted directory now.
    trap 'rm -rf -- "${TRELLIS_INSTALL_TEMP}"' EXIT
    TRELLIS_INSTALL_TEMP="$tmp"
    archive="$tmp/source.tar.gz"; source="$tmp/source"
    mkdir -p "$source"
    if [[ "$ref" == main ]]; then ref=refs/heads/main; fi
    echo "Downloading Trellis from $ref ..." >&2
    curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' \
        --retry 2 --connect-timeout 15 --max-time 300 \
        "https://codeload.github.com/datanger/Trellis/tar.gz/$ref" -o "$archive"
    tar -xzf "$archive" -C "$source" --strip-components=1
    [[ -f "$source/install.sh" && -f "$source/VERSION" && -f "$source/trellis.py" ]] || {
        echo 'Invalid Trellis archive' >&2; return 1;
    }
    version="$(cat "$source/VERSION")"
    [[ "$version" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || { echo 'Invalid archive VERSION' >&2; return 1; }
    [[ -z "$expected" || "$version" == "$expected" ]] || { echo 'Archive version does not match requested tag' >&2; return 1; }
    # Do not change directories: relative --target paths are relative to the caller.
    bash "$source/install.sh" "${args[@]}"
}

main "$@"
