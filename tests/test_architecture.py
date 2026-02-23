"""
Architecture Guardrail Tests — Slate EV Fan API
============================================================================
Enforces architectural rules using AST parsing. Catches violations at test
time before they make it into the codebase.

Adapted from jeffgreendesign/project-scaffold.

WHAT IT ENFORCES:
1. Single database access point — only app/db/session.py may call create_engine
2. No dangerous functions — eval(), exec(), os.system() are banned in app code
3. Endpoint registration — every router in app/api/ is included in main.py

HOW TO CUSTOMIZE:
- Update the constants at the top of each test class
- Add/remove tests based on your project's architecture
============================================================================
"""

import ast
import os
import unittest
from pathlib import Path
from typing import NamedTuple


class Violation(NamedTuple):
    file: str
    line: int
    message: str


# ============================================================================
# Project-specific constants
# ============================================================================

# Root directory to scan (application code only)
APP_DIR = "app"

# The single file allowed to create the database engine
DB_MODULE = "app/db/session.py"

# Functions/imports that should only appear in the DB module
FORBIDDEN_DB_PATTERNS = [
    "create_engine",
]

# Dangerous functions banned from all application code
DANGEROUS_FUNCTIONS = [
    "eval",
    "exec",
]

# Dangerous attribute calls banned from all application code
DANGEROUS_ATTR_CALLS = [
    ("os", "system"),
    ("os", "popen"),
]

# Main application file where routers are registered
MAIN_FILE = "main.py"

# Directory containing endpoint files
API_DIR = "app/api"


def get_python_files(directory: str) -> list[str]:
    """Recursively get all Python files in a directory."""
    files = []
    root = Path(directory)

    if not root.exists():
        return files

    for path in root.rglob("*.py"):
        parts = path.parts
        if any(
            p in ("__pycache__", ".venv", "venv", "node_modules", ".git")
            for p in parts
        ):
            continue
        # Skip test files
        if path.name.startswith("test_") or path.name.endswith("_test.py"):
            continue
        files.append(str(path))

    return files


def parse_file(filepath: str) -> ast.Module | None:
    """Parse a Python file into an AST, returning None on failure."""
    try:
        with open(filepath, encoding="utf-8") as f:
            return ast.parse(f.read(), filename=filepath)
    except (SyntaxError, UnicodeDecodeError):
        return None


class TestDatabaseAccessBoundary(unittest.TestCase):
    """
    Enforces single database access point.

    Rule: Only app/db/session.py may call create_engine.
    Bug: Direct engine creation bypasses connection pooling and session management.
    Prevent: AST scanning catches create_engine imports outside the approved module.
    """

    def test_no_direct_engine_creation(self) -> None:
        violations: list[Violation] = []
        files = get_python_files(APP_DIR)
        allowed = os.path.normpath(DB_MODULE)

        # NOTE: This scanner checks "from X import create_engine" (ast.ImportFrom)
        # and "sqlalchemy.create_engine(...)" calls (ast.Call/ast.Attribute).
        # It does NOT resolve aliases (e.g. "import sqlalchemy as sa;
        # sa.create_engine(...)") or re-exports. Full import resolution is
        # out of scope for this guardrail test.
        for filepath in files:
            normalized = os.path.normpath(filepath)
            if normalized == allowed:
                continue

            tree = parse_file(filepath)
            if tree is None:
                continue

            for node in ast.walk(tree):
                # Check 'from sqlalchemy import create_engine'
                if isinstance(node, ast.ImportFrom) and node.module:
                    for alias in node.names:
                        if alias.name in FORBIDDEN_DB_PATTERNS:
                            violations.append(
                                Violation(
                                    file=filepath,
                                    line=node.lineno,
                                    message=(
                                        f"Direct import of '{alias.name}' from "
                                        f"'{node.module}' — use app.db.session instead"
                                    ),
                                )
                            )

                # Check attribute-style calls: sqlalchemy.create_engine(...)
                if isinstance(node, ast.Call):
                    if (
                        isinstance(node.func, ast.Attribute)
                        and node.func.attr in FORBIDDEN_DB_PATTERNS
                        and isinstance(node.func.value, ast.Name)
                        and node.func.value.id == "sqlalchemy"
                    ):
                        violations.append(
                            Violation(
                                file=filepath,
                                line=node.lineno,
                                message=(
                                    f"Direct call to sqlalchemy.{node.func.attr}() — "
                                    f"use app.db.session instead"
                                ),
                            )
                        )

        if violations:
            msg = f"\nFound {len(violations)} forbidden DB import(s):\n\n"
            for v in violations:
                msg += f"  {v.file}:{v.line} — {v.message}\n"
            msg += f"\nOnly {DB_MODULE} may call create_engine."
            self.fail(msg)


