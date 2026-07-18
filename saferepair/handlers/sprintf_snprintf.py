"""Handler for sprintf(fixed_buf, fmt, ...) — missing bounds check (CWE-120)

Detects: sprintf(buf, "%s", s);                 i.e. no bounds, overflow possible
Fixes:   snprintf(buf, sizeof(buf), "%s", s);   i.e. bounded, safe

CWE-120: Buffer Copy without Checking Size of Input
CERT-C MSC24-C: Do not use deprecated or obsolescent functions
"""

import logging
import re
from typing import Optional
from clang.cindex import TranslationUnit

from ..models import Alert, RepairResult, RepairStatus, RepairPattern, SourceEdit
from ..source_rewriter import SourceRewriter
from ..ast_analyzer import find_call_expr_at_line, get_line_text
from .base import RepairHandler


logger = logging.getLogger(__name__)


# detects sprintf calls
SPRINTF_DETECT_RE = re.compile(
    r'\bsprintf\s*\('          # word boundary + sprintf + optional spaces + (
    r'(\s*(?:\([^)]*\)\s*)?)'  # group 1: optional cast like (char *) + whitespaces
    r'(\w+)'                   # group 2: destbuf name 
    r'\s*,'                    # optional whitespaces + first comma (end of first arg.)
)


class SprintfSnprintfHandler(RepairHandler):
    """exampless:
        sprintf(buf, "%s_%d", name, n)
        snprintf(buf, sizeof(buf), "%s_%d", name, n)

        sprintf((char *)type, "%c%d", Ctrl_V, width)
        snprintf((char *)type, sizeof(type), "%c%d", Ctrl_V, width)
    """

    def can_handle(self, alert: Alert) -> bool:
        return alert.pattern == RepairPattern.SPRINTF_UNBOUNDED

    def analyze(self, alert: Alert, tu: TranslationUnit) -> Optional[dict]:
        #step1: read source line
        file_path = alert.file_path
        line_num = alert.line
        line_text = get_line_text(file_path, line_num)
        if not line_text:
            logger.debug(f"Could not read line {line_num} from {file_path}")
            return None

        #step2:skip if line already has snprintf
        if "snprintf" in line_text:
            logger.debug(f"Line already uses snprintf, skipping: {line_text.strip()}")
            return None

        #step3: regex-detect sprintf(buf, ...) pattern to get buffer's name
        m = SPRINTF_DETECT_RE.search(line_text)
        if not m:
            logger.debug(f"Line does not match sprintf pattern: {line_text.strip()}")
            return None
        cast_prefix = m.group(1)   # "(char *)", "", etc.
        buf_name = m.group(2)      # "buf", "type", "titleb", etc.

        #stepp4: AST verify that a sprintf call exists at this line (not just sum comment, etc)
        call_cursor = find_call_expr_at_line(tu, file_path, line_num, "sprintf")
        if call_cursor is None:
            logger.debug(f"AST: no sprintf call found at line {line_num}")
            return None

        return {
            "buf_name": buf_name,
            "cast_prefix": cast_prefix,
            "original_line": line_text,
            "line_num": line_num,
        }

    def generate_fix(
        self,
        alert: Alert,
        context: dict,
        rewriter: SourceRewriter,
    ) -> RepairResult:

        #step1: find 'sprintf' in the line
        original_line = context["original_line"]
        buf_name = context["buf_name"]
        line_num = context["line_num"]
        sprintf_idx = original_line.find("sprintf")
        if sprintf_idx == -1:
            return RepairResult(
                alert=alert,
                status=RepairStatus.FAILED,
                error_message="'sprintf' not found in source line",
            )

        #step2: find buf_name after 'sprintf(', then find the first ',' after it
        paren_idx = original_line.find("(", sprintf_idx)
        if paren_idx == -1:
            return RepairResult(
                alert=alert,
                status=RepairStatus.FAILED,
                error_message="opening paren not found after 'sprintf'",
            )
        buf_idx = original_line.find(buf_name, paren_idx)
        if buf_idx == -1:
            return RepairResult(
                alert=alert,
                status=RepairStatus.FAILED,
                error_message=f"buf: '{buf_name}' not found after 'sprintf('",
            )
        comma_idx = original_line.find(",", buf_idx + len(buf_name))
        if comma_idx == -1:
            return RepairResult(
                alert=alert,
                status=RepairStatus.FAILED,
                error_message=f"comma not found after '{buf_name}'",
            )

        #step3: replace with 'snprintf' and insert ', sizeof(buf_name)' at that comma pos.
        before_comma = original_line[:comma_idx]      # substringg
        after_comma = original_line[comma_idx + 1:]   # skip original ','
        new_line = before_comma + f", sizeof({buf_name})," + after_comma
        new_line = new_line[:sprintf_idx] + "snprintf" + new_line[sprintf_idx + 7:]

        rewriter.replace_line(line_num, new_line)

        edit = SourceEdit(
            file_path=alert.file_path,
            line=line_num,
            old_text=original_line.rstrip(),
            new_text=new_line.rstrip(),
            description=(
                f"Replace sprintf with snprintf(buf={buf_name}, "
                f"sizeof({buf_name})) to bound output (CWE-120)"
            ),
        )

        return RepairResult(
            alert=alert,
            status=RepairStatus.SUCCESS,
            edits=[edit],
        )
