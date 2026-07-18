"""Tests for the index-check-after-use handler (PVS-Studio V781)."""

import subprocess
from pathlib import Path

import pytest

from saferepair.models import Alert, RepairPattern, RepairStatus
from saferepair.ast_analyzer import parse_file
from saferepair.source_rewriter import SourceRewriter
from saferepair.handlers.index_check_after_use import IndexCheckAfterUseHandler


@pytest.fixture
def handler():
    return IndexCheckAfterUseHandler()


def _create_c_file(tmp_path, name: str, content: str) -> Path:
    """Write a C file to tmp_path and return its path."""
    f = tmp_path / name
    f.write_text(content)
    return f


def _make_alert(file_path: Path, line: int, rule_id: str = "V781") -> Alert:
    """Create a V781 alert for the given file and line."""
    return Alert(
        rule_id=rule_id,
        file_path=file_path,
        line=line,
        column=5,
        message="Variable used as index before bound check",
        pattern=RepairPattern.INDEX_CHECK_AFTER_USE,
    )


# --------------------------------------------------------------------------- #
#  Routing                                                                     #
# --------------------------------------------------------------------------- #

def test_can_handle(handler):
    """Handler should accept INDEX_CHECK_AFTER_USE and reject all others."""
    yes = Alert("V781", Path("f.c"), 1, 0, "",
                pattern=RepairPattern.INDEX_CHECK_AFTER_USE)
    no = Alert("V781", Path("f.c"), 1, 0, "",
               pattern=RepairPattern.SUSPICIOUS_REALLOC)
    assert handler.can_handle(yes) is True
    assert handler.can_handle(no) is False


# --------------------------------------------------------------------------- #
#  Basic while loop                                                            #
# --------------------------------------------------------------------------- #

def test_basic_while_fix(handler, tmp_path):
    """while (buf[i] != '\\0' && i < len) should swap to (i < len && buf[i] != '\\0')."""
    src = _create_c_file(tmp_path, "while.c", (
        "#include <string.h>\n"
        "\n"
        "int scan(const char *buf, int len) {\n"
        "    int i = 0;\n"
        "    while (buf[i] != '\\0' && i < len) {\n"   # line 5
        "        i++;\n"
        "    }\n"
        "    return i;\n"
        "}\n"
    ))

    alert = _make_alert(src, line=5)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None, "analyze() should detect the V781 pattern"
    assert context["var"] == "i"
    assert "i < len" in context["right"]

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS
    assert len(result.edits) == 1

    patched = rewriter.apply()
    # Bound check must now come BEFORE the array access
    assert "i < len && buf[i]" in patched
    # Original buggy ordering must be gone
    assert "buf[i] != '\\0' && i < len" not in patched


# --------------------------------------------------------------------------- #
#  for-loop middle condition                                                   #
# --------------------------------------------------------------------------- #

def test_for_loop_fix(handler, tmp_path):
    """arr[k] != target && k < size in a for-loop condition should be swapped."""
    src = _create_c_file(tmp_path, "for.c", (
        "int find_val(int *arr, int size, int target) {\n"
        "    int k;\n"
        "    for (k = 0; arr[k] != target && k < size; k++) {}\n"  # line 3
        "    return k;\n"
        "}\n"
    ))

    alert = _make_alert(src, line=3)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None, "analyze() should detect V781 in for-loop condition"
    assert context["var"] == "k"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "k < size && arr[k]" in patched
    assert "arr[k] != target && k < size" not in patched


# --------------------------------------------------------------------------- #
#  if-statement condition                                                      #
# --------------------------------------------------------------------------- #

def test_if_condition_fix(handler, tmp_path):
    """data[idx] > 0 && idx < count in an if-condition should be swapped."""
    src = _create_c_file(tmp_path, "if.c", (
        "int check(int *data, int count, int idx) {\n"
        "    if (data[idx] > 0 && idx < count) {\n"    # line 2
        "        return 1;\n"
        "    }\n"
        "    return 0;\n"
        "}\n"
    ))

    alert = _make_alert(src, line=2)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None, "analyze() should detect V781 in if-condition"
    assert context["var"] == "idx"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "idx < count && data[idx]" in patched
    assert "data[idx] > 0 && idx < count" not in patched


# --------------------------------------------------------------------------- #
#  Already-safe: correct order, should be skipped                             #
# --------------------------------------------------------------------------- #

def test_already_safe_skip(handler, tmp_path):
    """(i < len && buf[i] != '\\0') is already correct — analyze() must return None."""
    src = _create_c_file(tmp_path, "safe.c", (
        "int scan(const char *buf, int len) {\n"
        "    int i = 0;\n"
        "    while (i < len && buf[i] != '\\0') {\n"   # line 3 — correct order
        "        i++;\n"
        "    }\n"
        "    return i;\n"
        "}\n"
    ))

    alert = _make_alert(src, line=3)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is None, (
        "analyze() should return None for already-safe (correct-order) condition"
    )


# --------------------------------------------------------------------------- #
#  Side-effect guard: ++ in array index — must NOT swap                       #
# --------------------------------------------------------------------------- #

def test_side_effect_skip(handler, tmp_path):
    """(a[iOff++] & 0x80) && iOff < iEnd has a side effect — must be skipped."""
    src = _create_c_file(tmp_path, "side_effect.c", (
        "int read_vlq(unsigned char *a, int iEnd) {\n"
        "    int iOff = 0;\n"
        "    while ((a[iOff++] & 0x80) && iOff < iEnd) {}\n"   # line 3
        "    return iOff;\n"
        "}\n"
    ))

    alert = _make_alert(src, line=3)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is None, (
        "analyze() must return None when the left operand has a side effect (++)"
    )


# --------------------------------------------------------------------------- #
#  Multi-part && condition                                                     #
# --------------------------------------------------------------------------- #

def test_multi_and_fix(handler, tmp_path):
    """arr[i] != 0 && i < n && flag: only the first V781 pair should be swapped."""
    src = _create_c_file(tmp_path, "multi.c", (
        "int scan_all(int *arr, int n, int flag) {\n"
        "    int i = 0;\n"
        "    while (arr[i] != 0 && i < n && flag) {\n"    # line 3
        "        i++;\n"
        "    }\n"
        "    return i;\n"
        "}\n"
    ))

    alert = _make_alert(src, line=3)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None
    assert context["var"] == "i"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    # Bound check must precede the array access in the patched output
    assert "i < n && arr[i]" in patched
    assert "arr[i] != 0 && i < n" not in patched


# --------------------------------------------------------------------------- #
#  End-to-end: patched file must compile                                      #
# --------------------------------------------------------------------------- #

def test_patched_file_compiles(handler, tmp_path):
    """Verify the patched output is syntactically valid C (gcc -fsyntax-only)."""
    src = _create_c_file(tmp_path, "compile_check.c", (
        "int count_nonzero(int *arr, int len) {\n"
        "    int i = 0, count = 0;\n"
        "    while (arr[i] != 0 && i < len) {\n"   # line 3
        "        count++;\n"
        "        i++;\n"
        "    }\n"
        "    return count;\n"
        "}\n"
    ))

    alert = _make_alert(src, line=3)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    output = tmp_path / "patched.c"
    rewriter.write(output)

    gcc = subprocess.run(
        ["gcc", "-c", "-fsyntax-only", str(output)],
        capture_output=True, text=True,
    )
    assert gcc.returncode == 0, (
        f"Patched file failed to compile:\n{gcc.stderr}"
    )
