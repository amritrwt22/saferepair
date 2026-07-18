"""Report generator for SafeRepair repair results."""

import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def generate_run_report(
    all_repo_results: list[dict],
    pattern_name: str,
    handler_name: str,
    output_path: Path,
    notes: list[str] | None = None,
) -> Path:
    """writes markdown validation report results.md for real-world run scripts

    all_repo_results: list of dicts with keys:
        name, display, passed, skipped, failed,
        results: list of {file, line, status, detail, gcc}
            gcc: True (OK) | False (FAIL) | None (not compiled)
    """

    total_pass  = sum(r["passed"]  for r in all_repo_results)
    total_skip  = sum(r["skipped"] for r in all_repo_results)
    total_fail  = sum(r["failed"]  for r in all_repo_results)
    total_alerts = total_pass + total_skip + total_fail
    denom = total_pass + total_fail
    rate_str = f"{100*total_pass//denom}%" if denom else "n/a"

    lines = [
        f"# {pattern_name} Real-World Validation Results",
        "",
        f"**Pattern:** `{pattern_name}`",
        f"**Handler:** `{handler_name}`",
        f"**Repos scanned:** {len(all_repo_results)}",
        f"**Total alerts:** {total_alerts}",
        f"**PASS:** {total_pass} | **SKIP:** {total_skip} | **FAIL:** {total_fail}",
        f"**Fix rate (PASS/PASS+FAIL):** {total_pass}/{denom} ({rate_str})",
        "",
        "## Per-Repo Summary",
        "",
        "| Repo | Alerts | PASS | SKIP | FAIL | Fix Rate |",
        "|------|--------|------|------|------|----------|",
    ]

    for r in all_repo_results:
        d = r["passed"] + r["failed"]
        rate = f"{100*r['passed']//d}%" if d else "n/a"
        total = r["passed"] + r["skipped"] + r["failed"]
        lines.append(
            f"| `{r['display']}` | {total} | {r['passed']} "
            f"| {r['skipped']} | {r['failed']} | {rate} |"
        )

    lines += [
        "",
        "## Per-Instance Detail",
        "",
        "| Repo | File | Line | Status | Detail | GCC |",
        "|------|------|------|--------|--------|-----|",
    ]

    for r in all_repo_results:
        for row in r["results"]:
            gcc_val = row.get("gcc")
            if gcc_val is True:
                gcc_label = "OK"
            elif gcc_val is False:
                gcc_label = "FAIL"
            else:
                gcc_label = "—"
            lines.append(
                f"| `{r['display']}` | `{row['file']}` | {row['line']} "
                f"| **{row['status']}** | {row['detail']} | {gcc_label} |"
            )

    lines += ["", "## Notes", ""]
    lines.append("- **SKIP** is correct behaviour when analyze() returns None: "
                 "pattern not confirmed in AST, or already fixed.")
    if notes:
        for note in notes:
            lines.append(f"- {note}")

    out_path = output_path / "results.md"
    output_path.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    logger.info(f"Wrote run report: {out_path}")
    return out_path
