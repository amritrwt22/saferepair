"""Tests for the suspicious-realloc handler."""

import subprocess
from pathlib import Path

import pytest

from saferepair.models import Alert, RepairPattern, RepairStatus
from saferepair.ast_analyzer import parse_file
from saferepair.source_rewriter import SourceRewriter
from saferepair.handlers.suspicious_realloc import SuspiciousReallocHandler


@pytest.fixture
def handler():
    return SuspiciousReallocHandler()


def _create_c_file(tmp_path, name, content):
    """Write a C file and return its path."""
    f = tmp_path / name
    f.write_text(content)
    return f


def _make_alert(file_path, line):
    """Create a realloc alert for a given file and line."""
    return Alert(
        rule_id="bugprone-suspicious-realloc-usage",
        file_path=file_path,
        line=line,
        column=5,
        message="suspicious realloc",
        pattern=RepairPattern.SUSPICIOUS_REALLOC,
    )


# ---------------------------------------------------------------------------
# can_handle
# ---------------------------------------------------------------------------

def test_can_handle(handler):
    """Handler should only accept SUSPICIOUS_REALLOC pattern."""
    alert_yes = Alert("rule", Path("f.c"), 1, 0, "msg",
                       pattern=RepairPattern.SUSPICIOUS_REALLOC)
    alert_no = Alert("rule", Path("f.c"), 1, 0, "msg",
                      pattern=RepairPattern.MISSING_NULL_CHECK_MALLOC)
    assert handler.can_handle(alert_yes) is True
    assert handler.can_handle(alert_no) is False


# ---------------------------------------------------------------------------
# Basic fix: p = realloc(p, n)
# ---------------------------------------------------------------------------

def test_basic_realloc_fix(handler, tmp_path):
    """p = realloc(p, 20) should be wrapped with temp pointer."""
    src = _create_c_file(tmp_path, "basic.c", (
        "#include <stdlib.h>\n"
        "\n"
        "int main() {\n"
        "    char *p = malloc(10);\n"
        "    p = realloc(p, 20);\n"
        "    free(p);\n"
        "    return 0;\n"
        "}\n"
    ))

    alert = _make_alert(src, 5)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None
    assert context["var_name"] == "p"
    assert context["size_expr"] == "20"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "_sr_tmp" in patched
    assert "if (_sr_tmp != NULL)" in patched
    assert "realloc(p, 20)" in patched
    # Original direct self-assignment should be gone; the realloc call
    # now lives inside "void *_sr_tmp = realloc(...)" instead
    for line in patched.splitlines():
        assert line.strip() != "p = realloc(p, 20);", \
            "Original self-assignment line should have been replaced"


# ---------------------------------------------------------------------------
# Cast form: buf = (char*)realloc(buf, n)
# ---------------------------------------------------------------------------

def test_realloc_with_cast(handler, tmp_path):
    """buf = (char*)realloc(buf, 200) should handle the cast."""
    src = _create_c_file(tmp_path, "cast.c", (
        "#include <stdlib.h>\n"
        "\n"
        "int main() {\n"
        "    char *buf = (char*)malloc(100);\n"
        "    buf = (char*)realloc(buf, 200);\n"
        "    free(buf);\n"
        "    return 0;\n"
        "}\n"
    ))

    alert = _make_alert(src, 5)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None
    assert context["var_name"] == "buf"
    assert context["cast_expr"] is not None
    assert "char" in context["cast_expr"]

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "_sr_tmp" in patched
    assert "buf = (char*)" in patched or "buf = (char *)" in patched


# ---------------------------------------------------------------------------
# Already-safe: temp pointer already used — skip
# ---------------------------------------------------------------------------

def test_already_safe_skip(handler, tmp_path):
    """Code that already uses a temp pointer should not match the regex."""
    src = _create_c_file(tmp_path, "safe.c", (
        "#include <stdlib.h>\n"
        "\n"
        "int main() {\n"
        "    char *p = malloc(10);\n"
        "    char *tmp = realloc(p, 20);\n"
        "    if (tmp != NULL) {\n"
        "        p = tmp;\n"
        "    }\n"
        "    free(p);\n"
        "    return 0;\n"
        "}\n"
    ))

    # Alert points at line 5: tmp = realloc(p, 20)
    # This is NOT self-assignment (tmp != p), so analysis should return None
    alert = _make_alert(src, 5)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is None, "Already-safe realloc should not be matched"


# ---------------------------------------------------------------------------
# Struct arrow member: ptr->field = realloc(ptr->field, n)
# ---------------------------------------------------------------------------

def test_struct_member_realloc_fix(handler, tmp_path):
    """ptr->field = realloc(ptr->field, n) should be wrapped with temp pointer."""
    src = _create_c_file(tmp_path, "struct_member.c", (
        "#include <stdlib.h>\n"
        "\n"
        "typedef struct { char *data; } Node;\n"
        "\n"
        "void grow(Node *n, int sz) {\n"
        "    n->data = realloc(n->data, sz);\n"
        "}\n"
    ))

    alert = _make_alert(src, 6)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None
    assert context["var_name"] == "n->data"
    assert context["size_expr"] == "sz"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "_sr_tmp" in patched
    assert "realloc(n->data, sz)" in patched
    assert "n->data = " in patched


# ---------------------------------------------------------------------------
# Struct dot member: obj.field = realloc(obj.field, n)
# ---------------------------------------------------------------------------

def test_struct_member_dot_form(handler, tmp_path):
    """obj.field = realloc(obj.field, n) dot-access form should also be fixed."""
    src = _create_c_file(tmp_path, "dot_member.c", (
        "#include <stdlib.h>\n"
        "\n"
        "typedef struct { char *buf; } Buf;\n"
        "\n"
        "void grow(Buf b, int sz) {\n"
        "    b.buf = realloc(b.buf, sz);\n"
        "}\n"
    ))

    alert = _make_alert(src, 6)
    tu = parse_file(src)
    assert tu is not None

    context = handler.analyze(alert, tu)
    assert context is not None
    assert context["var_name"] == "b.buf"

    rewriter = SourceRewriter(src)
    result = handler.generate_fix(alert, context, rewriter)
    assert result.status == RepairStatus.SUCCESS

    patched = rewriter.apply()
    assert "_sr_tmp" in patched
    assert "realloc(b.buf, sz)" in patched


# ---------------------------------------------------------------------------
# Compile check
# ---------------------------------------------------------------------------

def test_patched_file_compiles(handler, tmp_path):
    """Verify the patched output is valid C that compiles."""
    src = _create_c_file(tmp_path, "compile_test.c", (
        "#include <stdlib.h>\n"
        "\n"
        "int main() {\n"
        "    char *p = malloc(10);\n"
        "    p = realloc(p, 20);\n"
        "    free(p);\n"
        "    return 0;\n"
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
