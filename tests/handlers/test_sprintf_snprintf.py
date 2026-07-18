"""tests for sprintf_snprintf handler (CWE-120)"""

import subprocess
from pathlib import Path
import pytest

from saferepair.models import Alert, RepairPattern, RepairStatus
from saferepair.ast_analyzer import parse_file
from saferepair.source_rewriter import SourceRewriter
from saferepair.handlers.sprintf_snprintf import SprintfSnprintfHandler


@pytest.fixture
def handler():
    return SprintfSnprintfHandler()


def _c(tmp_path, name, content):
    f = tmp_path / name
    f.write_text(content, encoding="utf-8")
    return f


def _alert(file_path, line):
    return Alert(
        rule_id="CWE-120",
        file_path=file_path,
        line=line,
        column=5,
        message="sprintf to fixed-size buffer without bounds check",
        pattern=RepairPattern.SPRINTF_UNBOUNDED,
    )


# ---------------------------------------------------------------------------
# can_handle
# ---------------------------------------------------------------------------

def test_can_handle(handler):
    """handler accepts SPRINTF_UNBOUNDED, rejects other patterns"""
    yes = Alert("CWE-120", Path("f.c"), 1, 0, "msg",
                pattern=RepairPattern.SPRINTF_UNBOUNDED)
    no = Alert("rule", Path("f.c"), 1, 0, "msg",
               pattern=RepairPattern.SUSPICIOUS_REALLOC)
    assert handler.can_handle(yes) is True
    assert handler.can_handle(no) is False


# ---------------------------------------------------------------------------
# %s runtime string: must fix
# ---------------------------------------------------------------------------

