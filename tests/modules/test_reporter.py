"""tests for reporter.py"""

from pathlib import Path

from saferepair.models import (
    Alert, RepairPattern, RepairResult, RepairStatus,
)
from saferepair.reporter import generate_run_report


def _make_alert(name, line, pattern, rule_id):
    return Alert(
        rule_id=rule_id,
        file_path=Path(f"/src/{name}"),
        line=line,
        column=1,
        message=f"Test alert for {name}",
        pattern=pattern,
    )


def _make_results():
    """mixed repair results covering all 4 patterns"""
    return [
        RepairResult(
            alert=_make_alert("file_a.c", 10, RepairPattern.INDEX_CHECK_AFTER_USE,
                              rule_id="V781"),
            status=RepairStatus.SUCCESS,
        ),
        RepairResult(
            alert=_make_alert("file_b.c", 5, RepairPattern.SUSPICIOUS_REALLOC,
                              rule_id="bugprone-suspicious-realloc-usage"),
            status=RepairStatus.SUCCESS,
        ),
        RepairResult(
            alert=_make_alert("file_c.c", 3, RepairPattern.MISSING_NULL_CHECK_MALLOC,
                              rule_id="CWE-690"),
            status=RepairStatus.SKIPPED,
        ),
        RepairResult(
            alert=_make_alert("file_d.c", 7, RepairPattern.SPRINTF_UNBOUNDED,
                              rule_id="CWE-120"),
            status=RepairStatus.SUCCESS,
        ),
    ]


# ---------------------------------------------------------------------------
# generate_run_report
# ---------------------------------------------------------------------------

def test_generate_run_report_structure(tmp_path):
    """generate_run_report() should write results.md with correct tables and GCC column"""
    all_repo_results = [
        {
            "name": "myrepo",
            "display": "owner/myrepo",
            "passed": 2,
            "skipped": 1,
            "failed": 0,
            "results": [
                {"file": "foo.c", "line": 10, "status": "PASS",
                 "detail": "fixed condition", "gcc": True},
                {"file": "bar.c", "line": 22, "status": "PASS",
                 "detail": "fixed condition", "gcc": False},
                {"file": "baz.c", "line": 5,  "status": "SKIP",
                 "detail": "no pattern found", "gcc": None},
            ],
        },
    ]

    out_path = generate_run_report(
        all_repo_results,
        "TEST_PATTERN",
        "TestHandler",
        tmp_path,
        notes=["Extra note for testing."],
    )

    assert out_path == tmp_path / "results.md"
    assert out_path.exists()
    content = out_path.read_text()

    assert "TEST_PATTERN Real-World Validation Results" in content
    assert "TestHandler" in content
    assert "owner/myrepo" in content
    assert "OK" in content          # gcc=True
    assert "FAIL" in content        # gcc=False
    assert "no pattern found" in content
    assert "Extra note for testing." in content


def test_generate_run_report_fix_rate(tmp_path):
    """Fix rate should be calculated correctly as passed/(passed+failed)"""
    all_repo_results = [
        {
            "name": "repo",
            "display": "a/repo",
            "passed": 3,
            "skipped": 2,
            "failed": 1,
            "results": [
                {"file": "x.c", "line": 1, "status": "PASS", "detail": "ok",   "gcc": True},
                {"file": "x.c", "line": 2, "status": "PASS", "detail": "ok",   "gcc": True},
                {"file": "x.c", "line": 3, "status": "PASS", "detail": "ok",   "gcc": True},
                {"file": "x.c", "line": 4, "status": "SKIP", "detail": "skip", "gcc": None},
                {"file": "x.c", "line": 5, "status": "SKIP", "detail": "skip", "gcc": None},
                {"file": "x.c", "line": 6, "status": "FAIL", "detail": "err",  "gcc": False},
            ],
        },
    ]

    out_path = generate_run_report(all_repo_results, "PAT", "Handler", tmp_path)
    content = out_path.read_text()

    assert "75%" in content         # fix rate = 3/(3+1)
    assert "PASS:** 3" in content
    assert "SKIP:** 2" in content
    assert "FAIL:** 1" in content
