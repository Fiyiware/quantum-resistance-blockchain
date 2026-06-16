# EF ESP Office Hours — respuestas del formulario (listas para pegar)

> Ficha para rellenar el formulario de **Office Hours** en https://esp.ethereum.foundation
> El formulario lo traduce el navegador al español, pero el equipo lee en **inglés**:
> los textos largos van en inglés (traducción ES debajo para que entiendas qué dices).

## Información de contacto

| Campo | Valor |
|---|---|
| **Nombre de pila** | Luiggi Leonel |
| **Apellido** | Cedeño Bermeo |
| **Correo electrónico** | El que revises a diario (recomendado: `qrb.grants@proton.me`; si no lo miras, tu Gmail) |
| **Compañía** | QRB |
| **Tipo de perfil** | Individual |
| **Información de contacto alternativa** | (vacío, o tu otro email de respaldo) |
| **País** | España |
| **Huso horario** | España peninsular → `Europe/Madrid (GMT+1)`. Canarias → Lisboa/GMT+1 (el que viene por defecto) |

## Perfil del solicitante (bio) — pegar (EN)

> Solo founder of QRB. Background in digital product and web development. I designed QRB's
> architecture and built a working post-quantum proof of concept — an ML-DSA EVM precompile
> running end-to-end inside revm, with tests and public CI. The prototype was built with
> substantial AI assistance, which I disclose openly in the repo. As the work scales I plan
> to bring on a Rust/Reth engineer and a cryptographer.

*(ES: Fundador en solitario de QRB. Experiencia en producto digital y desarrollo web. Diseñé
la arquitectura y construí una prueba de concepto post-cuántica funcionando — un precompile
de ML-DSA corriendo de principio a fin en revm, con tests y CI público. El prototipo se hizo
con ayuda sustancial de IA, declarada abiertamente en el repo. Al escalar incorporaré a un
ingeniero de Rust/Reth y a un criptógrafo.)*

## Solicitud de horario de oficina

- **Tipo de solicitud** (desplegable): **"Comentarios sobre el proyecto"** (Project feedback).
- **Nombre del proyecto:** `QRB — Quantum-Resistance Blockchain`
- **Carga de archivos:** opcional (puedes subir el whitepaper o saltarlo).
- **Enlace al repositorio:** `https://github.com/Fiyiware/quantum-resistance-blockchain`
- **Dominio** (desplegable): **"Cryptography"** (si no está: "Protocol" o "Security").

### Resumen del proyecto — pegar (EN)

> QRB is an open-source project (MIT/Apache-2.0) helping Ethereum prepare for the quantum
> era. Once a large quantum computer exists, every ECDSA key ever exposed on-chain becomes
> forgeable — a direct threat to the funds and identities of Ethereum users. Ethereum still
> lacks in-EVM tooling to verify the new NIST post-quantum signatures, and that gap is what
> we're filling. We've built a working proof of concept: an MLDSAVERIFY EVM precompile that
> verifies NIST FIPS 204 ML-DSA-65 signatures, wrapped as a revm precompile and exercised
> end-to-end (a real transaction calls it through a full revm EVM and returns the expected
> result). Next is a post-quantum ERC-4337 smart account that uses it, in a Reth fork. We
> intend to upstream the precompile to Ethereum itself — as an EIP and a Reth PR — so the
> whole ecosystem benefits, not just our project. Repo:
> https://github.com/Fiyiware/quantum-resistance-blockchain

### ¿Cómo esperas que ESP pueda ayudarte? — pegar (EN)

> Mainly guidance before I invest further: (1) Alignment — does an upstreamable ML-DSA
> precompile + a post-quantum ERC-4337 account fit a current Wishlist or RFP item, and which
> one should I aim at? (2) Avoiding duplication — are there EF teams or projects already
> working on post-quantum signature verification in the EVM or clients that I should
> coordinate with rather than duplicate? (3) Approach — is forking Reth and proposing the
> precompile as an EIP the right venue, or would you suggest a different path?

### ¿Alguna otra pregunta o comentario? (opcional) — pegar (EN)

> I'm a solo founder at proof-of-concept stage. The prototype was built with substantial AI
> assistance, disclosed openly in the repo. The project has no token and none of this work
> depends on one.

## Detalles adicionales

| Campo | Valor |
|---|---|
| **¿Has solicitado subvención en la EF antes?** | No |
| **¿Permitir que la EF te contacte sobre otras oportunidades?** | Sí |

> Al enviar: aceptas su Política de Privacidad y que las subvenciones se pagan en ETH on-chain.
