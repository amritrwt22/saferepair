"""Base class for all repair pattern handlers."""

from abc import ABC, abstractmethod
from typing import Optional

from clang.cindex import TranslationUnit

from ..models import Alert, RepairResult
from ..source_rewriter import SourceRewriter


class RepairHandler(ABC):
    """Abstract base class for repair handlers
       to ensure each handlr has same interfcee 
    """

    @abstractmethod
    def can_handle(self, alert: Alert) -> bool:
        """return True if this handler can process given alert"""
        ...

    @abstractmethod
    def analyze(self, alert: Alert, tu: TranslationUnit) -> Optional[dict]:
        """analyze alert location in the AST & extract context for fix

        returns:
            dict (containing extracted info needed to generate fix) or 
            None (if alert cant be fixed)
        """
        ...

    @abstractmethod
    def generate_fix(
        self,
        alert: Alert,
        context: dict,
        rewriter: SourceRewriter,
    ) -> RepairResult:
        """Generate and apply the fix using source rewriter

        Returns:
            RepairResult describing the outcome
        """
        ...
