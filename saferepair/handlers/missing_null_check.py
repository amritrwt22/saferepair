"""Handler for missing NULL check after malloc (CWE-690)

Detects: ptr = malloc(size);  i.e. no NULL check before use
Fixes: insert if (ptr == NULL) { return <error>; } after malloc line

thee return err. val. depends on enclosing fn's return type:
    int/long/etc.  -> return -1;
    pointer        -> return NULL;
    void           -> return;
"""

import logging
import re
from typing import Optional
from clang.cindex import TranslationUnit

from ..models import Alert, RepairResult, RepairStatus, RepairPattern, SourceEdit
from ..source_rewriter import SourceRewriter
from ..ast_analyzer import (
    find_call_expr_at_line,
    find_enclosing_function,
    get_line_text
)
from .base import RepairHandler


logger = logging.getLogger(__name__)


# detects [type *]<var> = [cast] malloc( <size> ); statements
MALLOC_ASSIGN_RE = re.compile(
    r'^(\s*)'                            # group 1: indentation (spaces/tabs before)
    r'(?:[\w\s\*]+\s+\*?\s*)?'           # optional type prefix 
    r'(\w+)'                             # group 2: LHS var's name
    r'\s*=\s*'                           # assignment opr. + optional spaces
    r'(?:\(\s*\w[\w\s\*]*\)\s*)?'        # optionl cast e.g. (char*)
    r'malloc\s*\('                       # malloc(
    r'.+?'                               # size argument(s)
    r'\)\s*;'                            # ); (for single line mallocs)
)

# patterns indicating NULL check prolly already exists
NULL_CHECK_PATTERNS = [
    re.compile(r'\bif\s*\(\s*\w+\s*==\s*NULL\b'),    # if (ptr == NULL)
    re.compile(r'\bif\s*\(\s*NULL\s*==\s*\w+\b'),    # if (NULL == ptr)
    re.compile(r'\bif\s*\(\s*!\s*\w+\s*\)'),         # if (!ptr)
    re.compile(r'\bif\s*\(\s*\w+\s*!=\s*NULL\b'),    # if (ptr != NULL)
    re.compile(r'\bif\s*\(\s*NULL\s*!=\s*\w+\b'),    # if (NULL != ptr)
    re.compile(r'\bif\s*\(\s*\w+\s*\)'),             # if (ptr)
]

def _has_null_check(file_path, line_num, var_name, lookahead=3):
    """checks if there's already NULL check for var_name within lookahead lines"""
    for offset in range(1, lookahead + 1):
        next_line = get_line_text(file_path, line_num + offset)
        if not next_line:
            break
        for pattern in NULL_CHECK_PATTERNS:
            match = pattern.search(next_line)
            if match and var_name in next_line:
                return True
    return False


def _return_value_for_type(return_type: str) -> str:
    """returns the error return val. based on fn's return type"""
    rt = return_type.strip()
    if rt == "void":
        return "return;"
    if '*' in rt:
        return "return NULL;"
    return "return -1;" # for int/long/size_t, etc.


class MissingNullCheckHandler(RepairHandler):
    def can_handle(self, alert: Alert) -> bool:
        return alert.pattern == RepairPattern.MISSING_NULL_CHECK_MALLOC

    def analyze(self, alert: Alert, tu: TranslationUnit) -> Optional[dict]:
        #step1: read source line
        file_path = alert.file_path
        line_num = alert.line
        line_text = get_line_text(file_path, line_num)
        if not line_text:
            logger.debug(f"Could not read line {line_num} from {file_path}")
            return None

        #step2: regex match to get var. name
        match = MALLOC_ASSIGN_RE.match(line_text)
        if not match:
            logger.debug(f"Line does not match malloc assign pattern: {line_text.strip()}")
            return None
        indent = match.group(1)
        var_name = match.group(2)

        #steps3: AST verify that a malloc call exists at this line (not just sum comment, etc)
        call_cursor = find_call_expr_at_line(tu, file_path, line_num, "malloc")
        if call_cursor is None:
            logger.debug(f"AST: no malloc call found at line {line_num}")
            return None

        #step4: check if NULL check already exist
        if _has_null_check(file_path, line_num, var_name):
            logger.debug(f"NULL check already exists for '{var_name}' after line {line_num}")
            return None

        #step5:find enclosing function to find return type
        func_info = find_enclosing_function(tu, file_path, line_num)
        if func_info is None:
            logger.debug(f"Could not find enclosing function for line {line_num}")
            return None
        func_name, return_type = func_info

        return {
            "var_name": var_name,
            "indent": indent,
            "line_num": line_num,
            "original_line": line_text,
            "func_name": func_name,
            "return_type": return_type,
        }

    def generate_fix(
        self,
        alert: Alert,
        context: dict,
        rewriter: SourceRewriter,
    ) -> RepairResult:

        #stpe1: build the NULL check block
        var_name = context["var_name"]
        indent = context["indent"]
        line_num = context["line_num"]
        return_type = context["return_type"]
        return_stmt = _return_value_for_type(return_type)

        null_check = (
            f"{indent}if ({var_name} == NULL) {{\n"
            f"{indent}    {return_stmt}\n"
            f"{indent}}}\n"
        )

        # produces:
        #   if (ptr == NULL) {
        #       return NULL;
        #   }
        rewriter.insert_after_line(line_num, null_check)

        edit = SourceEdit(
            file_path=alert.file_path,
            line=line_num,
            old_text="",
            new_text=null_check.rstrip(),
            description=(
                f"Insert NULL check for '{var_name}' after malloc "
                f"(enclosing function '{context['func_name']}' returns {return_type})"
            ),
        )

        return RepairResult(
            alert=alert,
            status=RepairStatus.SUCCESS,
            edits=[edit],
        )
