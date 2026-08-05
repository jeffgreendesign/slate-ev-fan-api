#!/bin/bash
# ============================================================================
# Security Check — Source-Level Security Scanning for Python
# ============================================================================
# Scans Python source files for common security anti-patterns:
#   1. Hardcoded secrets (API keys, passwords, tokens)
#   2. Dangerous function calls (eval, exec, os.system)
#   3. SQL injection patterns (string interpolation in SQL)
#   4. Unsafe deserialization (pickle.loads from untrusted sources)
#   5. Debug/dev settings left enabled
#
# Usage:
#   bash scripts/security-check.sh           # Warnings only (exit 0)
#   bash scripts/security-check.sh --strict  # Exit 1 on any finding
# ============================================================================
set -euo pipefail

STRICT=false
if [ "${1:-}" = "--strict" ]; then
  STRICT=true
fi

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

# Scan targets may be directories or individual files.
SCAN_TARGETS=("app" "main.py")
SCAN_LABEL="${SCAN_TARGETS[*]}"
FINDINGS=0

check_pattern() {
  local description="$1"
  local pattern="$2"
  local severity="$3"
  shift 3
  local exclude_patterns=("$@")

  local results
  results=$(grep -rnE "$pattern" "${SCAN_TARGETS[@]}" 2>/dev/null || true)

  # Apply exclusions (filter empties first)
  local filtered=()
  for exclude in "${exclude_patterns[@]}"; do
    [ -n "$exclude" ] && filtered+=("$exclude")
  done

  for exclude in "${filtered[@]}"; do
    results=$(echo "$results" | grep -v "$exclude" || true)
  done

  # Remove empty lines
  results=$(echo "$results" | sed '/^$/d')

  if [ -n "$results" ]; then
    FINDINGS=$((FINDINGS + 1))
    if [ "$severity" = "HIGH" ]; then
      echo -e "${RED}[$severity] $description${NC}"
    else
      echo -e "${YELLOW}[$severity] $description${NC}"
    fi
    echo "$results" | while IFS= read -r line; do
      echo "  $line"
    done
    echo ""
  fi
}

echo "============================================"
echo " Security Scan — $SCAN_LABEL"
echo "============================================"
echo ""

# ---- HIGH severity ----

check_pattern \
  "Hardcoded secrets (api_key, password, secret, token assigned to string literal)" \
  "(api_key|secret_key|password|token|secret)\s*=\s*['\"][^'\"]{8,}['\"]" \
  "HIGH" \
  "test_" "\.example" "^\s*#" "\.pyc"

check_pattern \
  "eval() or exec() usage — code injection risk" \
  "\beval\s*\(|\bexec\s*\(" \
  "HIGH" \
  ""

check_pattern \
  "os.system() usage — command injection risk" \
  "\bos\.system\s*\(" \
  "HIGH" \
  ""

check_pattern \
  "subprocess with shell=True — command injection risk" \
  "subprocess\.\w+\(.*shell\s*=\s*True" \
  "HIGH" \
  ""

# ---- MEDIUM severity ----

check_pattern \
  "SQL string interpolation (f-string with SQL keywords)" \
  "f['\"].*\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b" \
  "MEDIUM" \
  "ddl-identifiers-validated"

check_pattern \
  "SQL string interpolation (% formatting with SQL keywords)" \
  "['\"].*\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b.*%\s" \
  "MEDIUM" \
  ""

check_pattern \
  "Unsafe pickle deserialization" \
  "pickle\.loads?\s*\(" \
  "MEDIUM" \
  ""

check_pattern \
  "Debug mode enabled in production settings" \
  "(DEBUG\s*=\s*True|debug\s*=\s*True)" \
  "MEDIUM" \
  "test_" "\.example"

# ---- LOW severity ----

check_pattern \
  "Broad exception handling (bare except or Exception)" \
  "except\s*:|except\s+Exception\s*:" \
  "LOW" \
  "transactional-rollback-guard"

check_pattern \
  "TODO/FIXME/HACK comments (potential incomplete work)" \
  "#\s*(TODO|FIXME|HACK|XXX)\b" \
  "LOW" \
  ""

# ---- Summary ----
echo "============================================"
if [ "$FINDINGS" -eq 0 ]; then
  echo -e "${GREEN}No security findings.${NC}"
  exit 0
fi

echo -e "${YELLOW}Found $FINDINGS category(ies) with findings.${NC}"
echo "Review each finding above. False positives can be suppressed"
echo "by adding exclusion patterns to this script."

if [ "$STRICT" = true ]; then
  echo ""
  echo -e "${RED}--strict mode: exiting with error.${NC}"
  exit 1
fi

exit 0
