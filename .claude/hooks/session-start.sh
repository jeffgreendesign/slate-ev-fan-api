#!/bin/bash
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(pwd)}"
cd "$PROJECT_DIR"

echo "--- Session start: installing dependencies ---"

if [ -f "requirements.txt" ]; then
  PIP_CMD="pip"
  if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo "⚠ No virtual environment detected — using python -m pip"
    PIP_CMD="python -m pip"
  fi
  $PIP_CMD install -r requirements.txt --quiet 2>&1
elif [ -f "pyproject.toml" ]; then
  PIP_CMD="pip"
  if [ -z "${VIRTUAL_ENV:-}" ]; then
    echo "⚠ No virtual environment detected — using python -m pip"
    PIP_CMD="python -m pip"
  fi
  if grep -qE '\[project\.optional-dependencies\]' pyproject.toml && grep -qE '^\s*dev\s*=' pyproject.toml; then
    $PIP_CMD install -e ".[dev]" --quiet 2>&1
  else
    $PIP_CMD install -e . --quiet 2>&1
  fi
else
  echo "⚠ No requirements.txt or pyproject.toml found — skipping dependency install"
fi

echo "--- Session start complete ---"
