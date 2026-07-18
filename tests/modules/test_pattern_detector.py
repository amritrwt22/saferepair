"""Tests for the pattern detector module."""

from pathlib import Path

from saferepair.models import Alert, RepairPattern
from saferepair.pattern_detector import classify_alerts, RULE_TO_PATTERN


def _alert(rule_id):
    return Alert(rule_id=rule_id, file_path=Path("f.c"), line=1, column=0, message="test")


# ---------------------------------------------------------------------------
# RULE_TO_PATTERN mapping completeness
# ---------------------------------------------------------------------------

def test_all_four_patterns_are_mapped():
    """every RepairPattern must have at least one rule_id mapping."""
    mapped = set(RULE_TO_PATTERN.values())
    for pattern in RepairPattern:
        assert pattern in mapped, f"{pattern} has no rule_id in RULE_TO_PATTERN"


def test_known_rule_ids_map_correctly():
    assert RULE_TO_PATTERN["bugprone-suspicious-realloc-usage"]  == RepairPattern.SUSPICIOUS_REALLOC
    assert RULE_TO_PATTERN["CWE-690"]                            == RepairPattern.MISSING_NULL_CHECK_MALLOC
    assert RULE_TO_PATTERN["clang-analyzer-unix.Malloc"]         == RepairPattern.MISSING_NULL_CHECK_MALLOC
    assert RULE_TO_PATTERN["V781"]                               == RepairPattern.INDEX_CHECK_AFTER_USE
    assert RULE_TO_PATTERN["CWE-120"]                            == RepairPattern.SPRINTF_UNBOUNDED
    assert RULE_TO_PATTERN["cert-err33-c"]                       == RepairPattern.SPRINTF_UNBOUNDED
    assert RULE_TO_PATTERN["clang-analyzer-security.insecureAPI.DeprecatedOrUnsafeBufferHandling"] \
                                                                 == RepairPattern.SPRINTF_UNBOUNDED


# ---------------------------------------------------------------------------
# classify_alerts
# ---------------------------------------------------------------------------

def test_known_rule_id_is_classified():
    alerts = [_alert("bugprone-suspicious-realloc-usage")]
    result = classify_alerts(alerts)
    assert len(result) == 1
    assert result[0].pattern == RepairPattern.SUSPICIOUS_REALLOC


def test_unknown_rule_id_is_dropped():
    alerts = [_alert("some-unknown-rule")]
    result = classify_alerts(alerts)
    assert result == []


def test_mixed_known_and_unknown():
    alerts = [
        _alert("CWE-690"),
        _alert("not-a-real-rule"),
        _alert("V781"),
    ]
    result = classify_alerts(alerts)
    assert len(result) == 2
    assert result[0].pattern == RepairPattern.MISSING_NULL_CHECK_MALLOC
    assert result[1].pattern == RepairPattern.INDEX_CHECK_AFTER_USE


def test_empty_input_returns_empty():
    assert classify_alerts([]) == []


def test_pattern_set_on_alert_in_place():
    """classify_alerts mutates the alert's pattern field"""
    alert = _alert("CWE-120")
    assert alert.pattern is None
    classify_alerts([alert])
    assert alert.pattern == RepairPattern.SPRINTF_UNBOUNDED


def test_all_four_patterns_classifiable():
    """One representative rule_id per pattern should classify correctly."""
    cases = [
        ("bugprone-suspicious-realloc-usage", RepairPattern.SUSPICIOUS_REALLOC),
        ("CWE-690",                           RepairPattern.MISSING_NULL_CHECK_MALLOC),
        ("V781",                              RepairPattern.INDEX_CHECK_AFTER_USE),
        ("CWE-120",                           RepairPattern.SPRINTF_UNBOUNDED),
    ]
    for rule_id, expected_pattern in cases:
        result = classify_alerts([_alert(rule_id)])
        assert len(result) == 1
        assert result[0].pattern == expected_pattern, f"Failed for {rule_id}"
