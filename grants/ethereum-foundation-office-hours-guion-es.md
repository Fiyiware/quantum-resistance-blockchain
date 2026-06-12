# Office Hours con Ethereum Foundation — guion para la llamada (en español)

> Para Luiggi. Esto es tu chuleta para la videollamada de 20 minutos con el equipo ESP.
> Tenlo abierto durante la llamada. La llamada será probablemente **en inglés** — al final
> de cada respuesta tienes la frase clave en inglés lista para leer.

---

## 1. Recuerda qué es esto (y qué NO es)

- **SÍ es:** una charla informal de 20 min para que te **orienten**.
- **NO es:** pedir dinero, ni un pitch para vender el proyecto.
- **3 reglas que NO puedes romper:**
  1. No pidas financiación en esta llamada (eso va después, en una solicitud aparte).
  2. **No menciones tokens** para nada (ellos no tratan ese tema; además QRB no tiene).
  3. No pidas ayuda con wallets/exchanges/transacciones.

Si te preguntan "¿buscas financiación?", la respuesta honesta y correcta es:
*"Sí, más adelante quiero presentar una solicitud a un ítem de vuestro Wishlist o RFP;
justo por eso pido esta llamada, para asegurarme de a cuál apuntar antes de invertir más
trabajo."*
> EN: *"Yes, eventually I'd like to apply to a Wishlist or RFP item — that's exactly why
> I'm here: to make sure I aim at the right one before investing more work."*

---

## 2. Qué quiero conseguir de la llamada (mi objetivo)

Salir con **tres cosas claras**:
1. **A qué ítem de Wishlist/RFP apuntar** (o si conviene mejor un Academic Grant).
2. **Si alguien en la EF ya está haciendo esto** (para no duplicar y, mejor aún, coordinarme).
3. **Si mi plan técnico es el correcto** (fork de Reth + proponer el precompile como EIP).

Si consigo respuesta a estas tres, la llamada ha sido un éxito.

---

## 3. Cómo abrir (30 segundos, lo primero que dices)

> "Hola, gracias por el tiempo. Soy fundador en solitario de un proyecto open-source
> llamado QRB. Estoy construyendo piezas criptográficas post-cuánticas para Ethereum.
> Ya tengo un prototipo que funciona y mi duda principal es dónde encaja mejor dentro de
> vuestro Wishlist o RFP antes de invertir más. ¿Os va si os doy contexto rápido y luego
> os hago tres preguntas concretas?"

> EN: *"Hi, thanks for the time. I'm a solo founder of an open-source project called QRB,
> building post-quantum cryptographic building blocks for Ethereum. I already have a
> working prototype, and my main question is where it best fits within your Wishlist or
> RFP before I invest more. Can I give you quick context and then ask three specific
> questions?"*

---

## 4. Las 3 preguntas que vas a hacer (el corazón de la llamada)

1. **Encaje:** ¿este tipo de trabajo — un precompile de ML-DSA reutilizable + una cuenta
   de account abstraction post-cuántica — encaja en algún ítem actual de vuestro Wishlist
   o RFP? ¿En cuál debería centrarme?
2. **No duplicar:** ¿hay equipos o proyectos en la EF que ya estén trabajando en
   verificación de firmas post-cuánticas dentro de la EVM o de los clientes, con los que
   debería coordinarme en lugar de duplicar?
3. **Enfoque:** ¿forkear Reth y proponer el precompile como un EIP es el camino adecuado,
   o sugeriríais otra vía?

---

## 5. Guion de respuestas a SUS posibles preguntas

Aquí van las preguntas que probablemente te hagan, con tu respuesta ya redactada en
lenguaje sencillo. Habla con naturalidad, no hace falta leerlo clavado.

**"¿Qué es QRB / qué estás construyendo?"**
> Una cadena/capa pensada desde cero para resistir a ordenadores cuánticos. Lo concreto
> que ya funciona es un "precompile" para la EVM que verifica firmas post-cuánticas
> (ML-DSA-65, el estándar de NIST). La idea es que sirva no solo a mi proyecto, sino a
> Ethereum entero.
> EN: *"A chain/layer designed from the ground up to resist quantum computers. The
> concrete piece that already works is an EVM precompile that verifies post-quantum
> signatures (ML-DSA-65, the NIST standard). The goal is for it to serve not just my
> project but Ethereum as a whole."*

