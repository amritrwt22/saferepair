"""Scan all sprintf-unbounded repos (using libclang AST) and write alerts.json for each."""

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional
from clang.cindex import CursorKind, Index, TranslationUnit, TypeKind  # type: ignore[attr-defined]  # clang has no type stubs
from config import SPRINTF_UNBOUNDED_REPOS
from script_utils import get_relative_path, setup_logging, write_alerts_json


logger = logging.getLogger(__name__)


# -ferror-limit=0: shows all errors
# -Wno-everything: caps no. of warnings to 0
PARSE_FLAGS = ["-ferror-limit=0", "-Wno-everything"]

# skip kernel-internal directories (sprintf there is intentional/controlled)
KERNEL_SKIP_DIRS = {"drivers", "arch", "kernel", "fs", "net", "mm", "sound", "block", "ipc", "security", "crypto", "init", "lib"}

@dataclass
class Instance:         #confirmed sprintf hit
    file:       str
    line:       int
    buf_name:   str
    array_size: int
    snippet:    str     #raw actual line 


#retunrns text of a line
def read_line(path: str, lineno: int) -> str:
    try:
        with open(path, errors="ignore") as fh:
            for i, line in enumerate(fh, 1):
                if i == lineno:
                    return line
    except Exception:
        pass
    return ""


#creates Index & returns TU of file
def parse_c_file(c_file: Path) -> Optional[TranslationUnit]:
    idx = Index.create()
    try:
        return idx.parse(str(c_file), args=PARSE_FLAGS, options=TranslationUnit.PARSE_INCOMPLETE)
    except Exception:
        return None


#iterative dfs of AST, returns as list to allow later dfs-style visits
def walk_all_cursors(root) -> list:
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node)
        stack.extend(reversed(list(node.get_children())))
    return result


# extracts fn. name from CALL_EXPR node
def get_callee_name(call_node) -> str:
    for child in call_node.get_children():
        #if stuff like someFunc or obj->someFunc
        if child.kind in (CursorKind.DECL_REF_EXPR, CursorKind.MEMBER_REF_EXPR):
            return child.spelling
        #if its a wrapper node
        if child.kind in (CursorKind.UNEXPOSED_EXPR, CursorKind.PAREN_EXPR):
            name = get_callee_name(child)
            if name:
                return name
    return call_node.spelling or ""


#returns first var. declaration node in a subtree 
def find_decl_ref(node) -> Optional[Any]:
    if node.kind == CursorKind.DECL_REF_EXPR:
        return node
    for child in node.get_children():
        result = find_decl_ref(child)
        if result:
            return result
    return None


# returns first string string literal in a subtree
def get_string_literal(node) -> Optional[str]:
    if node.kind == CursorKind.STRING_LITERAL:
        return node.spelling
    for child in node.get_children():
        result = get_string_literal(child)
        if result is not None:
            return result
    return None


def check_sprintf(call_node) -> Optional[Instance]:
    """returns Instance if input CALL_EXPR node is sprintf(fixed_array_buf, fmt_with_%, ...)."""
    
    #not a sprintf() call
    if get_callee_name(call_node) != "sprintf":
        return None

    #sprintf() mustve >=3 args.
    args = list(call_node.get_arguments())
    if len(args) < 3:
        return None

    #1st arg must have DECL_REF_EXPR node (i.e. we skip computed exp. etc.)
    buf_arg = args[0]
    decl_ref = find_decl_ref(buf_arg)
    if decl_ref is None:
        return None

    #see if buf was actually declared somewhere
    decl_cursor = decl_ref.referenced
    if decl_cursor is None:
        return None

    #get buf type & see its a cimpile-time fixed-size array
    decl_type = decl_cursor.type.get_canonical()
    if decl_type.kind != TypeKind.CONSTANTARRAY:
        return None

    #buf element type should be char
    element_type = decl_type.element_type.get_canonical()
    if element_type.kind not in (TypeKind.CHAR_S, TypeKind.CHAR_U, TypeKind.SCHAR, TypeKind.UCHAR):
        return None

    #verifies non-empty buf size
    array_size = decl_type.element_count
    if array_size <= 0:
        return None

    #extracts 2nd arg: string format literal
    fmt_str = get_string_literal(args[1])
    if fmt_str is None or "%s" not in fmt_str:  #no runtime string being written
        return None

    #gets localtion of call 
    loc = call_node.location
    if not loc.file:
        return None
    snippet = read_line(loc.file.name, loc.line).strip()
    return Instance(file=str(loc.file.name), line=loc.line, buf_name=decl_ref.spelling, array_size=array_size, snippet=snippet)


# skip if any part of file path matches with a kernal dir.
def should_skip_file(c_file: Path) -> bool:
    return bool(set(c_file.parts) & KERNEL_SKIP_DIRS)


#see that file contains sprintf & no snprintf
def contains_sprintf(c_file: Path) -> bool:
    try:
        text = c_file.read_text(errors="ignore")
        return "sprintf" in text and "snprintf" not in text
    except Exception:
        return False


def scan_repo(repo_path: Path, verbose: bool = False) -> list[dict]:
    """scans a repo & returns list of alerts as dicts."""

    all_c_files = list(repo_path.rglob("*.c"))
    c_files = [f for f in all_c_files if contains_sprintf(f) and not should_skip_file(f)]
    logger.info(f"Scanning {len(c_files)}/{len(all_c_files)} .c files in {repo_path.name} ...")

    #scan each file
    all_alerts = []
    for c_file in c_files:
        tu = parse_c_file(c_file)
        if tu is None:
            continue
        try:
            file_alerts = []
            # visits all nodes of AST
            for node in walk_all_cursors(tu.cursor):
                if node.kind == CursorKind.CALL_EXPR:
                    inst = check_sprintf(node)
                    if inst and inst.file:
                        file_alerts.append({
                            "rule_id": "CWE-120",
                            "file":    get_relative_path(Path(inst.file), repo_path),
                            "line":    inst.line,
                            "column":  0,
                            "message": "sprintf to fixed-size buffer without bounds (CWE-120)",
                        })
            if file_alerts:
                logger.info(f"  {c_file.relative_to(repo_path)}: {len(file_alerts)} hit(s)")
            all_alerts.extend(file_alerts)
        except Exception:
            pass

    return all_alerts


def main():
    p = argparse.ArgumentParser(description="Scan all sprintf-unbounded repos")
    p.add_argument("--verbose", "-v", action="store_true")     #syntax for adding flag
    args = p.parse_args()

    setup_logging(args.verbose)
    
    #scans all repos & writes their alerts.json
    for cfg in SPRINTF_UNBOUNDED_REPOS:
        repo_dir: Path = cfg["repo_dir"]
        if not repo_dir.is_dir():
            logger.warning(f"[SKIP] repo not found: {repo_dir}")
            continue
        alerts = scan_repo(repo_dir, verbose=args.verbose)
        logger.info(f"\nTotal: {len(alerts)} CWE-120 instance(s) in {cfg['display']}")
        write_alerts_json(alerts, cfg["alerts_json"])


if __name__ == "__main__":                   #main() only runs when executed directly, not when imported
    main()
