#!/usr/bin/env bash
# Scaffold one paper directory under survey/papers/.
#
#   bash Claude/scripts/new_paper.sh <PaperShortName> <arxiv-id | pdf-url>
#   bash Claude/scripts/new_paper.sh <PaperShortName> --web <page-url>
#
# Examples:
#   bash Claude/scripts/new_paper.sh GPTQ 2210.17323
#   bash Claude/scripts/new_paper.sh SomeVendorPost --web https://example.com/blog/post
#
# Creates survey/papers/<PaperShortName>/ with extract.py (or fetch.py),
# extracted/README.md and an ANALYSIS.md skeleton, with the download command and the
# URL already filled in. It does NOT download anything -- that is the next step, and
# it is printed for you.
set -euo pipefail

usage() { sed -n '2,12p' "$0"; exit 1; }
[ $# -ge 2 ] || usage

NAME="$1"; shift
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TPL="$ROOT/Claude/scripts/templates/paper"
DEST="$ROOT/survey/papers/$NAME"

[ -e "$DEST" ] && { echo "!! $DEST already exists; nothing done."; exit 1; }

MODE=pdf
if [ "$1" = "--web" ]; then MODE=web; shift; fi
SRC="$1"

mkdir -p "$DEST/extracted"
cp "$TPL/extracted/README.md" "$DEST/extracted/README.md"

# sed with | as the delimiter: URLs contain / but not |
if [ "$MODE" = web ]; then
    STEM="$(echo "$NAME" | tr '[:upper:]' '[:lower:]')"
    sed -e "s|__URL__|$SRC|g" -e "s|__STEM__|$STEM|g" "$TPL/fetch.py" > "$DEST/fetch.py"
    DOWNLOAD="python3 fetch.py --refetch"
    URL="$SRC"
    NEXT="cd survey/papers/$NAME && python3 fetch.py"
else
    case "$SRC" in
        http*) URL="$SRC"; STEM="$(basename "${SRC%.pdf}")" ;;
        *)     URL="https://arxiv.org/abs/$SRC"; STEM="$SRC" ;;
    esac
    case "$SRC" in
        http*) PDFURL="$SRC" ;;
        *)     PDFURL="https://arxiv.org/pdf/$SRC" ;;
    esac
    DOWNLOAD="curl -sSL -o $STEM.pdf $PDFURL"
    sed -e "s|__DOWNLOAD__|$DOWNLOAD|g" "$TPL/extract.py" > "$DEST/extract.py"
    NEXT="cd survey/papers/$NAME && $DOWNLOAD && python3 extract.py"
fi

sed -e "s|__NAME__|$NAME|g" \
    -e "s|__URL__|$URL|g" \
    -e "s|__DOWNLOAD__|$DOWNLOAD|g" \
    -e "s|__DATE__|$(date +%F)|g" \
    -e "s|__STATUS__|pdf missing|g" \
    "$TPL/ANALYSIS.md" > "$DEST/ANALYSIS.md"

echo "created survey/papers/$NAME/"
find "$DEST" -type f | sed "s|$ROOT/|  |"
echo
echo "next:"
echo "  $NEXT"
echo "  # then fill in ANALYSIS.md (every __PLACEHOLDER__ must go), verify the"
echo "  # publication info per AGENT-GUIDE §2.1, and add a row to survey/README.md"
