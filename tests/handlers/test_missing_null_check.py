"""tests for missing_null_check.py handler"""

import subprocess
from pathlib import Path
import pytest

from saferepair.models import Alert, RepairPattern, RepairStatus
from saferepair.ast_analyzer import parse_file
from saferepair.source_rewriter import SourceRewriter
from saferepair.handlers.missing_null_check import MissingNullCheckHandler


@pytest.fixture
def handler():
    return MissingNullCheckHandler()


def _create_c_file(tmp_path, name, content):
    """Write a C file and return its path."""
    f = tmp_path / name
    f.write_text(content)
    return f


def _make_alert(file_path, line):
    """Create a CWE-690 alert for a given file and line."""
    return Alert(
        rule_id="CWE-690",
        file_path=file_path,
        line=line,
        column=5,
        message="Value stored is the result of a malloc call and might be NULL",
        pattern=RepairPattern.MISSING_NULL_CHECK_MALLOC,
    )


# ---------------------------------------------------------------------------
# can_handle
# ---------------------------------------------------------------------------

def test_can_handle(handler):
    """handler should only accept MISSING_NULL_CHECK_MALLOC pattern."""
    alert_yes = Alert("CWE-690", Path("f.c"), 1, 0, "msg",
                      pattern=RepairPattern.MISSING_NULL_CHECK_MALLOC)
    alert_no = Alert("rule", Path("f.c"), 1, 0, "msg",
                     pattern=RepairPattern.SUSPICIOUS_REALLOC)
    assert handler.can_handle(alert_yes) is True
    assert handler.can_handle(alert_no) is False


# ---------------------------------------------------------------------------
# Basic fix: pointer-returning function
# ---------------------------------------------------------------------------

def test_basic_fix(handler, tmp_path):
    """malloc without NULL check should get a NULL guard inserted"""
    src = _create_c_file(tmp_path, "basic.c", (
        "#include <stdlib.h>\n"
        "#include <string.h>\n"
        "\n"
        "char *dup(const char *s) {\n"
        "    char *buf = malloc(strlen(s) + 1);\n"
        "    strcpy(buf, s);\n"
        "    return buf;\n"
        "}\n"
    ))

    alert = _make_alert(src, 5)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None
    assert context["var_name"] == "buf"
    assert context["return_type"] == "char *"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "if (buf == NULL)" in patched
    assert "return NULL;" in patched


# ---------------------------------------------------------------------------
# Already-safe: existing NULL check — skip
# ---------------------------------------------------------------------------

def test_already_checked_skip(handler, tmp_path):
    """malloc with existing NULL check should be skipped."""
    src = _create_c_file(tmp_path, "safe.c", (
        "#include <stdlib.h>\n"
        "\n"
        "int *alloc(int n) {\n"
        "    int *arr = malloc(n * sizeof(int));\n"
        "    if (arr == NULL) {\n"
        "        return NULL;\n"
        "    }\n"
        "    return arr;\n"
        "}\n"
    ))

    alert = _make_alert(src, 4)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is None, "Already-checked malloc should be skipped"


# ---------------------------------------------------------------------------
# void-returning function: still fix
# ---------------------------------------------------------------------------

def test_void_return(handler, tmp_path):
    """For void-returning function, NULL guard should use 'return;'"""
    src = _create_c_file(tmp_path, "void_ret.c", (
        "#include <stdlib.h>\n"
        "#include <string.h>\n"
        "\n"
        "void process(const char *input) {\n"
        "    char *buf = malloc(1024);\n"
        "    memset(buf, 0, 1024);\n"
        "    (void)input;\n"
        "    free(buf);\n"
        "}\n"
    ))

    alert = _make_alert(src, 5)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None
    assert context["return_type"] == "void"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "if (buf == NULL)" in patched
    assert "return;" in patched
    assert "return NULL" not in patched


# ---------------------------------------------------------------------------
# int-returning function: still fix
# ---------------------------------------------------------------------------

def test_int_return(handler, tmp_path):
    """For int-returning function, NULL guard should use 'return -1;'."""
    src = _create_c_file(tmp_path, "int_ret.c", (
        "#include <stdlib.h>\n"
        "\n"
        "int init_buffer(int size) {\n"
        "    char *buf = malloc(size);\n"
        "    buf[0] = 'A';\n"
        "    free(buf);\n"
        "    return 0;\n"
        "}\n"
    ))

    alert = _make_alert(src, 4)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None
    assert context["return_type"] == "int"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "if (buf == NULL)" in patched
    assert "return -1;" in patched


# ---------------------------------------------------------------------------
# Compile check
# ---------------------------------------------------------------------------

def test_patched_file_compiles(handler, tmp_path):
    """Verify the patched output is valid C that compiles."""
    src = _create_c_file(tmp_path, "compile_test.c", (
        "#include <stdlib.h>\n"
        "#include <string.h>\n"
        "\n"
        "char *dup(const char *s) {\n"
        "    char *buf = malloc(strlen(s) + 1);\n"
        "    strcpy(buf, s);\n"
        "    return buf;\n"
        "}\n"
    ))

    alert = _make_alert(src, 5)
    tu = parse_file(src)
    context = handler.analyze(alert, tu)
    assert context is not None

    rewriter = SourceRewriter(src)
    handler.generate_fix(alert, context, rewriter)

    output = tmp_path / "patched.c"
    rewriter.write(output)

    result = subprocess.run(
        ["gcc", "-c", "-fsyntax-only", str(output)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Compilation failed:\n{result.stderr}"
