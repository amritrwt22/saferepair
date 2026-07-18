"""Shared utilities for all scan_*.py & run_*.py scripts"""

import json
import logging
import subprocess
import sys
from pathlib import Path


# insert project root in sys.path so 'import saferepair' works (elsw Python will look in scripts/ for the package)
sys.path.insert(0, str(Path(__file__).parent.parent))

logger = logging.getLogger(__name__)

CLANG_TIDY = "clang-tidy"


#configure root logger with clean formatter
def setup_logging(verbose: bool = False) -> None:
    class _Fmt(logging.Formatter):
        def format(self, record):
            self._style._fmt = (
                "%(message)s" if record.levelno < logging.WARNING   # INFO, DEBUG messages print message text
                else "%(levelname)s: %(message)s"     #Warning n abpve print lebel name too
            )
            return super().format(record)

    _h = logging.StreamHandler()   #creates handler that writes log output to console
    _h.setFormatter(_Fmt())        #attaches custom formatter to handler
    logging.root.addHandler(_h)    #attaches handler to root logger
    logging.root.setLevel(logging.DEBUG if verbose else logging.INFO)


#sorted rglob of all *.c files under a path
def collect_c_files(repo_path: Path) -> list[Path]:
    return sorted(repo_path.rglob("*.c"))


#relative path string, falls back to filename
def get_relative_path(file_abs: Path, repo_path: Path) -> str:
    try:
        return str(file_abs.relative_to(repo_path))
    except ValueError:
        return file_abs.name


#mkdir + json.dump alerts list to file
def write_alerts_json(alerts: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2)
    logger.info(f"Written to {out_path}")


def run_clang_tidy(
    c_file: Path,
    check: str,
    include_args: list[str],
    extra_args: list[str],
    verbose: bool,
) -> str:
    """run clang-tidy on a .c file.
       returns: raw o/p from stdout & stderr.
    """
    cmd = [
        CLANG_TIDY,
        f"--checks=-*,{check}",     # disable all checks except {check}
        "--header-filter=^$",       #ignore warnings from header files
    ] + include_args + extra_args + [str(c_file)]

    if verbose:
        logger.debug(f"  CMD: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        logger.warning(f"  TIMEOUT: {c_file.name}")
        return ""
    except FileNotFoundError:
        logger.error("clang-tidy not found in PATH.")
        sys.exit(1)
    except Exception as e:
        logger.warning(f"  ERROR on {c_file.name}: {e}")
        return ""


def process_repo(cfg: dict) -> dict:
    """run repair pipeline on a repo & return a stats dict."""
    #here cuz whole module doesnt need these big packages
    from saferepair.pipeline import repair_pipeline
    from saferepair.models import RepairStatus
    from saferepair.validator import validate_repairs

    name: str = cfg["name"]
    display: str = cfg["display"]
    repo_dir: Path = cfg["repo_dir"]
    alerts_json: Path = cfg["alerts_json"]
    out_dir: Path = cfg["out_dir"]

    logger.info(f"\n{'='*60}")
    logger.info(f"  Repo: {display}")
    logger.info(f"{'='*60}")

    if not alerts_json.exists():
        logger.warning(f"  [SKIP] alerts.json not found: {alerts_json}")
        return {"name": name, "display": display, "results": [],
                "passed": 0, "skipped": 0, "failed":   0}

    results, _ = repair_pipeline(alerts_json, repo_dir, out_dir)  #list[RepairResult]
    validations = validate_repairs(out_dir, results)
    gcc_by_file = {v.file_path.name: v.compile_result.success for v in validations}   #filename->bool dict storing whther compile check worked

    # creates dict to be returned & used by reporter.py
    row_results = []
    passed = skipped = failed = 0
    for r in results:
        if r.status == RepairStatus.SUCCESS:
            detail = r.edits[0].description if r.edits else ""
            status = "PASS"
            passed += 1
        elif r.status == RepairStatus.SKIPPED:
            detail = r.error_message or "analyze() returned None"
            status = "SKIP"
            skipped += 1
        else:
            detail = r.error_message or "generate_fix failed"
            status = "FAIL"
            failed += 1
        row_results.append({
            "file": r.alert.file_path.name,
            "line": r.alert.line,
            "status": status,
            "detail": detail,
            "gcc": gcc_by_file.get(r.alert.file_path.name),
        })
        logger.info(f"    [{status}] {r.alert.file_path.name}:{r.alert.line} -- {detail}")
    logger.info(f"  PASS={passed}  SKIP={skipped}  FAIL={failed}")

    return {"name": name, "display": display, "results": row_results,
            "passed": passed, "skipped": skipped, "failed": failed}
