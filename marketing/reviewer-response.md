# Respuesta a la primera revisión técnica externa

> Fecha de la review: 30 de mayo de 2026 (Fase 0)
> Fecha de respuesta y acciones tomadas: mismo día.

Esta es la respuesta pública del proyecto a la primera revisión técnica externa recibida sobre el repo de QRB en Fase 0. La revisión original fue dura, honesta y mayoritariamente acertada. Se incorporan aquí los cambios ya aplicados, las discrepancias respetuosas, y una invitación a continuar el diálogo.

---

## A quien envió la review

Gracias. La honestidad técnica vale más que diez halagos. Has sido decisivo y casi todos los puntos los he incorporado de inmediato. Te detallo el antes/después por si quieres auditar:

### Aceptado y corregido

**1. "El código no implementa L2"** — Razón total. El README arrancaba diciendo *"QRB is the first Layer 2 blockchain on Ethereum"* cuando el código es una blockchain local de un solo nodo. Reescrito a *"research and prototype track for a post-quantum L2 on Ethereum-compatible infrastructure"*, y añadida una sección **Status** con tabla por componente que separa **Implementado / Diseñado / Research / Phase 3+ vision**.

**2. "La comparativa 'QRB es el único proyecto…' es marketing antes que evidencia"** — Cierto. La tabla mantiene las cinco columnas pero ahora cada celda de QRB lleva la fase correspondiente (Fase 0 / 1 / 3+), y el párrafo introductorio aclara explícitamente que la tabla representa la **combinación objetivo a lo largo del roadmap completo**, no paridad de capacidades hoy.

**3. "Bug en `block.py.sign_with`: no valida que `proposer_pubkey` corresponda a `proposer_address`"** — Fallo real, ya corregido. Cambios:

- Comprobación añadida en `sign_with`: lanza `ValueError` si la pubkey no corresponde a la `proposer_address` declarada.
- Comprobación equivalente añadida en `is_valid`, antes de la verificación de firma.
- Nuevo test de regresión `test_block_proposer_pubkey_must_match_address` que cubre los dos vectores: rechazo en firma y rechazo en validación con firma criptográficamente válida pero pubkey ajena.

El test menciona la revisión externa de 30/05/2026 en su docstring.

**4. "No hay CI verificable; el badge de 'tests pass' debería ser real"** — Solucionado. Añadido GitHub Actions con matriz Python 3.10 / 3.11 / 3.12 ejecutando los 6 tests end-to-end en cada `push` y `pull_request` a `main`. Badge real añadido al inicio del README. Workflow: `.github/workflows/ci.yml`.

**5. "Falta separar claramente implementado / diseñado / research / visión"** — Hecho a fondo:

- Sección **Status** del README con tabla por componente y enlace al fichero o sección de whitepaper correspondiente.
- Cada celda de la tabla comparativa lleva su fase.
- Mensaje explícito en el README: *"The Phase 0 prototype does not yet implement L2 mechanics, EVM, networking, or decentralised consensus. Those are explicit Phase 1 and Phase 2 deliverables."*

### Aceptado parcialmente

**6. "Encoding / mojibake en algunos archivos"** — Comprobado con `grep -rn "Ã\|â€"` sobre todo el repo: no aparecen patrones de mojibake. Los archivos están en UTF-8 limpio. Sospecho que el mojibake que viste se debió a tu terminal o editor interpretando UTF-8 como CP-1252 (típico de `cmd.exe` en Windows-ES). Si no es ese el caso y observas mojibake real en algún archivo concreto, te agradecería que pasaras la ruta exacta para verificarlo.

**7. "Claims agresivos que necesitan citas precisas o suavizado"** — Añadidas referencias inline en el README (CoinDesk para el Q-Day Prize, mención explícita al paper de Google de abril 2026 y al estudio Caltech+Atomic). El whitepaper ya traía bibliografía formal (FIPS 203-206, MiCA, NIS2, BB84, Shor). En el README las citas son enlaces activos para facilitar verificación al lector. Añadida también la línea: *"Estimates remain estimates — the year of arrival of a CRQC is genuinely uncertain. But the direction is unambiguous."*

### Aceptado como dirección futura

**8. "Construir una PoC más cerca de Ethereum: smart account PQ, verificador ML-DSA, integración mínima con OP Stack o Reth"** — De acuerdo, es exactamente el alcance de Fase 1. El whitepaper lo detalla en §3.3 (Account Abstraction PQ) y §3.5 (bridge sobre OP Stack). Plan operativo: aplicar a NLNet con presupuesto para 6 meses dedicados a:

- Smart account contract en Solidity con verificador ML-DSA-65 como precompilado.
- Devnet sobre fork de Reth con MLDSAVERIFY en lugar de ECRECOVER.
- Bridge mínimo bidireccional con Ethereum sepolia.

Si tienes disposición a revisar la application a NLNet antes de enviarla, sería un input significativo.

### Donde respetuosamente discrepo (con matiz)

**9. "3/10 como infraestructura blockchain real"** — Acepto la nota tal cual. Solo añado contexto: en Fase 0, con fundador único y presupuesto autofinanciado, el objetivo declarado **no es entregar infraestructura blockchain real**, es producir los artefactos (whitepaper defendible + prototipo demostrable + repo limpio con CI) que permiten acceder a los grants y al equipo que construirá la infraestructura real en Fase 1+. La nota que diste como narrativa para grants (7/10) es la que mide el progreso contra el objetivo declarado de esta fase. La nota de infraestructura corresponde a Fase 2, no a la actual.

Es una distinción de scope, no un desacuerdo sobre la observación técnica. La crítica subyacente sigue siendo válida y dirigió todos los cambios anteriores.

---

## Una pregunta directa

¿Estarías dispuesto a hacer una segunda revisión técnica una vez aplicados los cambios? Tu feedback aplicado y publicado tendría más peso para la application a NLNet que cualquier endorsement genérico. Y si te interesa involucrarte en el proyecto en algún rol (advisor, technical reviewer remunerado en Fase 1, dev de capa EVM-PQ), la conversación está abierta.

---

## Cierre

Gracias por la revisión. Las correcciones están aplicadas y verificables en los commits del repo. Si encuentras tiempo para una segunda lectura técnica, sería bienvenida.

— Fiyiware
QRB Project
[https://github.com/Fiyiware/quantum-resistance-blockchain](https://github.com/Fiyiware/quantum-resistance-blockchain)
[@QRB_PQ](https://x.com/QRB_PQ)
