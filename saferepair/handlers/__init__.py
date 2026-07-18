"""Repair pattern handlers for SafeRepair."""

from .base import RepairHandler
from .suspicious_realloc import SuspiciousReallocHandler
from .missing_null_check import MissingNullCheckHandler
from .index_check_after_use import IndexCheckAfterUseHandler
from .sprintf_snprintf import SprintfSnprintfHandler

# instances of all avail. handler classes
ALL_HANDLERS: list[RepairHandler] = [
    SuspiciousReallocHandler(),
    MissingNullCheckHandler(),
    IndexCheckAfterUseHandler(),
    SprintfSnprintfHandler(),
]


def get_handler_for_alert(alert) -> RepairHandler | None:
    """returns first handler that can process given alert"""
    for handler in ALL_HANDLERS:
        if handler.can_handle(alert):
            return handler
    return None
