Run all quality gates on the codebase:

1. Run `python -m pytest` (all tests including architecture guardrails)
2. Run `bash scripts/security-check.sh` (source-level security scan)
3. Report results for each gate
4. If any gate fails, identify the specific errors and fix them
5. Do NOT proceed with committing until all gates pass
