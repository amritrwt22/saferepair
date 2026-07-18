"""Handler for index-check-after-use pattern (PVS-Studio V781).

Detects: while (buf[i] != '\0' && i < len) i.e. out-of-bounds read if i >= len
Fixes:   while (i < len && buf[i] != '\0') i.e. safe order
Skips:   if left operand has ++ or --, swap could change behaviour so such case skipped
"""

import logging
import re
from pathlib import Path
from typing import Optional
from clang.cindex import TranslationUnit

from ..models import Alert, RepairResult, RepairStatus, RepairPattern, SourceEdit
from ..source_rewriter import SourceRewriter
from ..ast_analyzer import get_line_text
from .base import RepairHandler


logger = logging.getLogger(__name__)


_CONTROL_RE = re.compile(r'\b(while|if|for)\s*\(')     # matches while (, if (, for (
_SUBSCRIPT_RE = re.compile(r'\b\w+\s*\[([^\]]+)\]')    # matches something[index], captures what's inside the bracket
_IDENT_RE = re.compile(r'\b([A-Za-z_]\w*)\b')          # match any identifier (i.e. word starting with letter or underscore)
_SIDE_EFFECT_RE = re.compile(r'\+\+|--')               # matches ++ or --

# look like identifiers but are keywords
_COMMON_KEYWORDS = {
    'sizeof', 'NULL', 'null', 'true', 'false',
    'int', 'char', 'unsigned', 'long', 'short', 'void',
    'const', 'static', 'if', 'else', 'return',
}


def strip_line_comment(line: str) -> str:
    """Remove // comment from end of line, except in strings"""
    in_str = False
    for i, c in enumerate(line): #through each char. of line
        if c == '"' and (i == 0 or line[i - 1] != '\\'):     #not an \" escaped quote false +ive
            in_str = not in_str
        if not in_str and c == '/' and i + 1 < len(line) and line[i + 1] == '/':
            return line[:i]
    return line


def blank_string_literals(text: str) -> str:
    """returns text with string literal content replaced with spaces, to avoid false && matches"""
    result = []
    in_str = False
    for i, c in enumerate(text):
        if not in_str and c == '"':
            in_str = True
            result.append(c)
        elif in_str and c == '"' and (i == 0 or text[i - 1] != '\\'):   #not an \" escaped quote false +ive
            in_str = False
            result.append(c)
        elif in_str:
            result.append(' ')
        else:
            result.append(c)
    return ''.join(result)


def paren_closed(text: str) -> bool:
    """return true when the first while(...)/for(...)/if(...) block in text is complete"""
    m = _CONTROL_RE.search(text)
    if not m:
        return False
    depth = 0
    for c in text[m.end() - 1:]:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0:
                return True
    return False


def _extract_condition(
    file_path: Path, start_line: int
) -> tuple[Optional[str], Optional[str], int, int]:
    """Read lines starting from alert line and extract a while/if/for condition
    can handles multi-line conditions by joining <=10 consecutive lines

    returns:
        (keyword, condition_str, first_line_no, last_line_no) or
        (None,    None,          start_line_no, start_line_no) on failure.
    """

    # collect lines until the opening paren is closed (or 10 lines max)
    gathered: list[tuple[int, str]] = []   #(line_no, line_text)
    for ln in range(start_line, start_line + 10):
        text = get_line_text(file_path, ln)
        if not text:
            break
        gathered.append((ln, strip_line_comment(text)))
        combined = ' '.join(t for _, t in gathered)
        if paren_closed(combined):
            break

    if not gathered:
        return None, None, start_line, start_line

    combined_raw = ' '.join(t for _, t in gathered)
    combined_clean = blank_string_literals(combined_raw)   # hide string contents before parsing

    m = _CONTROL_RE.search(combined_clean)
    if not m:
        return None, None, start_line, start_line


    # extract conditions part from collected lines
    keyword = m.group(1)
    open_pos = m.end() - 1   # index of the '('
    depth = 0
    body_chars: list[str] = []

    # walk forward tracking paren depth to find the matching ')'
    for i in range(open_pos, len(combined_clean)):
        c = combined_clean[i]
        if c == '(':
            depth += 1
            if depth > 1:
                body_chars.append(combined_raw[i])  # keep '(' if a nested one
        elif c == ')':
            depth -= 1
            if depth == 0:
                break
            body_chars.append(combined_raw[i])
        else:
            if depth >= 1:
                body_chars.append(combined_raw[i])

    if depth != 0:
        return None, None, start_line, start_line

    full_body = ''.join(body_chars).strip() #all stuff in (...)
    # for loops: extract middle segment (init; COND; update)
    condition = for_middle_segment(full_body) if keyword == 'for' else full_body

    first_line = gathered[0][0]
    last_line = gathered[-1][0]
    return keyword, condition, first_line, last_line


