"""tests for ast_analyzer.py"""

from pathlib import Path
from clang.cindex import CursorKind

from saferepair.ast_analyzer import (
    parse_file,
    walk_ast,
    find_nodes_at_line,
    find_call_expr_at_line,
    get_line_text,
    get_line_indentation,
    find_enclosing_function,
    get_cursor_spelling_chain,
)


def _write_c(tmp_path, name, content):
    f = tmp_path / name
    f.write_text(content)
    return f


# ---------------------------------------------------------------------------
# parse_file
# ---------------------------------------------------------------------------

def test_parse_valid_c_file(tmp_path):
    src = _write_c(tmp_path, "ok.c", "int main(void) { return 0; }\n")
    tu = parse_file(src)
    assert tu is not None


def test_parse_nonexistent_file(tmp_path):
    result = parse_file(tmp_path / "missing.c")
    assert result is None


def test_parse_returns_tu_even_with_errors(tmp_path):
    """parse_file uses PARSE_INCOMPLETE so it tolerates missing headers"""
    src = _write_c(tmp_path, "incomplete.c", "#include <nonexistent.h>\nint x = 1;\n")
    tu = parse_file(src)
    assert tu is not None


# ---------------------------------------------------------------------------
# walk_ast
# ---------------------------------------------------------------------------

def test_walk_ast_visits_all_nodes(tmp_path):
    """walk_ast should visit every node including nested ones"""
    src = _write_c(tmp_path, "walk.c",
        "#include <stdlib.h>\n"
        "void f(void) { void *p = malloc(10); free(p); }\n"
    )
    tu = parse_file(src)
    visited = []
    walk_ast(tu.cursor, lambda c: visited.append(c.kind) or None)
    assert len(visited) > 5  # at minimum: TU, function decl, body, calls, etc.
    assert CursorKind.TRANSLATION_UNIT in visited
    assert CursorKind.FUNCTION_DECL in visited


def test_walk_ast_stop_on_true(tmp_path):
    """returning True from visitor stops descent into that node's children"""
    src = _write_c(tmp_path, "stop.c", "int f(void) { return 1; }\nint g(void) { return 2; }\n")
    tu = parse_file(src)
    visited_spellings = []

    def visitor(cursor):
        visited_spellings.append(cursor.spelling)
        if cursor.spelling == "f":
            return True  # stop descending into f's body
        return None

    walk_ast(tu.cursor, visitor)
    # g should still be visited (sibling, not child of f)
    assert "g" in visited_spellings
    # without stop: 9 nodes total; with stop: 6 (f's 3 children skipped)
    assert len(visited_spellings) == 6


# ---------------------------------------------------------------------------
# find_nodes_at_line
# ---------------------------------------------------------------------------

def test_find_nodes_at_line_returns_something(tmp_path):
    src = _write_c(tmp_path, "nodes.c", "int main(void) { return 0; }\n")
    tu = parse_file(src)
    nodes = find_nodes_at_line(tu, src, 1)
    assert len(nodes) > 0


def test_find_nodes_at_nonexistent_line_returns_empty(tmp_path):
    src = _write_c(tmp_path, "short.c", "int x = 1;\n")
    tu = parse_file(src)
    nodes = find_nodes_at_line(tu, src, 999)
    assert nodes == []


# ---------------------------------------------------------------------------
# find_call_expr_at_line
# ---------------------------------------------------------------------------

def test_find_call_expr_finds_malloc(tmp_path):
    src = _write_c(tmp_path, "malloc.c",
        "#include <stdlib.h>\n"
        "void f(void) { void *p = malloc(10); }\n"
    )
    tu = parse_file(src)
    node = find_call_expr_at_line(tu, src, 2, "malloc")
    assert node is not None
    assert node.spelling == "malloc"


