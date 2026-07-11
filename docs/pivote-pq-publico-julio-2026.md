# Pivote de julio de 2026 — del "L2 PQ propio" al proceso post-cuántico público de Ethereum

> **Qué es este documento**: el plan vigente del proyecto tras la respuesta de la
> Ethereum Foundation del 22 de junio de 2026. Sustituye a
> `marketing/plan-fase0-junio-agosto.md`. Idioma: español (documento de trabajo del
> fundador; los artefactos públicos siguen en inglés).

---

## 1. Qué ha pasado

- **16 jun 2026** — Se envió la solicitud de Office Hours al ESP de la Ethereum
  Foundation (según el plan). Acuse de recibo automático.
- **22 jun 2026** — Respuesta sustantiva de la EF: la ingeniería es interesante y el
  framing correcto, **pero no es un hueco abierto**. La verificación de firmas PQ en la
  capa de ejecución vía precompile, con migración por account abstraction, es el mandato
  activo del equipo **Post-Quantum** del cluster de Protocolo de la EF. No hay encaje de
  grant ESP y la EF no puede dar el acompañamiento de dirección que pedíamos.
- **Verificado de forma independiente (jul 2026)**: [pq.ethereum.org](https://pq.ethereum.org)
  existe con roadmap vivo (precompiles de verificación PQ, migración gradual opt-in vía
  AA, hitos de fork hasta ~2029, premios de investigación), y
  [EIP-8141](https://eips.ethereum.org/EIPS/eip-8141) (account abstraction nativa) es la
  vía de migración prevista, considerada para el fork Hegotá.

**Consecuencia honesta**: la premisa central del whitepaper §1.4 ("las L1 no pueden
migrar a tiempo → hace falta una cadena PQ-nativa") ha quedado superada. Construir una
L2 PQ competidora ya no tiene sentido. Descubrirlo en Fase 0, antes de aceptar dinero de
nadie, es exactamente para lo que se diseñó la Fase 0.

## 2. La decisión

1. **QRB no construirá una L2 post-cuántica competidora.**
2. **Los artefactos de Fase 0 se redirigen al proceso PQ público de Ethereum**: los PoC
   de verificación ML-DSA (`poc/`), el trabajo de benchmarks/vectores KAT y el diseño de
   smart account PQ encajan directamente en el roadmap de precompiles + AA del equipo PQ.
3. **La línea de investigación propia que se conserva es la Amenaza B**: confidencialidad
   post-cuántica (privacidad sobre STARKs con view keys, whitepaper §7.5). El programa de
   la EF cubre autenticación, no privacidad — ese hueco sigue abierto.
4. **Toda solicitud de financiación queda en pausa** hasta completar el reposicionamiento
   (notas de estado en `grants/`). Sin token, como siempre: eso no cambia.

## 3. Plan de acción (en orden)

### Paso 1 — Responder a la EF (esta semana)
Correo corto de agradecimiento confirmando que seguiremos la vía pública que indicaron.
Mantiene viva la relación con alguien de la EF que ya revisó el PoC.

### Paso 2 — Entrar al proceso público (semanas 1-2)
- Leer a fondo [pq.ethereum.org](https://pq.ethereum.org): roadmap, FAQ y "how to get
  involved". Identificar el workstream de estandarización del precompile de verificación.
- Localizar las **All Core Devs Post-Quantum breakout calls** (coordinadas por Antonio
  Sanso): agendas y enlaces en el repo `ethereum/pm` de GitHub y el Discord de Eth R&D.
  Asistir primero como oyente; presentarse con enlace al repo cuando haya oportunidad.
- Leer [EIP-8141](https://eips.ethereum.org/EIPS/eip-8141) y su hilo de discusión en
  Ethereum Magicians — el diseño de smart account PQ de QRB debe mapearse a este EIP.

### Paso 3 — Primera contribución concreta (semanas 2-6)
Convertir los issues abiertos en contribuciones útiles para el proceso público, no solo
para QRB:
- **#28** (benchmark con `criterion` del PoC ML-DSA) → alimenta el modelo de gas que el
  equipo PQ necesitará para el precompile.
- **#32** (vectores KAT del NIST en Python y Rust) → suite de interoperabilidad
  reutilizable por cualquier cliente.
- Revisar los **premios de investigación** publicados en pq.ethereum.org y evaluar si
  alguno encaja con lo que ya sabemos hacer.

### Paso 4 — Reposicionar los artefactos públicos (semanas 2-4)
- README: hecho (sección "Strategic update — July 2026").
- Whitepaper: nota de estado añadida; la v0.3 reescribirá §1.4, §2 y el roadmap alrededor
  de (a) contribución al proceso público y (b) la línea de confidencialidad PQ.
- Issues del repo: reetiquetar #27/#28/#31/#32 para reflejar el nuevo marco.

### Paso 5 — Financiación, solo cuando el reposicionamiento esté hecho
- **Premios de investigación del programa PQ de la EF**: la vía más directa y sin fricción.
- **NLnet Open Call (cuando reabra, después del verano)**: solo con el nuevo marco —
  tooling abierto para la migración PQ pública y/o la investigación de confidencialidad.
  Nunca el borrador antiguo tal cual.
- **Academic Grants de la EF**: posible encaje para la línea de confidencialidad (Fase 3)
  si se consigue el colaborador criptógrafo (#27).

## 4. Qué NO cambia

- Código abierto MIT/Apache-2.0, disclosure de asistencia de IA, disciplina
  implementado/diseñado/visión.
- Sin token. Ni ahora ni como condición de nada de lo anterior.
- El repositorio sigue siendo el portfolio verificable del trabajo.
