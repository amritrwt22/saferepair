"""Handler for suspicious realloc self-assignment pattern.

Detects: p = realloc(p, new_size);
         ptr->field = realloc(ptr->field, new_size);
Fixes:   Introduces a temp. pointer to avoid losing the original on failure.
"""

import logging
import re
from typing import Optional
from clang.cindex import TranslationUnit

from ..models import Alert, RepairResult, RepairStatus, RepairPattern, SourceEdit
from ..source_rewriter import SourceRewriter
from ..ast_analyzer import (
    find_call_expr_at_line,
    get_line_text,
)
from .base import RepairHandler


logger = logging.getLogger(__name__)


# Regex to match: <var> = [(type*)]realloc(<var>, <size>);
REALLOC_SELF_ASSIGN_RE = re.compile(
    r'^(\s*)'                      # group 1: indentation
    r'(\w+)'                       # group 2: LHS variable name
    r'\s*=\s*'                     # assignment opr.
    r'(?:\(\s*\w[\w\s\*]*\)\s*)?'  # optional cast like (char*)
    r'realloc\s*\(\s*'             # realloc(
    r'(\w+)'                       # group 3: first arg (must match LHS)
    r'\s*,\s*'                     # comma
    r'(.+?)'                       # group 4: size expr.
    r'\s*\)\s*;'                   # );
)

# Regex to match: ptr->field = realloc(ptr->field, size);  or  obj.field  = realloc(obj.field,  size);
REALLOC_MEMBER_RE = re.compile(
    r'^(\s*)'                          # group 1: indentation
    r'(\w+(?:(?:\.|->)\w+)+)'          # group 2: LHS like ptr->field or a.b.c
    r'\s*=\s*'                         # assignment opr
    r'(?:\(\s*\w[\w\s\*]*\)\s*)?'      # optional cast
    r'realloc\s*\(\s*'                 # realloc(
    r'(\w+(?:(?:\.|->)\w+)+)'          # group 3: first arg (same member-access form)
    r'\s*,\s*'                         # comma
    r'(.+?)'                           # group 4: size expression
    r'\s*\)\s*;'                       # );
)


class SuspiciousReallocHandler(RepairHandler):
    def can_handle(self, alert: Alert) -> bool:
        return alert.pattern == RepairPattern.SUSPICIOUS_REALLOC

    def analyze(self, alert: Alert, tu: TranslationUnit) -> Optional[dict]:

        # Step 1: Get the source line text
        file_path = alert.file_path
        line_num = alert.line
        line_text = get_line_text(file_path, line_num)
        if not line_text:
            logger.debug(f"Could not read line {line_num} from {file_path}")
            return None

        # Step2: Regex match plain identifier, struct-member forms
        match = REALLOC_SELF_ASSIGN_RE.match(line_text)
        if not match:
            match = REALLOC_MEMBER_RE.match(line_text)
        if not match:
            logger.debug(f"Line does not match realloc: {line_text.strip()}")
            return None

        # Step 3: Verify LHS == first argument (self-assignment)
        indent = match.group(1)
        lhs_var = match.group(2)
        first_arg = match.group(3)
        size_expr = match.group(4)
        if lhs_var != first_arg:
            logger.debug(f"Not self-assignment: {lhs_var} != {first_arg}")
            return None

        # Step4:AST confirm the realloc call
        call_cursor = find_call_expr_at_line(tu, file_path, line_num, "realloc")
        if call_cursor is None:
            logger.debug(f"AST: no realloc call found at line {line_num}")
            return None

        #step5: check if there's a cast (to preserve it in the fix)
        cast_match = re.search(r'=\s*(\(\s*\w[\w\s\*]*\))\s*realloc', line_text)
        cast_expr = cast_match.group(1) if cast_match else None

        return {
            "var_name": lhs_var,
            "size_expr": size_expr.strip(),
            "indent": indent,
            "cast_expr": cast_expr,
            "original_line": line_text,
            "line_num": line_num,
        }

    def generate_fix(
        self,
        alert: Alert,
        context: dict,
        rewriter: SourceRewriter,
    ) -> RepairResult:
        
        var_name = context["var_name"]
        size_expr = context["size_expr"]
        indent = context["indent"]
        cast_expr = context["cast_expr"]
        line_num = context["line_num"]
        original_line = context["original_line"]

        # Building the replacement code
        # void *_sr_tmp = realloc(p, new_size);
        # if (_sr_tmp != NULL) {
        #     p = _sr_tmp;
        # }
        # /* else: realloc failed, p still valid */
        tmp_name = "_sr_tmp"
        assign_cast = f"{cast_expr}" if cast_expr else ""
        fix_lines = [
            f"{indent}{{\n",
            f"{indent}    void *{tmp_name} = realloc({var_name}, {size_expr});\n",
            f"{indent}    if ({tmp_name} != NULL) {{\n",
            f"{indent}        {var_name} = {assign_cast}{tmp_name};\n",
            f"{indent}    }}\n",
            f"{indent}    /* else: realloc failed, {var_name} still valid */\n",
            f"{indent}}}\n",
        ]

        #Apply the edit: replace the single line with the block
        new_text = ''.join(fix_lines)
        rewriter.replace_line(line_num, new_text)

        edit = SourceEdit(
            file_path=alert.file_path,
            line=line_num,
            old_text=original_line.rstrip(),
            new_text=new_text.rstrip(),
            description="Wrap realloc in temp pointer to prevent memory leak on failure",
        )

        return RepairResult(
            alert=alert,
            status=RepairStatus.SUCCESS,
            edits=[edit],
        )
