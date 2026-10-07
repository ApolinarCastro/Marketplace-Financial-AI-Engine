"""Upload Center controlled-UX contract tests (PFO-UPLOAD-CENTER-CONTROLLED-UX-001).

Static structural verification of templates/upload_center.html:
request flags, state vocabulary, labels, escape coverage, extension parity.
Behavioral backend mapping is covered by tests/test_upload_center_e2e.py.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "upload_center.html"


@pytest.fixture(scope="module")
def html() -> str:
    return TEMPLATE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def script(html: str) -> str:
    m = re.search(r"<script>(.*)</script>", html, re.DOTALL)
    assert m, "no inline script found"
    return m.group(1)


def test_a_default_validation_is_dry_run(script: str):
    assert "?dry_run=true" in script
    validate_fn = script[script.index("async function validateFile"):script.index("async function validateFile") + 1200]
    assert "dry_run=true" in validate_fn
    assert "confirm_write=true" not in validate_fn


def test_b_no_write_in_validate_flow(script: str):
    assert "dry_run=false" in script  # only processFile may use it
    process_fn = script[script.index("async function processFile"):]
    assert "dry_run=false&confirm_write=true" in process_fn


def test_c_process_locked_before_validation(script: str, html: str):
    assert "Procesar archivos validados" in html
    assert "validatedFiles()" in script
    assert "btnProcess.disabled = !canProcess" in script
    assert "validated > 0" in script


def test_d_classification_from_backend_no_hardcode(script: str):
    for field in ("result.marketplace", "result.document_type", "result.period"):
        assert field in script
    for lit in ("'ML'", '"ML"', "'facturacion'", '"facturacion"', "'2026-01'", '"2026-01"'):
        assert lit not in script, f"hardcoded literal in UI: {lit}"


def test_e_confirmation_displayed(script: str, html: str):
    assert "Confirmar procesamiento" in html
    assert "Esta acción escribirá datos en la base activa." in html
    assert "Cancelar" in html
    assert "openConfirmModal" in script and "closeConfirmModal" in script


def test_f_cancel_sends_zero_requests(script: str):
    close_fn = script[script.index("function closeConfirmModal"):]
    close_fn = close_fn[:close_fn.index("}", close_fn.index("add('hidden')")) + 1]
    assert "fetch(" not in close_fn and "postUpload" not in close_fn


def test_g_confirmed_write_flags(script: str):
    assert "?dry_run=false&confirm_write=true" in script


def test_h_completed_mapping(script: str):
    assert "data.status === 'COMPLETED'" in script
    assert "f.status = 'completed'" in script


def test_i_failed_mapping(script: str):
    assert "f.status = 'failed'" in script
    assert "'Fallido'" in script


def test_j_duplicate_mapping(script: str):
    assert "SKIPPED_DUPLICATE" in script
    assert "f.status = 'duplicate'" in script
    assert "Ya procesado anteriormente" in script


def test_dry_run_validated_label_no_completed(script: str):
    assert "f.status = (data && data.status === 'DRY_RUN') ? 'validated' : 'failed'" in script
    assert "'Validado" in script
    assert "No se han escrito datos" in script


def test_multifile_validated_only(script: str):
    assert "files.filter(f => f.status === 'validated')" in script
    validate_all = script[script.index("async function validateAll"):]
    validate_all = validate_all[:validate_all.index("async function validateFile")]
    assert "f.status === 'pending'" in validate_all


def test_pending_button_label(script: str, html: str):
    assert "Validar archivos" in html
    assert "Subir Todo" not in html
    assert "'Completado'" not in script


def test_extensions_match_backend(script: str, html: str):
    assert "'.xlsx', '.csv', '.xml'" in script or '".xlsx", ".csv", ".xml"' in script or \
        "'.xlsx','.csv','.xml'" in script.replace(" ", "")
    assert ".zip" not in script.lower().replace("kpi-label", "")
    assert "Solo XLSX, CSV, XML" in html


def test_xss_safe_rendering(script: str):
    # Every interpolation carrying external data must pass through esc().
    # External tokens: file/result/meta payloads, error lists, loop vars.
    render_zone = script[script.index("function render()"):]
    interpolations = re.findall(r"\$\{([^}]+)\}", render_zone)
    assert interpolations, "no interpolations found (unexpected)"
    external = re.compile(r"f\.file|f\.result|f\.id|meta\.|\berrors\b|\bwarnings\b|\blabel\b|\bvalue\b|\berr\b|resp\.")
    unsafe = [expr for expr in interpolations
              if external.search(expr) and "esc(" not in expr]
    assert unsafe == [], f"unescaped external interpolations: {unsafe}"
    # No inline onclick handlers carrying identifiers (event delegation instead).
    assert "onclick=\"removeFile" not in script
    # esc() itself neutralizes the five HTML metacharacters.
    for entity in ("&lt;", "&quot;"):
        assert entity in script


def test_remove_resets_state(script: str):
    assert "files = files.filter(f => f.id !== id)" in script


def test_badge_counts(script: str):
    for token in ("pendientes", "validados", "procesados", "fallidos", "ya procesados"):
        assert token in script, token


def test_busy_reverts_to_validated_no_autoretry(script: str):
    assert "WRITE_IN_PROGRESS" in script
    assert "Otro procesamiento está en curso. Intenta nuevamente cuando finalice." in script
    assert "f.status = 'validated'" in script
    assert "Promise.all" not in script
    # No retry timers anywhere: user decides when to reprocess manually.
    assert "setTimeout" not in script
    assert "setInterval" not in script


def test_ui_write_mode_sequential(script: str):
    assert "for (const f of targets)" in script
    assert "await processFile(f)" in script


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