def for_middle_segment(body: str) -> str:
    """extract condition segment from for-loop body (init; COND; update)"""
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for c in body:
        if c in '([{':
            depth += 1
            current.append(c)
        elif c in ')]}':
            depth -= 1
            current.append(c)
        elif c == ';' and depth == 0: #splits on ; but only on depth=0
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(c)
    parts.append(''.join(current).strip())
    return parts[1] if len(parts) >= 2 else ''


def split_top_level_and(text: str) -> list[str]:
    """Split text at && operators that arent inside () or []"""
    parts: list[str] = []
    current: list[str] = []
    dp = db = 0   # paren & brackt depth
    i = 0
    while i < len(text):
        c = text[i]
        if c == '(':
            dp += 1; current.append(c)
        elif c == ')':
            dp -= 1; current.append(c)
        elif c == '[':
            db += 1; current.append(c)
        elif c == ']':
            db -= 1; current.append(c)
        elif (c == '&' and i + 1 < len(text) and text[i + 1] == '&'
              and dp == 0 and db == 0):
            # top-level && found: flush current segment
            parts.append(''.join(current).strip())
            current = []
            i += 2
            continue
        else:
            current.append(c)
        i += 1
    if current:
        parts.append(''.join(current).strip())
    return [p for p in parts if p]


def subscript_index_vars(expr: str) -> set[str]:
    """returns identifiers used as array subscript indices i.e. i from buf[i]"""
    result: set[str] = set()
    for m in _SUBSCRIPT_RE.finditer(expr): #iterates over all subscripts found
        for id_m in _IDENT_RE.finditer(m.group(1)):
            name = id_m.group(1)
            if name not in _COMMON_KEYWORDS:
                result.add(name)
    return result


def is_bound_check(expr: str, var: str) -> bool:
    """return true if expr contains a bound-check comparison on var."""
    v = re.escape(var)
    if re.search(r'\b' + v + r'\b\s*(?:<|<=|!=)\s*\S', expr):  # var < N  /  var != N
        return True
    if re.search(r'\S\s*(?:>|>=)\s*\b' + v + r'\b', expr):     # N > var  /  N >= var
        return True
    return False


def _find_v781_pair(condition: str) -> Optional[tuple[str, str, str]]:
    """Find the first (left, right, var) V781 pair in a condition string.
    (left has arr[var] subscript & has no side effects (++/--), right has bound check on var)

    returns: (left, right, var) or None.
    """

    parts = split_top_level_and(condition)
    if len(parts) < 2:
        return None

    for pi in range(len(parts) - 1):
        left = parts[pi]
        right = parts[pi + 1]

        # skip if ++ / -- in left
        if _SIDE_EFFECT_RE.search(left):
            continue

        idx_vars = subscript_index_vars(left)
        for var in idx_vars:
            #doesnt have bound check on var
            if not is_bound_check(right, var):
                continue
            # skip: right also uses var as index (unusual)
            if var in subscript_index_vars(right):
                continue
            # skip: left already has a bound check 
            if is_bound_check(left, var):
                continue
            return left, right, var

    return None


def _resplit_to_lines(orig_joined: str, fixed_joined: str, n_lines: int) -> list[str]:
    """Re-distribute fixed_joined back into n_lines segments.

    swap only changes text length slightly, so splitlines(keepends=True)
    usually gives the same count, handles edge cases
    """
      
    fixed_parts = fixed_joined.splitlines(keepends=True)

    if len(fixed_parts) == n_lines:
        return fixed_parts

    if n_lines == 1:
        # single-line: preserve the original line ending
        ending = '\n' if orig_joined.endswith('\n') else ''
        return [fixed_joined.rstrip('\n') + ending]

    # pad or truncate to match original line count
    result = list(fixed_parts)
    while len(result) < n_lines:
        result.append('')
    return result[:n_lines]



