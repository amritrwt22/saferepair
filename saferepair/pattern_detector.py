"""maps static analyzer rule_ids -> RepairPattern enum values"""

import logging
from .models import Alert, RepairPattern

logger = logging.getLogger(__name__)


#diff. tools & rules hav diff. names for same error
RULE_TO_PATTERN: dict[str, RepairPattern] = {
    "bugprone-suspicious-realloc-usage": RepairPattern.SUSPICIOUS_REALLOC,

    "CWE-690": RepairPattern.MISSING_NULL_CHECK_MALLOC,
    "clang-analyzer-unix.Malloc": RepairPattern.MISSING_NULL_CHECK_MALLOC,

    "V781": RepairPattern.INDEX_CHECK_AFTER_USE,

    "CWE-120": RepairPattern.SPRINTF_UNBOUNDED,
    "cert-err33-c": RepairPattern.SPRINTF_UNBOUNDED,
    "clang-analyzer-security.insecureAPI.DeprecatedOrUnsafeBufferHandling": RepairPattern.SPRINTF_UNBOUNDED,
}


def classify_alerts(alerts: list[Alert]) -> list[Alert]:
    """sets alert.pattern for each recognized alert, 
       and returns alerts that match a supported pattern
    """
    classified = []
    for alert in alerts:
        pattern = RULE_TO_PATTERN.get(alert.rule_id)
        if pattern is not None:
            alert.pattern = pattern
            classified.append(alert)
        else:
            logger.debug(f"Unrecognized rule_id '{alert.rule_id}', skipping: {alert}")

    logger.info(
        f"Classified {len(classified)}/{len(alerts)} alerts "
        f"({len(alerts) - len(classified)} unrecognized)"
    )
    return classified
