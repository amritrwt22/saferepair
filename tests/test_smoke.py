"""verify that libclang can parse C code from Python"""

import tempfile
from pathlib import Path
from clang.cindex import Index, CursorKind


def test_libclang_can_parse_c():
    """Parse a simplee C file & verify the AST root is a TU"""
    index = Index.create()

    #create temp. C file to parse
    with tempfile.NamedTemporaryFile(suffix='.c', mode='w', delete=False) as f:    # keeps file alivr after `with`, to let clang read it
        f.write('int main() { return 0; }') #code of temp. file
        tmp_path = f.name

    try:
        tu = index.parse(tmp_path, args=['-x', 'c', '-std=c11'])
        assert tu is not None, "Translation unit is None — libclang failed to parse"

        root = tu.cursor
        assert root.kind == CursorKind.TRANSLATION_UNIT, (
            f"Expected TRANSLATION_UNIT, got {root.kind}"
        )

        children = list(root.get_children())
        assert len(children) > 0, "AST has no children — parsing may have failed"

        #verifies the main() fn. is present
        func = children[0]
        assert func.kind == CursorKind.FUNCTION_DECL, (
            f"Expected FUNCTION_DECL, got {func.kind}"
        )
        assert func.spelling == 'main', (
            f"Expected function named 'main', got '{func.spelling}'"
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def test_libclang_can_find_function_calls():
    """Parse C code having a fn. call & verify if it can be found in AST"""
    index = Index.create()

    code = '''
        #include <stdlib.h>

        void foo() {
            int *p = malloc(10 * sizeof(int));
            free(p);
        }
        '''
    with tempfile.NamedTemporaryFile(suffix='.c', mode='w', delete=False) as f:
        f.write(code)
        tmp_path = f.name

    try:
        tu = index.parse(tmp_path, args=['-x', 'c', '-std=c11'])
        assert tu is not None, "Translation unit is None — libclang failed to parse"

        # Walk th AST to see if malloc() CALL_EXPR found
        call_exprs = []

        def walk(cursor):
            if cursor.kind == CursorKind.CALL_EXPR:
                call_exprs.append(cursor.spelling)
            for child in cursor.get_children():
                walk(child)

        walk(tu.cursor)

        assert 'malloc' in call_exprs, (
            f"Expected 'malloc' in call expressions, found: {call_exprs}"
        )
    finally:
        Path(tmp_path).unlink(missing_ok=True)
