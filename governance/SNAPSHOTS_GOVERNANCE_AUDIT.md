# AUDITORÍA DE GOBERNANZA DE SNAPSHOTS Y BASES DE DATOS V1

**FECHA:** 2026-07-27 17:17:51
**TOTAL BASES Y SNAPSHOTS DETECTADOS:** **205 archivos**
**TAMAÑO TOTAL ACUMULADO:** **5.312 GB** (5,704,072,595 bytes)
**ESTADO DE REPOSITORIO:** AUDITORÍA COMPLETADA ($0$ ALTERACIONES, $0$ ELIMINACIONES, $0$ COMPRESIONES)

---

## 1. RESUMEN DE PREGUNTAS Y VEREDICTO DE GOBERNANZA

```text
1. ¿Cuántos snapshots y bases existen realmente?:  205 archivos
2. ¿Cuántos pertenecen a certificaciones oficiales?: 10 archivos (Base oficial + copias certificadas)
3. ¿Cuántos pertenecen únicamente a pruebas/temp?:  86 archivos
4. ¿Cuántos son duplicados exactos (mismo hash)?:   61 archivos
5. ¿Cuántos pueden archivarse sin afectar reproducibilidad?: 195 archivos (4.224 GB)
6. Espacio a recuperar mediante archivado gobernado:  ~4.224 GB
7. Espacio a conservar permanentemente por gobierno:    ~1.089 GB
```

---

## 2. MATRIZ DE DECISIÓN Y CLASIFICACIÓN DE SNAPSHOTS

| Snapshot / Ruta | Tamaño | SHA-256 (Primeros 12) | CAP / Fase | Certificación | Clasificación | Acción Recomendada |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| `KnowledgeBase_baseline_v4.zip` | 0.02 MB | `280189e18cb2` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.agents/gstack/browse/src/snapshot.ts` | 0.03 MB | `3ec6cee340e8` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.agents/gstack/browse/test/snapshot.test.ts` | 0.02 MB | `bb4002cc3604` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.agents/gstack/browse/test/fixtures/snapshot.html` | 0.0 MB | `8d656df55291` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.agents/gstack/scripts/capture-baseline.ts` | 0.0 MB | `02a23eda95b6` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.agents/skills/gstack-browse/src/snapshot.ts` | 0.03 MB | `3ec6cee340e8` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.agents/skills/gstack-browse/test/snapshot.test.ts` | 0.02 MB | `bb4002cc3604` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.agents/skills/gstack-browse/test/fixtures/snapshot.html` | 0.0 MB | `8d656df55291` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.claude/memory.db` | 0.17 MB | `50a988fc7bac` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/logs/refs/heads/integration/baseline-v8` | 0.0 MB | `c0fbcfcc47bf` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/refs/heads/integration/baseline-v8` | 0.0 MB | `25ecd50a5b2c` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/refs/tags/baseline-v8-certified` | 0.0 MB | `f7d34619da91` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/refs/tags/BASELINE_V6` | 0.0 MB | `7470b54e4240` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/refs/tags/CERTIFIED_BASELINE_V1` | 0.0 MB | `bcdd739ca957` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/refs/tags/MARKETPLACE_AUDITOR_V3_5_STABLE_BASELINE` | 0.0 MB | `4e14d08f6529` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/refs/tags/PLATFORM_BASELINE_V4` | 0.0 MB | `0d95c8ef5acd` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/worktrees/marketplace-financial-baseline-v8-d15e94e/commondir` | 0.0 MB | `340ddcb67a62` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/worktrees/marketplace-financial-baseline-v8-d15e94e/gitdir` | 0.0 MB | `735b3b181a1a` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/worktrees/marketplace-financial-baseline-v8-d15e94e/HEAD` | 0.0 MB | `3ea05c774ba6` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/worktrees/marketplace-financial-baseline-v8-d15e94e/index` | 0.22 MB | `847c0100be98` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/worktrees/marketplace-financial-baseline-v8-d15e94e/ORIG_HEAD` | 0.0 MB | `3ea05c774ba6` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.git/worktrees/marketplace-financial-baseline-v8-d15e94e/logs/HEAD` | 0.0 MB | `e09b1eed6b51` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.0.db` | 0.87 MB | `d4282fec8729` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.1.db` | 0.88 MB | `2b9bad6d9a87` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.10.db` | 1.18 MB | `eeb8ab517c7e` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.11.db` | 0.69 MB | `0d98e2c201bb` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.12.db` | 0.41 MB | `9067a576194b` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.13.db` | 0.66 MB | `ac9f86efcd39` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.14.db` | 0.84 MB | `958381fe202c` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.15.db` | 0.58 MB | `fb2886dcebe5` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.2.db` | 0.95 MB | `b80b1b53a7b9` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.3.db` | 1.93 MB | `20d9f8b7c6f2` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.4.db` | 2.61 MB | `22004bd02711` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.5.db` | 0.64 MB | `8cd7d4de27e4` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.6.db` | 0.66 MB | `39ff64fea7f2` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.7.db` | 0.64 MB | `ec84805e55d8` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.8.db` | 0.43 MB | `bd6088eda7d2` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.mypy_cache/3.12/cache.9.db` | 0.95 MB | `5fbe323bfadb` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.swarm/memory.db` | 0.26 MB | `d75d048b12b8` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |
| `.venv/Lib/site-packages/playwright/driver/package/lib/vite/traceViewer/snapshot.html` | 0.0 MB | `11c80efe4f44` | Ninguno | **NO** | SNAPSHOT DE PRUEBAS | **ARCHIVAR** |

