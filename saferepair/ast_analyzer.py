"""libclang AST traversal utilities for analyzing C/C++ source files"""

import logging
from pathlib import Path
from typing import Optional, Callable

from clang.cindex import (
    Index,
    TranslationUnit,
    Cursor,
    CursorKind
)

logger = logging.getLogger(__name__)


#shared clang index for all parses
_index: Optional[Index] = None

def _get_index() -> Index:
    """get/create a shared Index"""
    global _index
    if _index is None:
        _index = Index.create()
    return _index


def parse_file(
    file_path: Path,
    compile_args: Optional[list[str]] = None,
) -> Optional[TranslationUnit]:
    """parse C/C++ file & returns its TU"""

    #settin flags fozr C vs C++
    # -nostdinc: skip search of system headers (windows.h, X11/Xlib.h, etc.)
    #            cuz we only need AST structure not fuly resolved types. 
    # -ferror-limit=5: caps the no. of errors the compiler reports to 5
    #                  to avoid err. shower due to missing headers
    # -Wno-everything: caps no. of warnings to 0
    args = compile_args or []
    if '-x' not in args: #nothing set alreadty
        if file_path.suffix in ('.c', '.h'):
            args = ['-x', 'c', '-std=c11',
                    '-nostdinc', '-ferror-limit=5', '-Wno-everything'] + args
        else:
            args = ['-x', 'c++', '-std=c++17',
                    '-nostdinc', '-ferror-limit=5', '-Wno-everything'] + args

    #parsing & returning TU
    index = _get_index()
    try:
        tu = index.parse(
            str(file_path),
            args=args,
            options=TranslationUnit.PARSE_INCOMPLETE,   #return AST even if headers missing
        )
        if tu is None:
            logger.error(f"Failed to parse {file_path}")
            return None

        #log warnings/errors from parsing
        for diag in tu.diagnostics:
            if diag.severity >= 3:  #Error/Fatal
                logger.debug(f"Parse diagnostic: {diag}")

        return tu
    except Exception as e:
        logger.error(f"Exception parsing {file_path}: {e}")
        return None


def walk_ast(cursor: Cursor, visitor: Callable[[Cursor], Optional[bool]]) -> None:
    """walk AST depth-first, calling visitor fn. on each node
       if visitor returns True, stop descending into children of that node

       fn. used by other fns. for traversal
    """
    stop = visitor(cursor)
    if stop:
        return
    for child in cursor.get_children():
        walk_ast(child, visitor)


def find_nodes_at_line(
    tu: TranslationUnit,
    file_path: Path,
    line: int,
) -> list[Cursor]:
    """returns list of AST nodes whose loc. is on givn line,
       by visiitng whole tree & matching lines & nodes.
    """

    file_str = str(file_path.resolve())
    matches = []

    def visitor(cursor: Cursor) -> Optional[bool]:
        loc = cursor.location
        if loc.file and str(Path(loc.file.name).resolve()) == file_str:
            if loc.line == line:
                matches.append(cursor)
        return None

    walk_ast(tu.cursor, visitor)   #tu.cursor = root node
    return matches


def find_call_expr_at_line(
    tu: TranslationUnit,
    file_path: Path,
    line: int,
    function_name: Optional[str] = None,
) -> Optional[Cursor]:
    """finds a CALL_EXPR node at given line,
       by vising all nodes & checking their line no. & node type.
    """
    
    file_str = str(file_path.resolve())
    result = None

    def visitor(cursor: Cursor) -> Optional[bool]:
        nonlocal result
        loc = cursor.location
        if loc.file and str(Path(loc.file.name).resolve()) == file_str:
            if loc.line == line and cursor.kind == CursorKind.CALL_EXPR:
                if function_name is None or cursor.spelling == function_name:
                    result = cursor
                    return True  #stop searching
        return None

    walk_ast(tu.cursor, visitor)
    return result


def get_line_text(file_path: Path, line: int) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for i, text in enumerate(f, 1):
                if i == line:
                    return text
    except (FileNotFoundError, IOError):
        pass
    return ""


def get_line_indentation(file_path: Path, line: int) -> str:
    """returns leading whitespace of a line"""
    text = get_line_text(file_path, line)
    return text[:len(text) - len(text.lstrip())]


def find_enclosing_function(
    tu: TranslationUnit,
    file_path: Path,
    line: int,
) -> Optional[tuple[str, str]]:
    """Finds fn. def. that encloses given line,
       walks AST looking for FUNCTION_DECL nodes whose source extent covers the line

    returns:
        tuple (function_name, return_type_spelling) if found, else None.
        return_type_spelling eg. "void", "int", "char *"
    """

    file_str = str(file_path.resolve())
    result = None

    def visitor(cursor: Cursor) -> Optional[bool]:
        nonlocal result
        if cursor.kind == CursorKind.FUNCTION_DECL:
            loc = cursor.location
            if loc.file and str(Path(loc.file.name).resolve()) == file_str:
                extent = cursor.extent
                if extent.start.line <= line <= extent.end.line:
                    result = (cursor.spelling, cursor.result_type.spelling)
        return None  # keep walking regardless to find tightest enclosing fn. as u go deeper

    walk_ast(tu.cursor, visitor)
    return result


def get_cursor_spelling_chain(cursor: Cursor) -> list[str]:
    """return curr. & child cursors' spellings (i.e. name of var/fn/keyword/etc.)"""
    result = []

    def visitor(c: Cursor) -> Optional[bool]:
        if c.spelling:
            result.append(f"{c.kind.name}: {c.spelling}")
        return None

    walk_ast(cursor, visitor)
    return result
