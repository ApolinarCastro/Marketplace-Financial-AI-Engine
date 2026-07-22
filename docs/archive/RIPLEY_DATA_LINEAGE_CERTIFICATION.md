# Ripley Data Lineage Certification

## Hallazgo Principal
Existen múltiples filas en el Ledger de Ripley por cada `order_id` debido a la naturaleza fragmentada de los datos enviados por Ripley.

## Causa Raíz
El cargador `surgical_loader.py` lee correctamente las distintas tablas que entrega Ripley (Excel base, CICLOS CSV, TH CSV, FF CSV). La duplicación en el ledger de primer nivel (`marketplace_ledger_v1`) es intencional. La inteligencia financiera recae en `engine/v4/marketplace_auditor.py`, el cual implementa reglas de negocio complejas (ADJ_01, ADJ_03) que filtran las redundancias anulando el campo `include_in_operational_pnl = False`.

## Plan de Remediación
Declarar **NO ACTION REQUIRED** sobre el loader de Ripley, puesto que su comportamiento está certificado y validado por el Auditor.
