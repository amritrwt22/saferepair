"""eval-case tests: run full pipeline, assert expected outcomes"""

import json
from pathlib import Path
import pytest

from saferepair.alert_parser import parse_alerts
from saferepair.ast_analyzer import parse_file
from saferepair.handlers import get_handler_for_alert
from saferepair.models import RepairResult, RepairStatus
from saferepair.pattern_detector import classify_alerts
from saferepair.source_rewriter import SourceRewriter

#paths in list
EVAL_CASES_DIR = Path(__file__).parent             #__file__ gives file path of curr. path

#iterdir() returns all subdirs. & files, sorted() ensures same ordering, only dirs. with all 3 files in list
CASES = [d for d in sorted(EVAL_CASES_DIR.iterdir()) if d.is_dir() and (d / "alerts.json").exists() and (d / "test.c").exists() and (d / "expected.json").exists()]


@pytest.mark.parametrize("case_dir", CASES, ids=[d.name for d in CASES])
def test_eval_case(case_dir, tmp_path):
    expected = json.loads((case_dir / "expected.json").read_text())

    alerts = parse_alerts(case_dir / "alerts.json", case_dir)
    assert alerts, f"No alerts parsed in {case_dir.name}"

    classified = classify_alerts(alerts)
    alerts_by_file: dict[Path, list] = {}
    for alert in classified:
        alerts_by_file.setdefault(alert.file_path, []).append(alert)

    results: list[RepairResult] = []
    for file_path, file_alerts in alerts_by_file.items():
        tu = parse_file(file_path)
        assert tu is not None, f"Failed to parse {file_path}"
        rewriter = SourceRewriter(file_path)
        for alert in file_alerts:
            handler = get_handler_for_alert(alert)
            if handler is None:
                results.append(RepairResult(alert=alert, status=RepairStatus.SKIPPED,
                                            error_message="No handler"))
                continue
            context = handler.analyze(alert, tu)
            if context is None:
                results.append(RepairResult(alert=alert, status=RepairStatus.SKIPPED,
                                            error_message="Analysis returned None"))
                continue
            results.append(handler.generate_fix(alert, context, rewriter))
        rewriter.write(tmp_path / file_path.name)

    success = sum(1 for r in results if r.status == RepairStatus.SUCCESS)
    skipped = sum(1 for r in results if r.status == RepairStatus.SKIPPED)

    assert success == expected["success"], (
        f"[{case_dir.name}] expected {expected['success']} SUCCESS, got {success}"
    )
    assert skipped == expected["skipped"], (
        f"[{case_dir.name}] expected {expected['skipped']} SKIPPED, got {skipped}"
    )