**"¿En qué punto estás? ¿Qué tienes hecho?"**
> Fase de prueba de concepto, pero funcionando de verdad: tengo el precompile metido
> dentro de un EVM real (revm) y una transacción que lo llama de principio a fin y
> devuelve el resultado correcto. No es una idea en papel, es código que corre, con tests
> y CI público.
> EN: *"Proof-of-concept stage, but genuinely working: the precompile runs inside a real
> EVM (revm), and a transaction calls it end-to-end and returns the correct result. It's
> not a paper idea — it's running code, with tests and public CI."*

**"¿Quién está detrás? ¿Equipo?"**
> Ahora mismo soy yo solo, fundador. He construido el prototipo con bastante ayuda de IA,
> y lo digo abiertamente en el repo. El siguiente paso es incorporar a un ingeniero de
> Rust/Reth y a un criptógrafo.
> EN: *"Right now it's just me, the founder. I built the prototype with substantial AI
> assistance, which I disclose openly in the repo. The next step is bringing on a
> Rust/Reth engineer and a cryptographer."*
> (Honestidad = punto a favor. No lo escondas.)

**"¿Por qué Ethereum y no tu propia cadena?"**
> Porque la pieza que construyo le sirve a Ethereum directamente. Mi intención es subirla
> "aguas arriba": proponer el precompile como un EIP y abrir un PR contra Reth. Aunque mi
> capa nunca llegue a mainnet, un precompile de ML-DSA probado y medido es una
> contribución útil para todo el ecosistema.
> EN: *"Because the piece I'm building serves Ethereum directly. My intent is to upstream
> it: propose the precompile as an EIP and open a PR against Reth. Even if my own layer
> never reaches mainnet, a tested, benchmarked ML-DSA precompile is a useful contribution
> for the whole ecosystem."*

**"¿En qué te diferencias de QRL/Zond, Quranium, etc.?"**
> Esos hacen firmas post-cuánticas pero con poco soporte de EVM y account abstraction.
> Los proyectos de privacidad (Aleo, Aztec) usan pruebas que NO son post-cuánticas. Yo
> intento cubrir las dos amenazas a la vez y, sobre todo, con herramientas nativas de
> Ethereum.
> EN: *"They do post-quantum signatures but with weak EVM/account-abstraction support.
> Privacy projects (Aleo, Aztec) use proofs that are not post-quantum. I try to cover
> both threats at once, and crucially with Ethereum-native tooling."*

**"¿Qué necesitas exactamente de nosotros?"**
> Sobre todo orientación: saber a qué ítem de vuestro Wishlist/RFP apuntar, con quién
> coordinarme para no duplicar, y si mi enfoque técnico (fork de Reth + EIP) es el
> adecuado.
> EN: *"Mainly guidance: which Wishlist/RFP item to aim at, who to coordinate with to
> avoid duplication, and whether my technical approach (Reth fork + EIP) is the right
> one."*

**"¿Cuál es tu plan / roadmap?"**
> A 6 meses: llevar el precompile a un fork de Reth con un modelo de coste de gas, una
> cuenta inteligente post-cuántica tipo ERC-4337, una devnet pública y un SDK con una
> wallet de referencia. Más adelante, investigar privacidad post-cuántica con STARKs.
> EN: *"Six months: bring the precompile into a Reth fork with a gas-cost model, a
> post-quantum ERC-4337 smart account, a public devnet, and an SDK with a reference
> wallet. Later, research post-quantum privacy using STARKs."*

**"¿Cómo te financias ahora?"**
> De momento es trabajo propio, sin financiación. Por eso exploro vías como la vuestra,
> de forma ordenada.
> EN: *"For now it's my own work, unfunded. That's why I'm exploring routes like yours, in
> an orderly way."*

---

## 6. Si no sabes responder algo

No pasa nada. Di la verdad:
> "Buena pregunta, eso aún lo estoy definiendo — de hecho es parte de por qué quería
> hablar con vosotros."
> EN: *"Good question — I'm still working that out, which is part of why I wanted to talk
> to you."*

Es una llamada de orientación: **no se espera que lo tengas todo resuelto.** Mostrar que
sabes lo que NO sabes es buena señal.

---

## 7. Antes de colgar

Pregunta siempre:
> "¿Cuál creéis que debería ser mi siguiente paso concreto?"
> EN: *"What do you think my concrete next step should be?"*

Y apunta lo que te digan (rellena las notas en
`ethereum-foundation-office-hours-request.md`).

---

## 8. Checklist rápido para el día

- [ ] Repo abierto en una pestaña por si quieren verlo: github.com/Fiyiware/quantum-resistance-blockchain
- [ ] Esta chuleta abierta.
- [ ] Cámara y micro probados, sitio tranquilo.
- [ ] Mentalidad: vienes a aprender y a pedir orientación, no a vender. Relájate.