def test_basic_string_fix(handler, tmp_path):
    """%s format with runtime arg: classic CWE-120 — must be fixed."""
    src = _c(tmp_path, "basic.c", (
        "#include <stdio.h>\n"
        "void f(const char *name, int n) {\n"
        "    char buf[64];\n"
        "    sprintf(buf, \"%s_%d\", name, n);\n"
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    assert tu is not None

    ctx = handler.analyze(alert, tu)
    assert ctx is not None
    assert ctx["buf_name"] == "buf"

    rw = SourceRewriter(src)
    result = handler.generate_fix(alert, ctx, rw)
    assert result.status == RepairStatus.SUCCESS

    patched = rw.apply()
    assert "snprintf(buf, sizeof(buf)," in patched
    assert "sprintf(buf," not in patched


# ---------------------------------------------------------------------------
# Numeric-only specifier: conservative fix
# ---------------------------------------------------------------------------

def test_numeric_specifier_fixed(handler, tmp_path):
    """%d only: not exploitable but sprintf is deprecated — fix conservatively"""
    src = _c(tmp_path, "num.c", (
        "#include <stdio.h>\n"
        "void f(int i) {\n"
        "    char buf[32];\n"
        "    sprintf(buf, \"t%d\", i);\n"
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is not None
    assert ctx["buf_name"] == "buf"

    rw = SourceRewriter(src)
    result = handler.generate_fix(alert, ctx, rw)
    assert result.status == RepairStatus.SUCCESS
    patched = rw.apply()
    assert "snprintf(buf, sizeof(buf)," in patched
    assert "sprintf(buf," not in patched


# ---------------------------------------------------------------------------
# Cast on buffer argument: still fix
# ---------------------------------------------------------------------------

def test_cast_on_buffer(handler, tmp_path):
    """sprintf((char *)buf, ...) -> snprintf((char *)buf, sizeof(buf), ...)"""
    src = _c(tmp_path, "cast.c", (
        "#include <stdio.h>\n"
        "void f(int i) {\n"
        "    char buf[30];\n"
        "    sprintf((char *)buf, \"pos%d\", i);\n"
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is not None
    assert ctx["buf_name"] == "buf"

    rw = SourceRewriter(src)
    result = handler.generate_fix(alert, ctx, rw)
    assert result.status == RepairStatus.SUCCESS
    patched = rw.apply()
    assert "snprintf((char *)buf, sizeof(buf)," in patched
    assert "sprintf((char *)buf," not in patched


# ---------------------------------------------------------------------------
# LHS assignment form: len = sprintf(buf, ...): also fix
# ---------------------------------------------------------------------------

def test_lhs_assignment_form(handler, tmp_path):
    """len = sprintf(buf, ...) should also be fixed."""
    src = _c(tmp_path, "lhs.c", (
        "#include <stdio.h>\n"
        "void f(const char *s) {\n"
        "    char packet[1024];\n"
        "    int len = sprintf(packet, \"prefix.%s\", s);\n"
        "    (void)len;\n"
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is not None
    assert ctx["buf_name"] == "packet"

    rw = SourceRewriter(src)
    result = handler.generate_fix(alert, ctx, rw)
    assert result.status == RepairStatus.SUCCESS
    patched = rw.apply()
    assert "int len = snprintf(packet, sizeof(packet)," in patched
    assert "sprintf(packet," not in patched


# ---------------------------------------------------------------------------
# Multiple sprintf calls in one file: only fix the alerted line
# ---------------------------------------------------------------------------

def test_only_alerted_line_fixed(handler, tmp_path):
    """Only the line in the alert should be modified, not other sprintf calls."""
    src = _c(tmp_path, "multi.c", (
        "#include <stdio.h>\n"
        "void f(const char *s) {\n"
        "    char a[64], b[64];\n"
        "    sprintf(a, \"%s\", s);\n"    # line 4 — alerted
        "    sprintf(b, \"%s\", s);\n"    # line 5 — NOT alerted
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is not None

    rw = SourceRewriter(src)
    handler.generate_fix(alert, ctx, rw)
    patched = rw.apply()

    lines = patched.splitlines()
    assert "snprintf" in lines[3]      # line 4 fixed
    assert lines[4].strip().startswith("sprintf")  # line 5 untouched


# ---------------------------------------------------------------------------
# Already-safe snprintf: skip
# ---------------------------------------------------------------------------

def test_already_snprintf_skipped(handler, tmp_path):
    """snprintf lines must be skipped — already safe."""
    src = _c(tmp_path, "safe.c", (
        "#include <stdio.h>\n"
        "void f(const char *name, int n) {\n"
        "    char buf[64];\n"
        "    snprintf(buf, sizeof(buf), \"%s_%d\", name, n);\n"
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is None, "Already-safe snprintf should be skipped"


# ---------------------------------------------------------------------------
# Real-world pattern: libpng titlebar
# ---------------------------------------------------------------------------

def test_libpng_titlebar_pattern(handler, tmp_path):
    """Mirrors libpng rpng-x.c: sprintf(titlebar, \"%s:  %s\", appname, filename)"""
    src = _c(tmp_path, "libpng_style.c", (
        "#include <stdio.h>\n"
        "void set_title(const char *appname, const char *filename) {\n"
        "    char titlebar[1024];\n"
        "    sprintf(titlebar, \"%s:  %s\", appname, filename);\n"
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is not None
    assert ctx["buf_name"] == "titlebar"

    rw = SourceRewriter(src)
    result = handler.generate_fix(alert, ctx, rw)
    assert result.status == RepairStatus.SUCCESS
    patched = rw.apply()
    assert "snprintf(titlebar, sizeof(titlebar)," in patched
    assert "sprintf(titlebar," not in patched


# ---------------------------------------------------------------------------
# Real-world pattern: TDengine SQL buffer
# ---------------------------------------------------------------------------

def test_tdengine_sql_pattern(handler, tmp_path):
    """Mirrors TDengine asyncdemo.c: sprintf(sql, \"drop database if exists %s\", db)."""
    src = _c(tmp_path, "tdengine_style.c", (
        "#include <stdio.h>\n"
        "void drop_db(const char *db) {\n"
        "    char sql[1024];\n"
        "    sprintf(sql, \"drop database if exists %s\", db);\n"
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is not None
    assert ctx["buf_name"] == "sql"

    rw = SourceRewriter(src)
    result = handler.generate_fix(alert, ctx, rw)
    assert result.status == RepairStatus.SUCCESS
    patched = rw.apply()
    assert "snprintf(sql, sizeof(sql)," in patched
    assert "sprintf(sql," not in patched


# ---------------------------------------------------------------------------
# Real-world pattern: vim sha256 hex output
# ---------------------------------------------------------------------------

def test_vim_hex_pattern_skipped(handler, tmp_path):
    """Mirrors vim sha256.c: sprintf(hexit + j*2, ...) — pointer arithmetic as
    first arg means libclang sees no CONSTANTARRAY, so analyze returns None (skipped)."""
    src = _c(tmp_path, "vim_style.c", (
        "#include <stdio.h>\n"
        "void hex_encode(unsigned char *sha256sum) {\n"
        "    char hexit[65];\n"
        "    for (int j = 0; j < 32; j++)\n"
        "        sprintf(hexit + j * 2, \"%02x\", sha256sum[j]);\n"
        "}\n"
    ))
    alert = _alert(src, 5)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is None, "pointer-arithmetic buffer arg should not be handled"


# ---------------------------------------------------------------------------
# Compile check
# ---------------------------------------------------------------------------

def test_patched_file_compiles(handler, tmp_path):
    """After fix, the patched C file must compile clean with gcc."""
    src = _c(tmp_path, "compile_check.c", (
        "#include <stdio.h>\n"
        "void log_user(const char *username, int uid) {\n"
        "    char msg[256];\n"
        "    sprintf(msg, \"user=%s uid=%d\", username, uid);\n"
        "}\n"
    ))
    alert = _alert(src, 4)
    tu = parse_file(src)
    ctx = handler.analyze(alert, tu)
    assert ctx is not None

    rw = SourceRewriter(src)
    handler.generate_fix(alert, ctx, rw)

    out = tmp_path / "patched.c"
    rw.write(out)

    result = subprocess.run(
        ["gcc", "-c", "-fsyntax-only", str(out)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Compilation failed:\n{result.stderr}"
