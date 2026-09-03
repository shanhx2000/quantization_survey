#!/usr/bin/env bash
# Read-only status sweep of survey/papers/. Prints, per paper directory:
# its declared status, whether the full text is actually extracted, whether the PDF is
# present locally, and any unfilled __PLACEHOLDER__ left in ANALYSIS.md.
#
#   bash Claude/scripts/check_survey.sh
#
# Use it before updating survey/README.md -- the status table there must match reality.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PAPERS="$ROOT/survey/papers"

echo "########## papers ##########"
printf '  %-28s %-16s %-9s %-5s %s\n' DIR STATUS EXTRACTED PDF PLACEHOLDERS
n=0
for d in "$PAPERS"/*/; do
    [ -d "$d" ] || continue
    n=$((n+1))
    name="$(basename "$d")"
    a="$d/ANALYSIS.md"
    status="(no ANALYSIS.md)"
    holes=0
    if [ -f "$a" ]; then
        status="$(sed -n 's/^[Ss]tatus: *\*\*\([^*]*\)\*\*.*/\1/p' "$a" | head -1)"
        [ -z "$status" ] && status="(unparsed)"
        holes="$(grep -o '__[A-Z_]*__' "$a" | sort -u | wc -l)"
    fi
    ext="no"
    [ -n "$(ls -A "$d/extracted" 2>/dev/null | grep -v '^README.md$')" ] && ext="yes"
    pdf="no"; ls "$d"/*.pdf >/dev/null 2>&1 && pdf="yes"
    printf '  %-28s %-16s %-9s %-5s %s\n' "$name" "$status" "$ext" "$pdf" "$holes"
done
[ "$n" = 0 ] && echo "  (empty -- no papers filed yet)"

echo
echo "########## uploads (should be empty apart from README.md) ##########"
pending="$(ls -A "$ROOT/survey/uploads" 2>/dev/null | grep -v '^README.md$')"
if [ -n "$pending" ]; then
    echo "$pending" | sed 's/^/  PENDING: /'
    echo "  -> file these per survey/uploads/README.md, then clear the directory."
else
    echo "  (clear)"
fi

echo
echo "########## consistency ##########"
readme="$ROOT/survey/README.md"
for d in "$PAPERS"/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    grep -q "$name" "$readme" 2>/dev/null || echo "  MISSING from survey/README.md: $name"
done
echo "  (nothing above == every paper directory is listed in survey/README.md)"
