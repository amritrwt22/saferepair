"""Scan all suspicious-realloc repos (using builtin CHECK) and write their alerts.json"""

import argparse
import logging
import re
from pathlib import Path
from config import SUSPICIOUS_REALLOC_REPOS
from script_utils import (
    collect_c_files,
    get_relative_path,
    run_clang_tidy,
    setup_logging,
    write_alerts_json,
)


logger = logging.getLogger(__name__)


#this builtin check auto flags realloc ptr uses without null check
CHECK = "bugprone-suspicious-realloc-usage"

_WARNING_RE = re.compile(  #matches clang-tidy warning line
    #file + line + col + warning msg + rulename
    r'^(?P<file>.+?):(?P<line>\d+):(?P<col>\d+):\s+warning:\s+(?P<msg>.+?)'
    r'\s+\[(?P<rule>[^\]]+)\]$'
)


def parse_output(raw: str, repo_path: Path) -> list[dict]:
    """parses raw clang-tidy output of a file.
       returns: alerts in a a dict.
    """

    #goes through each warning
    alerts = []
    for line in raw.splitlines():
        #skip if diff. format warning or not of CHECK rule
        m = _WARNING_RE.match(line)
        if not m or m.group("rule") != CHECK:
            continue

        alerts.append({
            "rule_id": CHECK,
            "file":    get_relative_path(Path(m.group("file")), repo_path),
            "line":    int(m.group("line")),
            "column":  int(m.group("col")),
            "message": m.group("msg"),
        })
    return alerts


def scan_repo(
    repo_path: Path, 
    includes: list[str], 
    extra_args: list[str], 
    verbose: bool
) -> list[dict]:
    """scans repo's .c files & returns alerts in a dict."""

    c_files = collect_c_files(repo_path)
    logger.info(f"Scanning {len(c_files)} .c files in {repo_path.name} ...")

    #-I used to include header paths so no type errors; only does -I for include dirs/headers that exist
    include_args = [f"--extra-arg=-I{repo_path / inc}" for inc in includes if (repo_path / inc).exists()]
    extra = [f"--extra-arg={a}" for a in extra_args] # any other flags repo might need

    all_alerts = []
    seen: set[tuple[str, int]] = set()     #set of tuples of (file, line_no)

    #scans each file
    for c_file in c_files:
        raw = run_clang_tidy(c_file, CHECK, include_args, extra, verbose)
        file_alerts = parse_output(raw, repo_path)

        #deduplicated cuz a realloc() call flagged each time a codepath reaches it without nullcheck 
        deduped = []
        for a in file_alerts:
            key = (a["file"], a["line"])
            if key not in seen:
                seen.add(key)
                deduped.append(a)

        if deduped:
            logger.info(f"  {c_file.relative_to(repo_path)}: {len(deduped)} hit(s)")
        all_alerts.extend(deduped)

    return all_alerts


def main():
    p = argparse.ArgumentParser(description="Scan all suspicious-realloc repos")
    p.add_argument("--verbose", "-v", action="store_true")       #syntax for adding flag
    args = p.parse_args()

    setup_logging(args.verbose)

    #scans all repos & writes their alerts.json
    for cfg in SUSPICIOUS_REALLOC_REPOS:
        repo_dir: Path = cfg["repo_dir"]
        if not repo_dir.is_dir():
            logger.warning(f"[SKIP] repo not found: {repo_dir}")
            continue
        alerts = scan_repo(repo_dir, cfg["includes"], cfg["extra_args"], args.verbose)
        logger.info(f"\nTotal: {len(alerts)} {CHECK} instance(s) in {cfg['display']}")
        write_alerts_json(alerts, cfg["alerts_json"])


if __name__ == "__main__":                 #main() only runs when executed directly, not when imported
    main()
