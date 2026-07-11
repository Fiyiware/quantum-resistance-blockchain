# Plan de Fase 0 — junio en adelante (foco Ethereum Foundation)

> **🛑 SUPERADO (julio de 2026).** El primer paso de este plan (Office Hours de la EF) se
> ejecutó y obtuvo respuesta el 22 de junio: **no hay encaje de grant ESP** porque el
> trabajo de precompiles PQ + migración por account abstraction es el mandato activo del
> equipo Post-Quantum de la propia EF. El plan vigente es
> [`docs/pivote-pq-publico-julio-2026.md`](../docs/pivote-pq-publico-julio-2026.md).
> Este documento se conserva como registro histórico.

Hoja de ruta práctica desde mediados de junio de 2026. **Cambio de plan respecto a la
versión anterior:** el NGI Zero Commons Fund de NLnet **cerró** (junio 2026) y su Open
Call genérica no reabre hasta **después del verano de 2026**. La vía principal pasa a ser
la **Ethereum Foundation (ESP)**, que es mejor encaje temático y **no tiene fecha límite
fija** (es de convocatoria continua, vía Wishlist/RFP + Office Hours). NLnet queda como
**plan B** para después del verano.

## Principio rector

**Conseguir financiación no dilutiva para la Fase 1 es la prioridad #1.** Es lo que
desbloquea el trabajo pagado. No depende de seguidores ni de impresiones en X — se evalúa
por el whitepaper, el repositorio y la propuesta. Las redes son un canal secundario: 
construyen comunidad y atraen colaboradores, pero no son la puerta del dinero.

**El primer paso concreto, ahora mismo, es enviar la solicitud de Office Hours de la EF**
(ya está todo preparado en `grants/`). Es orientación, no dinero: sirve para saber a qué
ítem de Wishlist/RFP apuntar antes de invertir más.

## Qué es "éxito" en Fase 0 (expectativas realistas)

No es viralidad. Es:

- ✅ **Solicitud de Office Hours de la EF enviada** y, idealmente, llamada realizada.
- ✅ Saber **a qué ítem de Wishlist/RFP** apuntar (o si conviene Academic Grants).
- ✅ **Solicitud de grant de la EF enviada** una vez claro el encaje.
- ✅ Prototipo un poco más sólido (cerrar 1-2 `good-first-issue`; PoCs de Rust en CI ✓ hecho).
- ✅ Un puñado de personas **genuinamente interesadas** y **al menos 1 conversación seria**
  con un posible colaborador/co-fundador.

---

## Pasos (sin calendario rígido — la EF es de convocatoria continua)

### Ahora — Contacto con la EF
- **Enviar el formulario de Office Hours** con el texto preparado
  (`grants/ethereum-foundation-office-hours-formulario-respuestas.md`).
- Tener a mano el guion de la llamada (`grants/ethereum-foundation-office-hours-guion-es.md`).
- Montar una **wallet de ETH** que controles (la EF paga los grants on-chain en ETH).

### Tras la llamada — Solicitud
- Anotar a qué ítem de Wishlist/RFP te orientan.
- Adaptar la solicitud (`grants/ethereum-foundation-esp-draft.md`) a ese ítem y enviarla.

### En paralelo — Credibilidad técnica del repo
- Cerrar **1-2 `good-first-issue`**. Un repo con actividad reciente impresiona al evaluador.
- (Opcional) Generar el PDF del whitepaper en inglés desde tu PC: `cd whitepaper && node _build_pdf.js en`.
- Mantener verde la CI (ahora cubre también los PoCs de Rust).

### En paralelo — Comunidad (efecto compuesto, 15 min/día)
- **Hacker News**: un "Show HN" con el README del repo.
- **Reddit**: post en r/ethereum o r/postquantum **enmarcado como petición de feedback**.
- **Telegram / Discord**: unirse a comunidades de cripto-PQ / Ethereum, participar de verdad.
- **DMs**: 10-20 personas concretas (criptógrafos PQ, proyectos adyacentes), mensajes personalizados.

### Después del verano — Plan B
- Cuando reabra la **Open Call de NLnet**, valorar enviar también allí
  (`grants/nlnet-commons-application-draft.md` está listo para reusar).

---

## Prioridad de canales de distribución (de más fácil a más difícil)

1. **Telegram / Discord** — te unes a comunidades existentes. No necesitas seguidores.
2. **Hacker News** — meritocrático, cuenta nueva vale, público = devs.
3. **Reddit** — el más estricto; necesita karma/historial y framing de "feedback".
4. **X** — efecto compuesto a largo plazo; no esperar resultados rápidos con cuenta nueva.

## Reglas de oro

- **Autenticidad > volumen.** Nada de automatizar cuentas o spam: lleva a baneos y daña la
  credibilidad, que es tu activo principal.
- **No medir el éxito en likes.** Medirlo en: contacto con la EF, solicitud enviada, repo mejorado, conversaciones reales.
- **15 min/día de comunidad** es sostenible; 3 horas un día y nada el resto, no.
- **El grant primero.** Si una semana hay que elegir entre redes y avanzar la solicitud de la EF, gana la EF.