class TestNoDangerousPatterns(unittest.TestCase):
    """
    Enforces that dangerous functions are not used in application code.

    Rule: eval(), exec(), os.system(), os.popen() are banned.
    Bug: These functions enable code injection and command injection.
    Prevent: AST scanning catches calls to these functions.
    """

    def test_no_eval_exec(self) -> None:
        violations: list[Violation] = []
        files = get_python_files(APP_DIR)

        for filepath in files:
            tree = parse_file(filepath)
            if tree is None:
                continue

            # NOTE: This scanner checks bare names (eval, exec) and module.attr
            # patterns (os.system, os.popen). It does NOT resolve aliases or
            # direct imports like "from os import system; system(...)".
            # Full import resolution is out of scope for this guardrail test.
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Check bare function calls: eval(...), exec(...)
                    if (
                        isinstance(node.func, ast.Name)
                        and node.func.id in DANGEROUS_FUNCTIONS
                    ):
                        violations.append(
                            Violation(
                                file=filepath,
                                line=node.lineno,
                                message=f"Call to {node.func.id}() — banned in app code",
                            )
                        )

                    # Check attribute calls: os.system(...), os.popen(...)
                    if isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            for mod, func in DANGEROUS_ATTR_CALLS:
                                if (
                                    node.func.value.id == mod
                                    and node.func.attr == func
                                ):
                                    violations.append(
                                        Violation(
                                            file=filepath,
                                            line=node.lineno,
                                            message=(
                                                f"Call to {mod}.{func}() — "
                                                f"banned in app code"
                                            ),
                                        )
                                    )

        if violations:
            msg = f"\nFound {len(violations)} dangerous function call(s):\n\n"
            for v in violations:
                msg += f"  {v.file}:{v.line} — {v.message}\n"
            msg += "\nUse safe alternatives (subprocess.run with shell=False, etc.)."
            self.fail(msg)


def _get_registered_modules(main_file: str) -> set[str]:
    """Extract API module names registered in main.py via AST analysis.

    Walks the AST to find imports from app.api.* and include_router calls,
    so that matches in comments or strings don't cause false positives.
    """
    tree = parse_file(main_file)
    if tree is None:
        return set()

    registered = set()
    router_vars: dict[str, str] = {}  # variable name -> module name

    for node in ast.walk(tree):
        # Track "from app.api.<module> import router [as alias]"
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("app.api."):
                module_name = node.module.rsplit(".", 1)[-1]
                for alias in node.names:
                    var_name = alias.asname if alias.asname else alias.name
                    router_vars[var_name] = module_name

        # Track "<app>.include_router(<var>, ...)" calls
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "include_router" and node.args:
                arg = node.args[0]
                if isinstance(arg, ast.Name) and arg.id in router_vars:
                    registered.add(router_vars[arg.id])

    return registered


class TestEndpointRegistration(unittest.TestCase):
    """
    Enforces that every endpoint module is registered in main.py.

    Rule: Every .py file in app/api/ that defines a router must be imported in main.py.
    Bug: New endpoints that aren't registered are silently unreachable.
    Prevent: This test compares API modules to main.py imports.
    """

    def test_all_api_routers_registered(self) -> None:
        if not os.path.exists(API_DIR):
            self.skipTest(f"No API directory at {API_DIR}")

        if not os.path.exists(MAIN_FILE):
            self.skipTest(f"No main file at {MAIN_FILE}")

        # Find all non-__init__ Python files in app/api/
        api_modules = set()
        for filepath in get_python_files(API_DIR):
            module_name = Path(filepath).stem
            if module_name != "__init__":
                api_modules.add(module_name)

        if not api_modules:
            return

        # Use AST analysis to find modules actually registered via include_router
        registered = _get_registered_modules(MAIN_FILE)

        unregistered = []
        for module in sorted(api_modules):
            if module not in registered:
                unregistered.append(module)

        if unregistered:
            msg = f"\nFound {len(unregistered)} unregistered endpoint module(s):\n\n"
            for module in unregistered:
                msg += f"  - {module} (in {API_DIR}/{module}.py)\n"
            msg += f"\nRegister them in {MAIN_FILE} with include_router()."
            self.fail(msg)


if __name__ == "__main__":
    unittest.main()
