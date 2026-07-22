# GOV-R002R4 OpenCode Subordination Review

Fecha: 2026-07-15  
Responsable: Codex local  
OpenCode: NO EJECUTADO

## Objetivo

Subordinar formalmente la configuracion de OpenCode y su plugin Graphify a las instrucciones rectoras de `governance/coordination/`, sin modificar `.opencode/` ni ejecutar la neutralizacion GOV-R002R2.

## Precondicion

Antes del cambio se verifico que `opencode.json` no existia en la raiz. Resultado: PASS. No fue necesario emitir `ROOT_CONFIG_REQUIRES_REVIEW`.

## Hashes previos

| Archivo protegido | SHA-256 previo |
|---|---|
| `.opencode/opencode.json` | `0A640DDA699CFA8FFF1949131C501D9CB115CBC01E16AA983EF20D157CF09443` |
| `.opencode/plugins/graphify.js` | `F44668D0BE8ABD803A3B12CAC8857D7BD1671F5CDDD9D24ADDE519DBC673CAD1` |
| `AGENTS.md` | `AD4BA1B6BD72ED956E0A31875FFFE7E02991BD4B5F7B95DCD8CD2026A4D2053B` |
| `CLAUDE.md` | `9C04FA35F83A65CD0D0A623E848E972BDC37AC77F6152D2525B1D8B4C1D687F0` |
| `governance/coordination/FOUNDATION_RESET.md` | `94C0A60444DC326E292C0528E0851BC5C9EE19A5C8AB4F3B7DC0151CB4A7BB83` |
| `governance/coordination/COORDINATION_CONTRACT.md` | `A20250EEEA89910AEC3C253A998ED869BF663A0F8A5BC912DEEA340B285ACF54` |
| `governance/coordination/MASTER_STABILIZATION_AND_PRODUCTION_PLAN.md` | `706BFD9CE0EDC2472E381EA110B95AB4C8798AF09301B8E417D2AEB5881CA25A` |
| DB oficial | `73E3B2CE9E7B741D0A4DB8330F9ECC71087FD03320A408733ED1E06A19ECDD33` |
| `execution_board.json` | `7D4C275A1910A9D115B0B7AAB7B04A8B4ED8E742F0776B758622AA64DDB8DAC8` |

## Cambio aplicado

Se creo exclusivamente `opencode.json` en la raiz con el contenido autorizado:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "governance/coordination/FOUNDATION_RESET.md",
    "governance/coordination/COORDINATION_CONTRACT.md",
    "governance/coordination/MASTER_STABILIZATION_AND_PRODUCTION_PLAN.md"
  ]
}
```

SHA-256 resultante de `opencode.json`:

`44F4CB9079B3CC5BF5830DD7D0C21D16349A1E690650083493BA152954CBD6DA`

## Validacion estatica

| Control | Resultado |
|---|---|
| Parseo JSON | PASS |
| Schema exacto | PASS |
| Numero de instrucciones | PASS, 3 |
| Orden y rutas exactas | PASS |
| Existencia de las tres referencias | PASS |
| Instrucciones fuera de `governance/coordination/` | 0 |

La configuracion raiz obliga al ejecutor a cargar Foundation Reset, Coordination Contract y Master Stabilization and Production Plan como instrucciones del proyecto. No crea tareas, estados, handoffs, propietarios, mailbox ni memoria compartida.

## Integridad posterior

Los nueve archivos protegidos conservaron exactamente los mismos SHA-256 registrados antes del cambio. En particular:

- `.opencode/opencode.json` y `.opencode/plugins/graphify.js`: sin cambios.
- `AGENTS.md` y `CLAUDE.md`: sin cambios.
- Documentos rectores: sin cambios.
- DB oficial y `execution_board.json`: sin cambios.
- `engine/rc1/`, `engine/v4/`, Claude Flow, registry y state: no modificados.

## Limites de evidencia

La validacion es estatica. OpenCode no fue iniciado ni se ejecuto ninguna tarea o plugin para comprobar la carga runtime de las instrucciones. Esa ejecucion estaba prohibida por la directiva.

No se actualizo el baseline y no se aplico la neutralizacion GOV-R002R2.

## Archivos creados

1. `opencode.json`
2. `governance/coordination/reviews/GOV-R002R4_OPENCODE_SUBORDINATION_REVIEW.md`

## Veredicto

APPLIED_AND_STATICALLY_VERIFIED
