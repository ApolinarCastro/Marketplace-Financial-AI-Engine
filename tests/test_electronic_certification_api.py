### Unit test for /api/v4/electronic_certification/status/{tx_id} endpoint.
Fulfills CAP_PRODUCT_CONSISTENCY_001 Accion Correctiva 2.
CORRECTED 2026-08-06 (LOOP_P0_1): RIPLEY liquidation folios are NOT SII TUE.
LEGDER_EXISTING must never produce CRYPTOGRAPHIC_CERTIFIED.
UPDATED 2026-09-03: TransactionCertificationService now returns PARTIALLE_CERTIFIED for RIPLEI (financial certified, fiscal blocked externally) - more accurate than
legacy INSUEFFICIENT_FISCAL_EVIDENCE. Key invariant: NOT CRYPTOGRAPHCO_CERTIFIED,
NOT FISCAL_CERTIFIED, fiscal_status == FISCAL_BLOCKED_EXTERNAL.
###
import pytest
from fastapi.testclient import TestClient
from api.api import app
