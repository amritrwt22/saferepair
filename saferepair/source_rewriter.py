"""source code line-by-line rewriter for applying repair"""

import logging
from enum import Enum
from pathlib import Path


logger = logging.getLogger(__name__)


class EditType(Enum):
    REPLACE = "replace"
    INSERT_BEFORE = "insert_before"
    INSERT_AFTER = "insert_after"


class SourceRewriter:
    """collects & applies edits in reverse line order, to avoid offset issues"""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.original_text = file_path.read_text(encoding='utf-8', errors='replace')
        self.lines = self.original_text.splitlines(keepends=True)   #each line has own \n
        self._edits: list[tuple[int, EditType, str]] = []  # (line, type, text)

    def replace_line(self, line_num: int, new_text: str) -> None:
        """replace line with new text, include trailing newline if needed"""
        if not new_text.endswith('\n'):
            new_text += '\n'
        self._edits.append((line_num, EditType.REPLACE, new_text))

    def insert_before_line(self, line_num: int, text: str) -> None:
        """insert text before line, include trailing newline if needed"""
        if not text.endswith('\n'):
            text += '\n'
        self._edits.append((line_num, EditType.INSERT_BEFORE, text))

    def insert_after_line(self, line_num: int, text: str) -> None:
        """insert text aftr line, include trailing newline if needed"""
        if not text.endswith('\n'):
            text += '\n'
        self._edits.append((line_num, EditType.INSERT_AFTER, text))

    def apply(self) -> str:
        """apply all edits & returns modified source text

        (primary key) edits sorted by line number desc. 
        (sec. key) for same-line edits, INSERT_BEFORE after INSERT_AFTER and REPLACE in sorted order
        """

        if not self._edits:
            return self.original_text

        lines = list(self.lines)  #edit on a copy

        #sorting edits
        type_order = {
            EditType.INSERT_AFTER: 0,   # applied first
            EditType.REPLACE: 1,
            EditType.INSERT_BEFORE: 2, 
        }
        def sort_key(edit):
            line_num  = edit[0]
            edit_type = edit[1]
            return (-line_num, type_order[edit_type]) #2 keys to find sort pos.
        sorted_edits = sorted(self._edits, key=sort_key)

        #applying edits
        for line_num, edit_type, text in sorted_edits:
            idx = line_num - 1  #0-based

            if idx < 0 or idx >= len(lines):
                logger.warning(
                    f"Edit at line {line_num} is out of range "
                    f"(file has {len(lines)} lines), skipping"
                )
                continue

            if edit_type == EditType.REPLACE:
                lines[idx] = text
            elif edit_type == EditType.INSERT_BEFORE:
                lines.insert(idx, text)
            elif edit_type == EditType.INSERT_AFTER:
                lines.insert(idx + 1, text)

        return ''.join(lines)

    def write(self, output_path: Path) -> str:
        """write edit result to output_path, returns patched text str"""

        patched = self.apply()

        output_path.parent.mkdir(parents=True, exist_ok=True) #makes any missing parent dirs.
        output_path.write_text(patched, encoding='utf-8', errors='replace')
        logger.info(f"Wrote patched file: {output_path}")
        return patched
