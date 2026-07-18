## Clone repos

Clones all repos into `scripts/repos/`. Safe to re-run — already cloned repos are skipped.
For sqlite and cpython, only the specific source file needed (sqlite3.c / lexer.c) is
downloaded rather than cloning the full repo.

```bash
python scripts/clone_repos.py
```

---

## Scan repos (generate alerts.json)

Scans all repos for a pattern and writes their `alerts.json` files. 
All paths are hardcoded — no arguments needed.
Run from project root using the venv Python:

```bash
.venv/Scripts/python.exe scripts/scan_suspicious_realloc.py    [--verbose]
.venv/Scripts/python.exe scripts/scan_missing_null_check.py    [--verbose]
.venv/Scripts/python.exe scripts/scan_index_check_after_use.py [--verbose]
.venv/Scripts/python.exe scripts/scan_sprintf_snprintf.py      [--verbose]
```

Each script iterates all repos for its pattern (defined in `scripts/config.py`),
skips any whose `repo_dir` is not present, and writes `alerts.json` for each repo
that was scanned.

Re-running is safe — `alerts.json` files are unconditionally overwritten.
Only needed if regenerating alerts from scratch; committed `alerts.json` files are
already present and correct.

---

## Run real-world validation

All paths are hardcoded — no arguments needed.
Run from project root using the venv Python:

```bash
.venv/Scripts/python.exe scripts/run_missing_null_check.py
.venv/Scripts/python.exe scripts/run_suspicious_realloc.py
.venv/Scripts/python.exe scripts/run_sprintf_snprintf.py
.venv/Scripts/python.exe scripts/run_index_check_after_use.py
```

Exit code 0 = all repairs passed (no FAILs). Exit code 1 = at least one FAIL.

Output written to `test_suite/real_world/<pattern>/results.md`.

Re-running is safe — all output files are unconditionally overwritten.
Only re-run after changing handler logic in `saferepair/handlers/`.

---

## Running tests

Run from project root (`C:\Users\ammar\projects\btp\`):

```bash
# run entire test suite
.venv/Scripts/python.exe -m pytest tests/ -v

# run a specific file or folder
.venv/Scripts/python.exe -m pytest tests/modules/test_alert_parser.py -v
```

`.venv/Scripts/python.exe`: to use project's vir. env., not system Python
`-m pytest`: runs pytest as a module, explicit about which Python
`tests/`: directory (discovers all `test_*.py` files recursively)
`-v`: verbose output, pytest shows each test name & PASSED/FAILED

---

## Logging

All scripts log to **stderr** via Python's `logging` module, configured by
`setup_logging()` in `script_utils.py`.

**Scan scripts** (`scan_*.py`) accept `--verbose` / `-v`:
- Default (no flag): INFO level — repo name, file hit counts, total alert count.
- `--verbose`: DEBUG level — adds per-line candidate conditions, skip reasons, and clang-tidy commands.

**Run scripts** (`run_*.py`) have no `--verbose` flag — they always run at INFO level,
printing `[PASS]` / `[SKIP]` / `[FAIL]` per alert and a summary line per repo.

**`clone_repos.py`** uses plain `print()` (no logging) — outputs one status line
(`cloned` / `skipped` / `error: ...`) per repo, then a final summary.

**`saferepair/` internals** (pipeline, handlers, reporter, validator) use module-level
loggers throughout. Their output appears when a run or scan script is active — no
separate configuration needed.
