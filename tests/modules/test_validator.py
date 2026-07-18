"""tests for validator.py"""

from saferepair.validator import compile_check, validate_repairs
from saferepair.models import (
    Alert, RepairPattern, RepairResult, RepairStatus
)


def _create_c_file(tmp_path, name, content):
    """write a C file and return its path"""
    f = tmp_path / name
    f.write_text(content)
    return f


def _make_alert(file_path, line, pattern=RepairPattern.MISSING_NULL_CHECK_MALLOC):
    """create a test alert with a neutral default pattern"""
    return Alert(
        rule_id="CWE-690",
        file_path=file_path,
        line=line,
        column=1,
        message="Test alert",
        pattern=pattern,
    )


# ---------------------------------------------------------------------------
# compile_check
# ---------------------------------------------------------------------------

def test_valid_file_compiles(tmp_path):
    """A correct C file should compile successfully."""
    src = _create_c_file(tmp_path, "good.c", """\
        #include <stdlib.h>

        int main(void) {
            int x = 42;
            return x;
        }
        """)
    result = compile_check(src)
    assert result.success is True
    assert result.return_code == 0
    assert result.file_path == src


def test_broken_file_fails(tmp_path):
    """A C file with syntax errors should fail compilation"""
    src = _create_c_file(tmp_path, "bad.c", """\
        int main(void) {
            int x = 42
            return x;
        }
        """)
    result = compile_check(src)
    assert result.success is False
    assert result.return_code != 0
    assert len(result.output) > 0  # error message captured


def test_missing_gcc_graceful(tmp_path):
    """using nonexistent compiler should return failure, not raise"""
    src = _create_c_file(tmp_path, "test.c", "int main(void) { return 0; }\n")
    result = compile_check(src, compiler="nonexistent_gcc_xyz_12345")
    assert result.success is False
    assert "not found" in result.output.lower()
    assert result.return_code == -1


# ---------------------------------------------------------------------------
# validate_repairs
# ---------------------------------------------------------------------------

def test_validate_repairs_with_patched_files(tmp_path):
    """validate repairs should compile-check successfully repaired files."""
    src1 = _create_c_file(tmp_path, "file_a.c", "int main(void) { return 0; }\n")
    src2 = _create_c_file(tmp_path, "file_b.c", "int foo(void) { return 1; }\n")

    results = [
        RepairResult(alert=_make_alert(src1, 1), status=RepairStatus.SUCCESS),
        RepairResult(alert=_make_alert(src2, 1), status=RepairStatus.SUCCESS),
    ]

    validations = validate_repairs(tmp_path, results)
    assert len(validations) == 2
    for v in validations:
        assert v.compile_result.success is True


def test_validate_repairs_skips_non_success(tmp_path):
    """Only SUCCESS results should be validated, not SKIPPED/FAILED."""
    src1 = _create_c_file(tmp_path, "skipped.c", "int main(void) { return 0; }\n")
    src2 = _create_c_file(tmp_path, "failed.c", "int foo(void) { return 1; }\n")

    results = [
        RepairResult(alert=_make_alert(src1, 1), status=RepairStatus.SKIPPED),
        RepairResult(alert=_make_alert(src2, 1), status=RepairStatus.FAILED),
    ]

    validations = validate_repairs(tmp_path, results)
    assert len(validations) == 0


def test_validate_repairs_broken_file_detected(tmp_path):
    """patched file with a syntax error should show compile failure"""
    src = _create_c_file(tmp_path, "broken.c", "int main(void) { int x = 42\n")  # missing semicolon

    results = [
        RepairResult(alert=_make_alert(src, 1), status=RepairStatus.SUCCESS),
    ]

    validations = validate_repairs(tmp_path, results)
    assert len(validations) == 1
    assert validations[0].compile_result.success is False
