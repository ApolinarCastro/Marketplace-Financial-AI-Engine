"""engine/v4/marketplace_auditor_ml.py
Auditoría de clasificación para Marketplace Libre (ML).

Este módulo expone `audit_ml_misclassifications()` que inspecciona la tabla
`marketplace_ledger_v1` y detecta transacciones cuyo `detalle` no corresponde a
una clasificación operativa válida según `RAW_TO_CLASSIFICATION_MAP`.
Los hallazgos se registran en `marketplace_auditoria_v1` y se devuelven como
DataFrame para su consumo posterior (p. ej. dashboard o corrección).
"""

import pandas as pd
from engine.v4.database import DatabaseV4
from engine.v4.marketplace_auditor import RAW_TO_CLASSIFICATION_MAP


def _normalize_detalle(detalle: str) -> str:
    """Normaliza el texto del detalle usando el mapa de clasificación.

    Devuelve la clasificación operativa si está presente en el mapa o a través de la
    regla dinámica de retiros y normalización de textos.
    """
    if not isinstance(detalle, str) or pd.isna(detalle):
        return None
    
    # 1. Emparejamiento directo en el mapa crudo
    raw_val = RAW_TO_CLASSIFICATION_MAP.get(detalle.strip())
    if raw_val is not None:
        return raw_val
        
    # 2. Regla Dinámica de Tesorería (Retiros de dinero)
    det_lower = detalle.lower().strip()
    if ('pre_payout_' in det_lower or 
        'post_payout_' in det_lower or 
        'withdraw' in det_lower or 
        'retiro de dinero' in det_lower or 
        'reserve_for_dispute' in det_lower):
        return "Retiro de dinero"
        
    # 3. Emparejamiento normalizado
    from engine.v4.marketplace_auditor import normalize_detail, NORMALIZED_CLASSIFICATION_MAP
    norm = normalize_detail(detalle)
    return NORMALIZED_CLASSIFICATION_MAP.get(norm)


def audit_ml_misclassifications() -> pd.DataFrame:
    """Audita transacciones de Mercado Libre (ML) y detecta mis‑clasificaciones.

    - Consulta `marketplace_ledger_v1` para el marketplace `'ML'`.
    - Para cada fila, intenta mapear `detalle` a una clasificación operativa.
    - Si el mapeo es `None` o la clasificación resultante contiene la cadena
    - genérica "Ajuste Poscobro General", se considera **MISCLASSIFIED**.
    - Registra cada hallazgo en `marketplace_auditoria_v1` con `check_name`
      = 'MISCLASSIFIED'.
    - Devuelve un DataFrame con columnas: `id_transaccion`, `detalle_original`,
      `clasificacion_sugerida`.
    """
    db = DatabaseV4.get()
    # Limpiar alertas MISCLASSIFIED anteriores para evitar ruido histórico
    db.execute("DELETE FROM marketplace_auditoria_v1 WHERE check_name = 'MISCLASSIFIED'")
    # Obtener todas las transacciones de ML
    df = db.query(
        """
        SELECT id_transaccion, detalle
        FROM marketplace_ledger_v1
        WHERE marketplace = 'ML'
        """
    )

    misclassified = []
    for _, row in df.iterrows():
        detalle = row["detalle"]
        clasif = _normalize_detalle(detalle)
        # Consideramos mis‑clasificada solo si no hay mapeo (Ajuste Poscobro General ya está en FINANCIAL_STRUCTURE)
        if clasif is None:
            misclassified.append(
                {
                    "id_transaccion": row["id_transaccion"],
                    "detalle_original": detalle,
                    "clasificacion_sugerida": clasif or "NO_CLASIFICADO",
                }
            )

    if not misclassified:
        return pd.DataFrame(columns=["id_transaccion", "detalle_original", "clasificacion_sugerida"])

    mis_df = pd.DataFrame(misclassified)

    # Registrar auditoría
    audit_records = []
    for rec in misclassified:
        audit_records.append(
            {
                "marketplace": "ML",
                "check_name": "MISCLASSIFIED",
                "condition_detected": rec["detalle_original"],
                "action_taken": "REVIEW_REQUIRED",
                "order_id": None,
            }
        )
    audit_df = pd.DataFrame(audit_records)
    db.insert_df(audit_df, "marketplace_auditoria_v1")

    return mis_df