---

## 3. CLASIFICACIÓN DETALLADA DE CONSERVACIÓN OBLIGATORIA (PERMANENTE)

Las siguientes bases de datos **DEBEN CONSERVARSE OBLIGATORIAMENTE** por formar parte de la línea base oficial, certificaciones de gobierno o verificaciones end-to-end:

- **`data/db/controlled_cap_f2_001.db`** (57.26 MB)
  - **SHA-256:** `fe3213baa83768d6875738145693acd3207a8b5a90f763b1ad657c1d63af9ca4`
  - **CAP / Fase:** CAP-F2-001 (Fase 2)
  - **Evidencia Vinculada:** `EVID-F2-001`
  - **Acción:** CONSERVAR TEMPORAL

- **`data/db/meli_financial_v4.db`** (56.01 MB)
  - **SHA-256:** `311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9`
  - **CAP / Fase:** CAP-TD-001 a 008, CAP-F2-001 (Fase 1, Fase 2)
  - **Evidencia Vinculada:** `EVID-TD-001 a 008, EVID-F2-001`
  - **Acción:** CONSERVAR PERMANENTE

- **`data/db/snapshot_baseline_v6_20260529_105928/meli_financial_v4.db`** (125.26 MB)
  - **SHA-256:** `e1e341ef44e0a61c4e846d34e05d14a4c291dcd904869f20fdf6e9a37fef1c29`
  - **CAP / Fase:** Sprint A1, B2.5C (Fase 1)
  - **Evidencia Vinculada:** `governance/INCIDENT_DB_SURVIVAL_AUDIT.md`
  - **Acción:** CONSERVAR HISTÓRICO

- **`data/db/snapshot_pre_fase2_20260603_112908/meli_financial_v4.db`** (125.01 MB)
  - **SHA-256:** `3939ad54b2442b1d7182aee856265979b6433e04842a6ff7ef7eba957b4915ea`
  - **CAP / Fase:** B2.5C (Fase 1)
  - **Evidencia Vinculada:** `evidence/fase_1b/post_classification_evidence.json`
  - **Acción:** CONSERVAR HISTÓRICO

- **`data/db/snapshot_pre_ripley_rebuild_20260601_172024/meli_financial_v4.db`** (125.26 MB)
  - **SHA-256:** `c341b272da889474d4d9d80586efbe887c5ef0547462bf26d87c01829748518a`
  - **CAP / Fase:** Sprint B2.5C (Fase 1)
  - **Evidencia Vinculada:** `governance/RIPLEY_POST_CLASSIFICATION_CERTIFICATION.md`
  - **Acción:** CONSERVAR HISTÓRICO

- **`data/db/snapshot_pre_ripley_rebuild_20260601_172043/meli_financial_v4.db`** (125.26 MB)
  - **SHA-256:** `88082bbc073af49aab625b859d986f8d2f3eb7f8482ce3b2ce198b8e29a7a3bb`
  - **CAP / Fase:** Sprint B2.5C (Fase 1)
  - **Evidencia Vinculada:** `governance/RIPLEY_POST_CLASSIFICATION_CERTIFICATION.md`
  - **Acción:** CONSERVAR HISTÓRICO

- **`_archive/backup_20260608_120239/db/snapshot_baseline_v6_20260529_105928/meli_financial_v4.db`** (125.26 MB)
  - **SHA-256:** `e1e341ef44e0a61c4e846d34e05d14a4c291dcd904869f20fdf6e9a37fef1c29`
  - **CAP / Fase:** Sprint A1, B2.5C (Fase 1)
  - **Evidencia Vinculada:** `governance/INCIDENT_DB_SURVIVAL_AUDIT.md`
  - **Acción:** CONSERVAR HISTÓRICO

- **`_archive/backup_20260608_120239/db/snapshot_pre_fase2_20260603_112908/meli_financial_v4.db`** (125.01 MB)
  - **SHA-256:** `3939ad54b2442b1d7182aee856265979b6433e04842a6ff7ef7eba957b4915ea`
  - **CAP / Fase:** B2.5C (Fase 1)
  - **Evidencia Vinculada:** `evidence/fase_1b/post_classification_evidence.json`
  - **Acción:** CONSERVAR HISTÓRICO

- **`_archive/backup_20260608_120239/db/snapshot_pre_ripley_rebuild_20260601_172024/meli_financial_v4.db`** (125.26 MB)
  - **SHA-256:** `c341b272da889474d4d9d80586efbe887c5ef0547462bf26d87c01829748518a`
  - **CAP / Fase:** Sprint B2.5C (Fase 1)
  - **Evidencia Vinculada:** `governance/RIPLEY_POST_CLASSIFICATION_CERTIFICATION.md`
  - **Acción:** CONSERVAR HISTÓRICO

