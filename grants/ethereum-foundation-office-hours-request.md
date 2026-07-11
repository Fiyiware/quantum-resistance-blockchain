# EF ESP — Office Hours request (ready to paste)

> **🛑 OUTCOME (July 2026): sent and answered — goal achieved, request closed.**
> Submitted 16 June 2026 (auto-acknowledged by the ESP team); substantive written reply
> received 22 June 2026. The answer to the call's core question ("does this duplicate an
> EF post-quantum effort?") is **yes**: precompile-based PQ signature verification +
> account-abstraction migration is the active mandate of the EF's Post-Quantum team
> ([pq.ethereum.org](https://pq.ethereum.org)). No ESP grant fit; recommended path is
> the public PQ process (roadmap/FAQ, ACD PQ breakout calls,
> [EIP-8141](https://eips.ethereum.org/EIPS/eip-8141)). Exactly the steer this request
> was designed to get **before** investing in the Reth fork — it worked. Follow-up plan:
> `docs/pivote-pq-publico-julio-2026.md`.

> **What this is**: text for the EF ESP **Office Hours** request form
> (https://esp.ethereum.foundation → Office Hours). Office Hours is a short, informal
> 20-minute call for **non-financial guidance** — *not* a funding application and *not* a
> pitch. So this message asks for **alignment guidance**, not money.
>
> **Hard rules from EF's own page (do not break):**
> - Do **not** ask for financial support or pitch for funding here.
> - Do **not** mention tokens at all (EF explicitly does not engage with token topics;
>   QRB has no token anyway — keep it out entirely).
> - Do **not** ask for wallet/transaction/exchange help.
> - **Be specific** about what you need — that is what makes the call useful.
>
> **Goal of the call**: get a steer on whether QRB's post-quantum work fits a current
> Wishlist/RFP item (and which), and avoid duplicating any EF post-quantum effort —
> *before* investing in the Reth fork.

---

## Message (paste into the "what do you need / context" field)

**Context — what I'm working on**

QRB is an open-source project (MIT/Apache-2.0) building post-quantum cryptographic
building blocks for Ethereum. I have a working proof of concept: an `MLDSAVERIFY` EVM
precompile that verifies NIST FIPS 204 ML-DSA-65 signatures, wrapped as a `revm`
precompile and exercised **end-to-end** — a real transaction that calls the precompile
runs through a full `revm` EVM and returns the expected result. My next step is a
post-quantum ERC-4337 smart account that uses it, built in a Reth fork, with a published
gas-cost model. The intent is to upstream the precompile (EIP + Reth PR) as a public good,
not to keep it siloed. Repo: https://github.com/Fiyiware/quantum-resistance-blockchain

**What I'd like guidance on**

1. **Alignment** — does this kind of work (an upstreamable ML-DSA precompile + a PQ
   account-abstraction account) fit a current Wishlist or RFP item? If so, which one
   should I aim at?
2. **Avoiding duplication** — are there EF teams or projects already working on
   post-quantum signature verification in the EVM or clients that I should coordinate
   with rather than duplicate?
3. **Approach** — is forking Reth and proposing the precompile as an EIP the right venue,
   or would you suggest a different path?

I'm a solo founder at the proof-of-concept stage, and before I scale the work up I mainly
want to make sure I'm pointing my effort where it's genuinely useful to Ethereum.

---

## Versión en español (SOLO para que la entiendas — en el formulario va el inglés de arriba)

> ⚠️ Esto es una traducción para tu comprensión. **No pegues esto en el formulario**;
> pega el texto en inglés de la sección anterior.

**Contexto — en qué estoy trabajando**

QRB es un proyecto open-source (licencias MIT/Apache-2.0) que construye piezas
criptográficas post-cuánticas para Ethereum. Tengo una prueba de concepto que funciona:
un precompile de la EVM, `MLDSAVERIFY`, que verifica firmas ML-DSA-65 (el estándar NIST
FIPS 204), envuelto como un precompile de `revm` y probado **de principio a fin** — una
transacción real que llama al precompile se ejecuta a través de un EVM `revm` completo y
devuelve el resultado esperado. Mi siguiente paso es una cuenta inteligente post-cuántica
tipo ERC-4337 que lo use, construida en un fork de Reth, con un modelo de coste de gas
publicado. La intención es subir el precompile aguas arriba (como un EIP y un PR a Reth)
como bien público, no mantenerlo aislado. Repositorio:
https://github.com/Fiyiware/quantum-resistance-blockchain

**Sobre qué me gustaría orientación**

1. **Encaje** — ¿este tipo de trabajo (un precompile de ML-DSA reutilizable + una cuenta
   de account abstraction post-cuántica) encaja en algún ítem actual de vuestro Wishlist
   o RFP? Si es así, ¿en cuál debería centrarme?
2. **No duplicar** — ¿hay equipos o proyectos en la EF que ya estén trabajando en
   verificación de firmas post-cuánticas dentro de la EVM o de los clientes, con los que
   debería coordinarme en lugar de duplicar?
3. **Enfoque** — ¿forkear Reth y proponer el precompile como un EIP es la vía adecuada, o
   sugeriríais un camino distinto?

Soy fundador en solitario, en fase de prueba de concepto, y antes de escalar el trabajo
quiero sobre todo asegurarme de dirigir mi esfuerzo a donde sea de verdad útil para
Ethereum.

---

## After the call (internal notes — fill in)

- Which Wishlist/RFP item they pointed to (name + URL): …
- EF teams / projects to coordinate with: …
- Their view on the Reth-fork + EIP approach: …
- Recommended next step (apply to item X / Academic Grants / other): …
