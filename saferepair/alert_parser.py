"""converts static analysis alert .JSON file -> Alert objects"""

import json
import logging
from pathlib import Path
from .models import Alert


logger = logging.getLogger(__name__)


def parse_alerts(alerts_path: Path, source_dir: Path) -> list[Alert]:
    """args:
        alerts_path: path to JSON file containing array of alert objects
        source_dir: root directory of source code,
                    used to resolve the relative "file" paths in alerts

        returns:
            list of Alert objects; alerts with missing/unresolvable fields are skipped
    """
    try:
        with open(alerts_path, 'r') as f:
            raw_alerts = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {alerts_path}: {e}")
        return []
    except FileNotFoundError:
        logger.error(f"Alert file not found: {alerts_path}")
        return []

    if not isinstance(raw_alerts, list):       #if json not returned as list
        logger.error(f"Expected JSON array in {alerts_path}, got {type(raw_alerts).__name__}")
        return []
 
    alerts = []
    for i, raw in enumerate(raw_alerts):    #list of dicts
        try:
            rule_id = raw["rule_id"]
            line = int(raw["line"])
            column = int(raw.get("column", 0))          #get() cuz optional
            message = raw.get("message", "")

            if "file" not in raw:
                logger.warning(f"Alert #{i}: missing required field 'file', skipping")
                continue

            file_str = raw["file"]
            file_path = source_dir / file_str
            if not file_path.exists():
                # clang-tidy sometimes emits bare filenames without subdirectory;
                # search the tree as a last resort i.e. all files with name under source_dir
                matches = list(source_dir.rglob(Path(file_str).name))
                if not matches:
                    logger.warning(f"Alert #{i}: file not found: {file_str}")
                    continue
                file_path = matches[0]
                if len(matches) > 1:
                    logger.debug(
                        f"Alert #{i}: '{file_str}' matched {len(matches)} files, "
                        f"using {file_path.relative_to(source_dir)}"
                    )

            alerts.append(Alert(
                rule_id=rule_id,
                file_path=file_path.resolve(),
                line=line,
                column=column,
                message=message,
            ))
        except KeyError as e:
            logger.warning(f"Alert #{i}: missing required field {e}, skipping")
        except (TypeError, ValueError) as e:                         
            logger.warning(f"Alert #{i}: value of wrong type: {e}, skipping")

    logger.info(f"Parsed {len(alerts)} alerts from {alerts_path}")
    return alerts
