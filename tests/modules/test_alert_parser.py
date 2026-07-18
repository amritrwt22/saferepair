"""tests for alert_parser.py"""

import json
import pytest

from saferepair.alert_parser import parse_alerts


@pytest.fixture
def source_dir(tmp_path):
    """create dummy .c file inside new temp. source dir."""
    c_file = tmp_path / "test.c"
    c_file.write_text("int main() { return 0; }\n")
    return tmp_path


def _write_alerts(tmp_path, alerts_data):
    """write alerts.json & return its path"""
    alerts_file = tmp_path / "alerts.json"
    alerts_file.write_text(json.dumps(alerts_data))
    return alerts_file


# ---------------------------------------------------------------------------
# Basic parsing
# ---------------------------------------------------------------------------

def test_parse_valid_alerts(tmp_path, source_dir):
    alerts_file = _write_alerts(tmp_path, [
        {
            "rule_id": "bugprone-suspicious-realloc-usage",
            "file": "test.c",
            "line": 1,
            "column": 5,
            "message": "suspicious realloc",
        }
    ])
    alerts = parse_alerts(alerts_file, source_dir)
    assert len(alerts) == 1
    assert alerts[0].rule_id == "bugprone-suspicious-realloc-usage"
    assert alerts[0].line == 1
    assert alerts[0].column == 5


def test_parse_empty_alerts(tmp_path, source_dir):
    alerts_file = _write_alerts(tmp_path, [])
    alerts = parse_alerts(alerts_file, source_dir)
    assert alerts == []


# ---------------------------------------------------------------------------
# file_path key (alternative to file key)
# ---------------------------------------------------------------------------

def test_parse_using_file_path_key(tmp_path, source_dir):
    """parser supports both 'file' and 'file_path' keys"""
    alerts_file = _write_alerts(tmp_path, [
        {
            "rule_id": "CWE-690",
            "file_path": str(source_dir / "test.c"),
            "line": 1,
            "column": 0,
            "message": "null check missing",
        }
    ])
    alerts = parse_alerts(alerts_file, source_dir)
    assert len(alerts) == 1
    assert alerts[0].rule_id == "CWE-690"


# ---------------------------------------------------------------------------
# Optional field defaults
# ---------------------------------------------------------------------------

def test_parse_column_defaults_to_zero(tmp_path, source_dir):
    """column is optional so should default to 0 when absen"""
    alerts_file = _write_alerts(tmp_path, [
        {"rule_id": "V781", "file": "test.c", "line": 1, "message": "index check"}
    ])
    alerts = parse_alerts(alerts_file, source_dir)
    assert len(alerts) == 1
    assert alerts[0].column == 0


def test_parse_message_defaults_to_empty(tmp_path, source_dir):
    """message is optional so should default to '' when absent"""
    alerts_file = _write_alerts(tmp_path, [
        {"rule_id": "CWE-120", "file": "test.c", "line": 1, "column": 0}
    ])
    alerts = parse_alerts(alerts_file, source_dir)
    assert len(alerts) == 1
    assert alerts[0].message == ""


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

def test_parse_missing_required_field(tmp_path, source_dir):
    """Alert missing 'line' should be skipped."""
    alerts_file = _write_alerts(tmp_path, [
        {"rule_id": "CWE-690", "file": "test.c", "message": "no line field"},
    ])
    alerts = parse_alerts(alerts_file, source_dir)
    assert len(alerts) == 0


def test_parse_invalid_json(tmp_path, source_dir):
    alerts_file = tmp_path / "bad.json"
    alerts_file.write_text("not json {{{")
    alerts = parse_alerts(alerts_file, source_dir)
    assert alerts == []


def test_parse_non_list_json(tmp_path, source_dir):
    """JSON object instead of array should return []"""
    alerts_file = tmp_path / "object.json"
    alerts_file.write_text(json.dumps({"rule_id": "CWE-690", "line": 1}))
    alerts = parse_alerts(alerts_file, source_dir)
    assert alerts == []


def test_parse_alerts_file_not_found(tmp_path, source_dir):
    alerts = parse_alerts(tmp_path / "missing.json", source_dir)
    assert alerts == []


def test_parse_file_not_found(tmp_path, source_dir):
    """Alert referencing nonexistent source file should be skipped"""
    alerts_file = _write_alerts(tmp_path, [
        {
            "rule_id": "CWE-690",
            "file": "notest.c",
            "line": 1,
            "column": 0,
            "message": "test",
        }
    ])
    alerts = parse_alerts(alerts_file, source_dir)
    assert len(alerts) == 0


def test_parse_multiple_alerts_partial_valid(tmp_path, source_dir):
    """Valid alerts are returned even if some in same file are malformed"""
    alerts_file = _write_alerts(tmp_path, [
        {"rule_id": "CWE-690", "file": "test.c", "line": 1},
        {"rule_id": "V781"},   # missing file & line so  skipped
        {"rule_id": "CWE-120", "file": "test.c", "line": 1},
    ])
    alerts = parse_alerts(alerts_file, source_dir)
    assert len(alerts) == 2