- **`_archive/backup_20260608_120239/db/snapshot_pre_ripley_rebuild_20260601_172043/meli_financial_v4.db`** (125.26 MB)
  - **SHA-256:** `88082bbc073af49aab625b859d986f8d2f3eb7f8482ce3b2ce198b8e29a7a3bb`
  - **CAP / Fase:** Sprint B2.5C (Fase 1)
  - **Evidencia Vinculada:** `governance/RIPLEY_POST_CLASSIFICATION_CERTIFICATION.md`
  - **Acción:** CONSERVAR HISTÓRICO

---

## 4. LISTADO DE CANDIDATOS A ARCHIVADO (SANEAMIENTO SEGURO)

Los siguientes snapshots y duplicados **NO participan en certificaciones activas** y pueden archivarse fuera del repositorio de desarrollo sin afectar la reproducibilidad:

- **`KnowledgeBase_baseline_v4.zip`** (0.02 MB) — Hash: `280189e18cb2` — Motivo: NO DUPLICADO
- **`.agents/gstack/browse/src/snapshot.ts`** (0.03 MB) — Hash: `3ec6cee340e8` — Motivo: NO DUPLICADO
- **`.agents/gstack/browse/test/snapshot.test.ts`** (0.02 MB) — Hash: `bb4002cc3604` — Motivo: NO DUPLICADO
- **`.agents/gstack/browse/test/fixtures/snapshot.html`** (0.0 MB) — Hash: `8d656df55291` — Motivo: NO DUPLICADO
- **`.agents/gstack/scripts/capture-baseline.ts`** (0.0 MB) — Hash: `02a23eda95b6` — Motivo: NO DUPLICADO
- **`.agents/skills/gstack-browse/src/snapshot.ts`** (0.03 MB) — Hash: `3ec6cee340e8` — Motivo: DUPLICADO EXACTO
- **`.agents/skills/gstack-browse/test/snapshot.test.ts`** (0.02 MB) — Hash: `bb4002cc3604` — Motivo: DUPLICADO EXACTO
- **`.agents/skills/gstack-browse/test/fixtures/snapshot.html`** (0.0 MB) — Hash: `8d656df55291` — Motivo: DUPLICADO EXACTO
- **`.claude/memory.db`** (0.17 MB) — Hash: `50a988fc7bac` — Motivo: NO DUPLICADO
- **`.git/logs/refs/heads/integration/baseline-v8`** (0.0 MB) — Hash: `c0fbcfcc47bf` — Motivo: NO DUPLICADO
- **`.git/refs/heads/integration/baseline-v8`** (0.0 MB) — Hash: `25ecd50a5b2c` — Motivo: NO DUPLICADO
- **`.git/refs/tags/baseline-v8-certified`** (0.0 MB) — Hash: `f7d34619da91` — Motivo: NO DUPLICADO
- **`.git/refs/tags/BASELINE_V6`** (0.0 MB) — Hash: `7470b54e4240` — Motivo: NO DUPLICADO
- **`.git/refs/tags/CERTIFIED_BASELINE_V1`** (0.0 MB) — Hash: `bcdd739ca957` — Motivo: NO DUPLICADO
- **`.git/refs/tags/MARKETPLACE_AUDITOR_V3_5_STABLE_BASELINE`** (0.0 MB) — Hash: `4e14d08f6529` — Motivo: NO DUPLICADO
- **`.git/refs/tags/PLATFORM_BASELINE_V4`** (0.0 MB) — Hash: `0d95c8ef5acd` — Motivo: NO DUPLICADO
- **`.git/worktrees/marketplace-financial-baseline-v8-d15e94e/commondir`** (0.0 MB) — Hash: `340ddcb67a62` — Motivo: NO DUPLICADO
- **`.git/worktrees/marketplace-financial-baseline-v8-d15e94e/gitdir`** (0.0 MB) — Hash: `735b3b181a1a` — Motivo: NO DUPLICADO
- **`.git/worktrees/marketplace-financial-baseline-v8-d15e94e/HEAD`** (0.0 MB) — Hash: `3ea05c774ba6` — Motivo: NO DUPLICADO
- **`.git/worktrees/marketplace-financial-baseline-v8-d15e94e/index`** (0.22 MB) — Hash: `847c0100be98` — Motivo: NO DUPLICADO

---

# VEREDICTO DE GOBERNANZA

```text
AUDITORÍA DE GOBERNANZA: COMPLETADA
MODIFICACIÓN DE ARCHIVOS: NO (0 alterados)
COMPRESIÓN DE DATOS: NO (0 comprimidos)
ELIMINACIÓN DE DATOS: NO (0 eliminados)
BASE OFICIAL INTACTA: SÍ (SHA-256 311c78e2b7471b3e227df68d17115f7147d9315fec0c3d6d9cace9ff73defdb9)

SIGUIENTE PASO AUTORIZADO:
Creación de SNAPSHOTS_RETENTION_POLICY_V1.md para definir formalmente las reglas de retención y archivado.
```