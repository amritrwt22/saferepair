"""tests if SafeRepair models.py storing correct data"""

from pathlib import Path
from saferepair.models import (
    Alert, SourceEdit, RepairResult, CompileResult, ValidationResult,
    RepairPattern, RepairStatus,
)


# ---------------------------------------------------------------------------
# RepairPattern
# ---------------------------------------------------------------------------

def test_repair_pattern_enum_values():
    assert RepairPattern.SUSPICIOUS_REALLOC.value        == "suspicious_realloc"
    assert RepairPattern.MISSING_NULL_CHECK_MALLOC.value == "missing_null_check_malloc"
    assert RepairPattern.INDEX_CHECK_AFTER_USE.value     == "index_check_after_use"
    assert RepairPattern.SPRINTF_UNBOUNDED.value         == "sprintf_unbounded"


# ---------------------------------------------------------------------------
# RepairStatus
# ---------------------------------------------------------------------------

def test_repair_status_enum_values():
    assert RepairStatus.SUCCESS.value == "success"
    assert RepairStatus.FAILED.value  == "failed"
    assert RepairStatus.SKIPPED.value == "skipped"


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------

def test_alert_creation():
    alert = Alert(
        rule_id="bugprone-suspicious-realloc-usage",
        file_path=Path("test.c"),
        line=10,
        column=5,
        message="suspicious realloc",
    )
    assert alert.rule_id == "bugprone-suspicious-realloc-usage"
    assert alert.line == 10
    assert alert.pattern is None  # not yet classified


def test_alert_str():
    alert = Alert(
        rule_id="CWE-690",
        file_path=Path("foo.c"),
        line=42,
        column=1,
        message="malloc return unchecked",
    )
    s = str(alert)
    assert "foo.c" in s
    assert "42" in s
    assert "CWE-690" in s


# ---------------------------------------------------------------------------
# SourceEdit
# ---------------------------------------------------------------------------

def test_source_edit_creation():
    edit = SourceEdit(
        file_path=Path("test.c"),
        line=5,
        old_text="int *p = malloc(n);",
        new_text="int *p = malloc(n);\nif (!p) return NULL;",
        description="add null check after malloc",
    )
    assert edit.line == 5
    assert edit.file_path == Path("test.c")
    assert "null check" in edit.description


def test_source_edit_str():
    edit = SourceEdit(
        file_path=Path("foo.c"),
        line=10,
        old_text="old",
        new_text="new",
        description="replaced line",
    )
    s = str(edit)
    assert "foo.c" in s
    assert "10" in s
    assert "replaced line" in s


# ---------------------------------------------------------------------------
# RepairResult
# ---------------------------------------------------------------------------

def test_repair_result_defaults():
    alert = Alert("rule", Path("f.c"), 1, 0, "msg")
    result = RepairResult(alert=alert, status=RepairStatus.SUCCESS)
    assert result.success is True
    assert result.edits == []
    assert result.original_source == ""
    assert result.patched_source == ""
    assert result.error_message == ""


def test_repair_result_failed():
    alert = Alert("rule", Path("f.c"), 1, 0, "msg")
    result = RepairResult(
        alert=alert,
        status=RepairStatus.FAILED,
        error_message="could not parse",
    )
    assert result.success is False
    assert result.error_message == "could not parse"


def test_repair_result_skipped():
    alert = Alert("rule", Path("f.c"), 1, 0, "msg")
    result = RepairResult(alert=alert, status=RepairStatus.SKIPPED)
    assert result.success is False


def test_repair_result_edits_not_shared():
    """mutable default: each RepairResult must get its own edits list"""
    a = Alert("r", Path("f.c"), 1, 0, "m")
    r1 = RepairResult(alert=a, status=RepairStatus.SUCCESS)
    r2 = RepairResult(alert=a, status=RepairStatus.SUCCESS)
    r1.edits.append(SourceEdit(Path("f.c"), 1, "old", "new", "desc"))
    assert r2.edits == []


# ---------------------------------------------------------------------------
# CompileResult
# ---------------------------------------------------------------------------

def test_compile_result_success():
    cr = CompileResult(file_path=Path("out.c"), success=True, output="", return_code=0)
    assert cr.success is True
    assert cr.return_code == 0


def test_compile_result_failure():
    cr = CompileResult(
        file_path=Path("bad.c"),
        success=False,
        output="error: expected ';'",
        return_code=1,
    )
    assert cr.success is False
    assert cr.return_code != 0
    assert len(cr.output) > 0


# ---------------------------------------------------------------------------
# ValidationResult
# ---------------------------------------------------------------------------

def test_validation_result():
    cr = CompileResult(file_path=Path("ok.c"), success=True, output="", return_code=0)
    vr = ValidationResult(file_path=Path("ok.c"), compile_result=cr)
    assert vr.compile_result.success is True
    assert vr.file_path == Path("ok.c")
