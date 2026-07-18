"""checks if patched code compiles"""

import logging
import shutil
import subprocess
from pathlib import Path

from .models import CompileResult, ValidationResult, RepairResult, RepairStatus


logger = logging.getLogger(__name__)


def compile_check(
    file_path: Path,
    compiler: str = "gcc",
    compile_args: list[str] | None = None,
) -> CompileResult:
    """compile-check C file using gcc -fsyntax-only"""
    if compile_args is None:
        compile_args = ["-c", "-fsyntax-only"]      #compile-only (no `main()` needed) and only check syntax+type errors

    # Check if compiler avail.
    if not shutil.which(compiler):
        return CompileResult(
            file_path=file_path,
            success=False,
            output=f"Compiler not found: {compiler}",
            return_code=-1,
        )

    #run command
    cmd = [compiler] + compile_args + [str(file_path)]
    try:
        proc = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30,
        )
        return CompileResult(
            file_path=file_path,
            success=(proc.returncode == 0),
            output=proc.stderr.strip(),
            return_code=proc.returncode,
        )
    except subprocess.TimeoutExpired:
        return CompileResult(
            file_path=file_path,
            success=False,
            output="Compilation timed out (30s)",
            return_code=-1,
        )
    except OSError as e:
        return CompileResult(
            file_path=file_path,
            success=False,
            output=f"Failed to run compiler: {e}",
            return_code=-1,
        )


def validate_repairs(
    output_dir: Path,
    results: list[RepairResult],
    compiler: str = "gcc",
    compile_args: list[str] | None = None,
) -> list[ValidationResult]:
    """compile-checks all successfully repaired files & returns results"""

    #unique file paths that had successful repairs
    repaired_files: set[Path] = set()              #set so no-duplicates
    for r in results:
        if r.status == RepairStatus.SUCCESS:
            repaired_files.add(r.alert.file_path)

    #run checks on each filee
    validations: list[ValidationResult] = []
    for original_path in sorted(repaired_files):                #sorted to give result in same order every run
        #find patched file of same name in patched output dir.
        matches = list(output_dir.rglob(original_path.name))         #rglob searches file in whole folder
        if not matches:
            logger.warning(
                f"Patched file not found for {original_path.name} in {output_dir}"
            )
            continue

        patched_path = matches[0]
        cr = compile_check(patched_path, compiler, compile_args)
        validations.append(ValidationResult(
            file_path=patched_path,
            compile_result=cr,
        ))

    return validations
