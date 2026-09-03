#!/usr/bin/env bash
# Print the host state that matters to this project. Read-only, changes nothing.
#   bash Claude/scripts/check_host.sh
#
# This project is text-only (read papers, write a survey), so this checks the PDF
# toolchain and the network rather than GPUs. For the GPU/CUDA facts of this host see
# ~/moe_ws/moe_placement/Claude/instructions/ENVIRONMENT.md.

echo "########## 1. host ##########"
echo "hostname : $(hostname)"
echo "kernel   : $(uname -r)"
echo "date     : $(date +'%F %T')"

echo
echo "########## 2. disk ##########"
df -h /home 2>/dev/null
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
printf '  %-28s %s\n' "quantization_survey" "$(du -sh "$root" 2>/dev/null | cut -f1)"
printf '  %-28s %s\n' "survey/papers" "$(du -sh "$root/survey/papers" 2>/dev/null | cut -f1)"

echo
echo "########## 3. toolchain this project needs ##########"
for t in pdftotext pdfinfo curl git python3; do
    printf '  %-10s %s\n' "$t" "$(command -v "$t" || echo '<MISSING>')"
done
echo "  pdftotext version: $(pdftotext -v 2>&1 | head -1)"
echo "  python3          : $(python3 -V 2>&1)"
echo "  (no conda env needed: the scripts use stdlib + poppler-utils only)"

echo
echo "########## 4. network reachability ##########"
for u in https://arxiv.org https://api.crossref.org/works?rows=0; do
    code="$(curl -s -o /dev/null -w '%{http_code}' -m 15 "$u" 2>/dev/null)"
    printf '  %-42s %s\n' "$u" "${code:-<no response>}"
done
echo "  Subscription publishers (ACM DL / IEEE Xplore) return 403 to scripts by design."
echo "  Those go through survey/uploads/ -- see AGENT-GUIDE §3."

echo
echo "########## 5. survey status ##########"
bash "$root/Claude/scripts/check_survey.sh"
