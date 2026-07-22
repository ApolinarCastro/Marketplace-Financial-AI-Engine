# Marketplace Lock Policy

## Estados del Marketplace
Un marketplace en la plataforma transita por los siguientes estados:

1. **DRAFT**: En desarrollo y descubrimiento.
2. **CERTIFIED**: Validaciones técnicas iniciales aprobadas, con flujos funcionales.
3. **PRE_LOCK**: Validaciones preliminares financieras y de UI completas, a la espera de validación visual y ejecutiva final.
4. **LOCKED**: Certificación total y congelamiento de cambios.

## Reglas para el estado PRE_LOCK
Un marketplace pasa a PRE_LOCK cuando cumple:
* Delta financiero preliminar = 0
* UI = API = SQL en pruebas
* Cobertura documental certificada a nivel técnico
* Alertas justificadas

## Reglas para el estado LOCKED
Un marketplace pasa a LOCKED cuando cumple:
* Delta financiero = 0
* UI = API = SQL en validación final y productiva
* Cobertura documental certificada y formal
* Alertas justificadas
* Certificación ejecutiva emitida

## Marketplaces Actuales en PRE_LOCK
* **Mercado Libre (ML)** -> PRE_LOCK
* **PARIS** -> PRE_LOCK

## Reglas de Modificación (Para estados LOCKED / PRE_LOCK)
Queda estrictamente prohibido modificar:
* ETL
* Taxonomía
* Matching
* API
* Frontend

**Excepciones permitidas solo si se cumple la triada:**
1. RFC aprobado.
2. Evidencia certificada.
3. Regression certification aprobada.
