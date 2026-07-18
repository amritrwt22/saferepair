"""integration tests for full SafeRepair pipeline

Each pattern runs full pipeline against unit_cases/<pattern>/ dir.
Assertions cover: repair_pipeline -> validate -> report
"""

from pathlib import Path
import pytest

from saferepair.models import RepairStatus
from saferepair.pipeline import repair_pipeline
from saferepair.validator import validate_repairs


PATTERNS = [
    "suspicious_realloc",
    "missing_null_check",
    "index_check_after_use",
    "sprintf_snprintf",
]


@pytest.mark.parametrize("pattern", PATTERNS)
def test_full_pipeline_with_validation(tmp_path, pattern):
    """full pipeline: repair_pipeline() -> validate -> report"""

    here = Path(__file__).parent   # ...tests/unit_cases/
    source_dir = here / pattern    # ...tests/unit_cases/<pattern>
    alerts_file = here / pattern / "alerts.json"

    assert alerts_file.exists(), f"Missing alerts.json for pattern '{pattern}'"

    # --- repair (uses the shared repair_pipeline from pipeline.py) ----------
    results, _ = repair_pipeline(alerts_file, source_dir, tmp_path)

    assert len(results) >= 1, f"[{pattern}] Expected at least 1 result, got 0"

    success_count = sum(1 for r in results if r.status == RepairStatus.SUCCESS)
    assert success_count >= 1, (
        f"[{pattern}] Expected at least 1 SUCCESS, got {success_count}"
    )

    # --- validate (compile check) -------------------------------------------
    validations = validate_repairs(tmp_path, results)
    for v in validations:
        assert v.compile_result.success, (
            f"[{pattern}] {v.file_path.name} failed compilation:\n"
            f"{v.compile_result.output}"
        )

