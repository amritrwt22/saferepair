"""data models for saferepair"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class RepairPattern(Enum):
    """supported repair patterns"""
    SUSPICIOUS_REALLOC = "suspicious_realloc"
    MISSING_NULL_CHECK_MALLOC = "missing_null_check_malloc"
    INDEX_CHECK_AFTER_USE = "index_check_after_use"
    SPRINTF_UNBOUNDED = "sprintf_unbounded"


class RepairStatus(Enum):
    """outcome of repair attempt"""
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Alert:
    """static analysis alert to be processed"""
    rule_id: str        #rule name frm scanner eg. "bugprone-suspicious-realloc-usage", "CWE-690"
    file_path: Path
    line: int
    column: int         
    message: str        #human readble warning text from scanner
    pattern: Optional[RepairPattern] = None   #initially set to None, then Op[rep]...

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}:{self.column} [{self.rule_id}] {self.message}"


@dataclass
class SourceEdit:
    """single text edit to apply to source file"""
    file_path: Path
    line: int              # 1-based line number
    old_text: str          
    new_text: str          
    description: str       # human-readable description

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line} - {self.description}"


@dataclass
class RepairResult:
    """result of attempting to repair an alert"""
    alert: Alert
    status: RepairStatus
    edits: list[SourceEdit] = field(default_factory=list)  #not =[] (a mutable default), cuz a bug where its shared across all objects 
    original_source: str = ""
    patched_source: str = ""
    error_message: str = ""

    @property
    def success(self) -> bool:
        return self.status == RepairStatus.SUCCESS


@dataclass
class CompileResult:
    """result of compiling a file with gcc"""
    file_path: Path
    success: bool
    output: str          # stderr text from gcc (warns, errors, etc.)
    return_code: int     # exit code from gcc (0=ok, other = bad)


@dataclass
class ValidationResult:
    """validation result for a repaired file"""
    file_path: Path
    compile_result: CompileResult