class IndexCheckAfterUseHandler(RepairHandler):
    def can_handle(self, alert: Alert) -> bool:
        return alert.pattern == RepairPattern.INDEX_CHECK_AFTER_USE

    def analyze(self, alert: Alert, tu: TranslationUnit) -> Optional[dict]:
        """locate the V781 pattern at the alert line via text analysis"""

        file_path = alert.file_path
        line_num = alert.line

        line_text = get_line_text(file_path, line_num)
        if not line_text:
            logger.debug(f"Could not read line {line_num} from {file_path}")
            return None

        # step 1: extract full while/if/for condition
        keyword, condition, first_line, last_line = _extract_condition(file_path, line_num)
        if not condition or '&&' not in condition:
            logger.debug(f"No && condition found starting at line {line_num}")
            return None

        # step2: locate the V781 (left, right, var) part
        pair = _find_v781_pair(condition)
        if pair is None:
            logger.debug(
                f"No V781 pattern in condition at line {line_num}: "
                f"{condition[:80]!r}"   # the !r adds \n char. not actually puts on nextline, for logging later 
            )
            return None

        left, right, var = pair

        #step3: collect raw source lines so generate_fix can rewrite them
        source_lines: list[tuple[int, str]] = []
        for ln in range(first_line, last_line + 1):
            source_lines.append((ln, get_line_text(file_path, ln)))

        return {
            'var': var,
            'left': left,
            'right': right,
            'condition': condition,
            'first_line': first_line,
            'last_line': last_line,
            'source_lines': source_lines,
        }

    def generate_fix(
        self,
        alert: Alert,
        context: dict,
        rewriter: SourceRewriter,
    ) -> RepairResult:
        
        left = context['left']
        right = context['right']
        source_lines: list[tuple[int, str]] = context['source_lines']
        var = context['var']

        orig_pair = f"{left} && {right}"
        fixed_pair = f"{right} && {left}"

        # step 1: join all source lines, then swap the operand pair in one shot
        joined = ''.join(text for _, text in source_lines)
        if orig_pair in joined:
            fixed_joined = joined.replace(orig_pair, fixed_pair, 1)
        else:
            # fallback: match with flexible whitespace around &&
            pattern = re.escape(left) + r'\s*&&\s*' + re.escape(right)
            m = re.search(pattern, joined)
            if not m:
                logger.warning(
                    f"Could not locate swap target in lines "
                    f"{context['first_line']}-{context['last_line']}: "
                    f"{orig_pair!r}"
                )
                return RepairResult(
                    alert=alert,
                    status=RepairStatus.FAILED,
                    error_message=f"swap target not found in source: {orig_pair!r}",
                )
            fixed_joined = joined[:m.start()] + fixed_pair + joined[m.end():]

        #step2: re-split fixed text back into per-line strings
        fixed_lines = _resplit_to_lines(joined, fixed_joined, len(source_lines))

        #step3: apply only lines that actually changed
        edits: list[SourceEdit] = []
        for (ln, orig_text), new_text in zip(source_lines, fixed_lines):
            if new_text == orig_text:
                continue
            rewriter.replace_line(ln, new_text)
            edits.append(SourceEdit(
                file_path=alert.file_path,
                line=ln,
                old_text=orig_text.rstrip('\n'),
                new_text=new_text.rstrip('\n'),
                description=(
                    f"Swap && operands: move bound check '{right.strip()}' "
                    f"before array access '{var}[...]' "
                    f"(V781: index used before bound check)"
                ),
            ))

        if not edits:
            return RepairResult(
                alert=alert,
                status=RepairStatus.FAILED,
                error_message="no lines changed after operand swap (no-op fix)",
            )

        return RepairResult(
            alert=alert,
            status=RepairStatus.SUCCESS,
            edits=edits,
        )