def test_find_call_expr_wrong_name_returns_none(tmp_path):
    src = _write_c(tmp_path, "malloc2.c",
        "#include <stdlib.h>\n"
        "void f(void) { void *p = malloc(10); }\n"
    )
    tu = parse_file(src)
    node = find_call_expr_at_line(tu, src, 2, "realloc")
    assert node is None


def test_find_call_expr_any_name(tmp_path):
    src = _write_c(tmp_path, "call.c",
        "#include <stdlib.h>\n"
        "void f(void) { void *p = malloc(10); }\n"
    )
    tu = parse_file(src)
    node = find_call_expr_at_line(tu, src, 2)  # no name filter
    assert node is not None


# ---------------------------------------------------------------------------
# get_line_text / get_line_indentation
# ---------------------------------------------------------------------------

def test_get_line_text_returns_correct_line(tmp_path):
    src = _write_c(tmp_path, "lines.c", "int x = 1;\nint y = 2;\n")
    assert get_line_text(src, 1).strip() == "int x = 1;"
    assert get_line_text(src, 2).strip() == "int y = 2;"


def test_get_line_text_out_of_range_returns_empty(tmp_path):
    src = _write_c(tmp_path, "short.c", "int x = 1;\n")
    assert get_line_text(src, 999) == ""


def test_get_line_text_missing_file():
    assert get_line_text(Path("nonexistent.c"), 1) == ""


def test_get_line_indentation(tmp_path):
    src = _write_c(tmp_path, "indent.c", "void f(void) {\n    int x = 1;\n}\n")
    assert get_line_indentation(src, 2) == "    "
    assert get_line_indentation(src, 1) == ""


# ---------------------------------------------------------------------------
# find_enclosing_function
# ---------------------------------------------------------------------------

def test_find_enclosing_function_basic(tmp_path):
    src = _write_c(tmp_path, "func.c",
        "#include <stdlib.h>\n"
        "int compute(int n) {\n"
        "    return n * 2;\n"
        "}\n"
    )
    tu = parse_file(src)
    result = find_enclosing_function(tu, src, 3)
    assert result is not None
    name, ret = result
    assert name == "compute"
    assert "int" in ret


def test_find_enclosing_function_void_return(tmp_path):
    src = _write_c(tmp_path, "void_func.c",
        "void do_nothing(void) {\n"
        "    int x = 1;\n"
        "}\n"
    )
    tu = parse_file(src)
    result = find_enclosing_function(tu, src, 2)
    assert result is not None
    name, ret = result
    assert name == "do_nothing"
    assert ret == "void"


def test_find_enclosing_function_outside_any_function(tmp_path):
    src = _write_c(tmp_path, "global.c", "int global_var = 42;\n")
    tu = parse_file(src)
    result = find_enclosing_function(tu, src, 1)
    assert result is None


# ---------------------------------------------------------------------------
# get_cursor_spelling_chain
# ---------------------------------------------------------------------------

def test_get_cursor_spelling_chain_returns_list(tmp_path):
    src = _write_c(tmp_path, "chain.c",
        "#include <stdlib.h>\n"
        "void f(void) { void *p = malloc(10); }\n"
    )
    tu = parse_file(src)
    chain = get_cursor_spelling_chain(tu.cursor)
    assert isinstance(chain, list)
    assert len(chain) > 0


def test_get_cursor_spelling_chain_contains_function_name(tmp_path):
    src = _write_c(tmp_path, "chain2.c",
        "int add(int a, int b) { return a + b; }\n"
    )
    tu = parse_file(src)
    chain = get_cursor_spelling_chain(tu.cursor)
    spellings = " ".join(chain)
    assert "add" in spellings


def test_get_cursor_spelling_chain_format(tmp_path):
    """Each entry should be 'KIND: spelling' format."""
    src = _write_c(tmp_path, "chain3.c", "int x = 1;\n")
    tu = parse_file(src)
    chain = get_cursor_spelling_chain(tu.cursor)
    for entry in chain:
        assert ":" in entry, f"Expected 'KIND: spelling' format, got: {entry!r}"
