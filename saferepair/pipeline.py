"""core repair pipeline"""

import logging
from pathlib import Path

from .alert_parser import parse_alerts
from .pattern_detector import classify_alerts
from .ast_analyzer import parse_file
from .source_rewriter import SourceRewriter
from .handlers import get_handler_for_alert
from .models import RepairResult, RepairStatus


logger = logging.getLogger(__name__)


def repair_pipeline(
    alerts_path: Path,
    source_dir: Path,
    output_dir: Path,
    progress_fn=None,
) -> tuple[list[RepairResult], dict[str, tuple[str, str]]]:
    """runs core repair pipeline on a single alerts file + source dir.

       returns (results, file_texts), where file_texts is
       filename->(original_text, patched_text) for diff gen.
    """

    #step1: parse alerts (alert_parser.py)
    alert_list = parse_alerts(alerts_path, source_dir)
    if not alert_list:
        if progress_fn: progress_fn("No alerts parsed. Nothing to do.")
        return [], {}
    if progress_fn: progress_fn(f"Parsed {len(alert_list)} alert(s)")


    #step2: classify alerts by pattern (pattern_detector.py)
    classified = classify_alerts(alert_list)
    if not classified:
        if progress_fn: progress_fn("No alerts match supported patterns. Nothing to do.")
        return [], {}
    if progress_fn: progress_fn(f"Classified {len(classified)} alert(s) into supported patterns")


    #group alerts by file for efficiencyy
    alerts_by_file: dict[Path, list] = {}
    for alert in classified:
        alerts_by_file.setdefault(alert.file_path, []).append(alert)    #.setdefault(key, default) inserts key:default (if not there alrdy) & returns default


    #process each file
    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[RepairResult] = []
    file_texts: dict[str, tuple[str, str]] = {}     #filename -> (original, patched)

    for file_path, file_alerts in alerts_by_file.items():
        if progress_fn: progress_fn(f"\nProcessing {file_path.name} ({len(file_alerts)} alert(s))...")

        #step3: parse file with libclang (ast_analyzer.py)
        tu = parse_file(file_path)
        if tu is None:                               #mark all fail
            for alert in file_alerts:
                results.append(RepairResult(
                    alert=alert,
                    status=RepairStatus.FAILED,
                    error_message=f"Failed to parse {file_path}",
                ))
            continue

        #step4: rewriter instance (source_rewriter.py)
        rewriter = SourceRewriter(file_path)

        for alert in file_alerts:
            handler = get_handler_for_alert(alert)
            if handler is None:                          #mark all skip
                logger.warning(f"No handler for pattern {alert.pattern}: {alert}")
                results.append(RepairResult(
                    alert=alert,
                    status=RepairStatus.SKIPPED,
                    error_message=f"No handler available for {alert.pattern}",
                ))
                continue

            #analyze context
            context = handler.analyze(alert, tu)
            if context is None:
                if progress_fn: progress_fn(f"  SKIP: {alert.rule_id} at line {alert.line} (analysis failed)")
                results.append(RepairResult(
                    alert=alert,
                    status=RepairStatus.SKIPPED,
                    error_message="AST analysis could not confirm the pattern",
                ))
                continue

            #generate fix
            result = handler.generate_fix(alert, context, rewriter)
            results.append(result)

            status_icon = "OK" if result.success else "FAIL"
            if progress_fn: progress_fn(f"  {status_icon}: {alert.rule_id} at line {alert.line}")

        #write patched file
        #fiind rel. path from source_dir (to try preserve dir. structure in output_dir)
        try:
            rel_path = file_path.relative_to(source_dir)
        except ValueError:
            rel_path = Path(file_path.name)

        output_file = output_dir / rel_path
        patched_text = rewriter.write(output_file)
        file_texts[file_path.name] = (rewriter.original_text, patched_text)

    return results, file_texts
