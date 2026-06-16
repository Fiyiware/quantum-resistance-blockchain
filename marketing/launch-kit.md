# QRB — Kit de lanzamiento público

Materiales listos para usar en el lanzamiento público de QRB (mayo-junio 2026).

---

## 1. Configuración de la cuenta de X (Twitter)

### Handle (por orden de preferencia, comprueba disponibilidad)

1. `@QRB_chain`
2. `@QuantumResistant`
3. `@QRBprotocol`
4. `@QRB_PQ`
5. `@qrbchain`

### Nombre mostrado

`QRB — Quantum-Resistance Blockchain`

### Bio (280 caracteres máx)

> L2 post-cuántica sobre Ethereum. Firmas Dilithium + privacidad real con STARKs. Open source. Fase 0 activa. Whitepaper y prototipo en GitHub. Por la cripto que sobreviva al ordenador cuántico. 🛡️🔐

### Foto de perfil

Mientras no tengas logo definitivo, sirve un cuadrado de fondo azul oscuro (`#0b3d91`, el mismo del whitepaper) con las letras **QRB** centradas en blanco, fuente sans bold. Cualquier herramienta gratuita (Canva, Figma, GIMP) lo hace en 5 minutos.

### Cabecera (1500×500 px)

Un fondo gradient azul oscuro → negro con la frase de Brassard en blanco:

> *"Todo el internet de los últimos 40 años será un libro abierto."*

— Gilles Brassard, ACM A.M. Turing Award 2025

### Sitios webs a vincular

- Si tienes dominio (recomendado, 30-50 €/año): `qrb.io`, `qrb.chain`, `qrb-protocol.com`, `quantum-resistant.io`.
- Mientras tanto: la URL del repo de GitHub.

---

## 2. El hilo de lanzamiento

> ⚠️ **La versión definitiva y corregida del hilo está en [`x-thread-ready.md`](x-thread-ready.md).**
> Copia SIEMPRE de ahí. El texto de abajo se mantiene solo como referencia histórica
> y NO incluye las correcciones de los tuits 1, 5 y 7.



**1/10**

En abril de 2026, un investigador rompió la primera clave criptográfica con un ordenador cuántico de acceso público.

Google adelanta su migración post-cuántica a 2029.

Vitalik: *"cripto tiene hasta 2028 para evitar el colapso cuántico."*

El mayor robo de la historia ha empezado.

🧵

---

**2/10**

Te presento **QRB** — Quantum-Resistance Blockchain.

La primera L2 sobre Ethereum diseñada desde el origen para ser resistente a ataques con ordenadores cuánticos.

No es teoría. Es código y un whitepaper de 24 páginas que acabo de publicar.

---

**3/10**

El problema, visualízalo:

Una transacción de Bitcoin en vuelo. 10 minutos para confirmarse.

En el minuto 9, un atacante con un ordenador cuántico ha derivado tu clave privada a partir de tu clave pública (visible en la cadena) y vacía tu cartera.

Tú creías que pagaste. Nadie recibió nada.

Esto es el "ataque de 9 minutos".

---

**4/10**

Lo que casi nadie explica: hay DOS amenazas cuánticas, no una.

1️⃣ Suplantación → te roban firmando como tú.
2️⃣ Cosecha retroactiva → "harvest now, decrypt later". Tu historial cifrado de hoy se descifra mañana.

Bitcoin y Ethereum sufren las dos. Las "soluciones" actuales solo cubren la primera.

---

**5/10**

QRB cubre las dos:

🔐 **Firmas ML-DSA-65** (estándar NIST 2024) para autenticación.
👁️ **STARKs + lattice commitments** para privacidad post-cuántica real.

¿Por qué STARKs? Porque los SNARKs de Aleo y Aztec **NO son post-cuánticos**. Su privacidad es falsa a largo plazo. Cosechan hoy, descifran mañana.

---

**6/10**

¿Por qué L2 sobre Ethereum y no L1 propia?

🔸 Hereda seguridad y liquidez de Ethereum desde el día 1.
🔸 Cualquier app de Solidity migra sin reescribir nada.
🔸 Cuesta 10× menos lanzar.

Una L1 PQ-nueva tarda años y muere por falta de validadores. Una L2 PQ entrega valor en meses.

---

**7/10**

Bonus que nadie más está haciendo:

Integración planificada con **QKD** (Quantum Key Distribution).

Bennett y Brassard recibieron el ACM A.M. Turing Award 2025 (anunciado en marzo de 2026) por su BB84 de 1984. Su criptografía cuántica física se despliega ya en Alemania, China, Telefónica.

QRB será la primera blockchain que combine la respuesta matemática (PQ) Y la respuesta física (QKD).

---

**8/10**

Estado actual:

✅ Whitepaper v0.2 publicado (PDF, 24 pp)
✅ Prototipo Python funcional con firmas Dilithium reales
✅ Open source MIT/Apache-2.0
🔜 Solicitud de grants a @ethereumfndn (ESP), NLnet, Optimism

Buscando colaboradores:
- Dev Rust/Go (blockchain client)
- Criptógrafo (retículos / Dilithium)
- Dev frontend (wallet + explorer)
- Technical writer ES/EN

DMs abiertos.

---

**9/10**

Filosofía de financiación:

1️⃣ Grants no dilutivos (Ethereum Foundation, NLnet, Optimism)
2️⃣ Producto demostrable + comunidad
3️⃣ Solo entonces token, registrado bajo MiCA

🚫 No ICO antes de producto.
🚫 No vaporware.
🚫 No promesas sin código.

El sector cripto necesita más proyectos así.

---

**10/10**

📄 Whitepaper v0.2: [URL del PDF en GitHub]
💻 Repo: [URL de GitHub]
🐦 Sígueme aquí para updates de Fase 0.

Si construyes cripto, si tienes claves expuestas en cadena, si te importa la privacidad post-cuántica de tus datos a 30 años vista — esto te interesa.

RT si quieres apoyar.

#PostQuantum #Ethereum #L2 #Cryptography

---

## 3. Versión post largo (X Premium / LinkedIn / Mirror)

Si tienes X Premium o quieres publicar en LinkedIn / Mirror.xyz, copia el contenido de [resumen.md](../resumen.md) como artículo. Es exactamente la longitud correcta para una pieza de pensamiento (~700 palabras).

Title sugerido para LinkedIn / Mirror:

> *"Cuando la criptografía caiga: por qué construyo una blockchain post-cuántica sobre Ethereum"*

---

## 4. Mensaje corto para DMs (cuando alguien te pregunte qué haces)

> QRB es una blockchain de capa 2 sobre Ethereum diseñada desde el día uno para ser resistente a ataques con ordenadores cuánticos, los que la industria estima entre 2028 y 2032. A diferencia de los otros proyectos post-cuánticos (QRL, Quranium, Aleo, Aztec), QRB combina autenticación PQ + privacidad PQ + EVM nativa, lo cual ninguno de ellos tiene. Whitepaper v0.2 y prototipo en GitHub. Open source.

---

## 5. Cómo subir el repo a GitHub público (paso a paso)

### Si NO tienes cuenta de GitHub

1. Ve a https://github.com/signup
2. Usa tu correo `openclow153@gmail.com` (o el que prefieras).
3. Elige username público (sugerencias: `openclow`, `fiyiware`, `qrb-founder` — el que ya uses).
4. Verifica el email.
5. Plan gratuito está bien.

### Crear el repositorio

1. Una vez dentro, click en **"+"** arriba a la derecha → **"New repository"**.
2. Datos:
   - **Repository name**: `quantum-resistance-blockchain` (recomendado) o `qrb`
   - **Description**: `Post-quantum L2 blockchain on Ethereum with ML-DSA-65 signatures and a STARK-based privacy layer (Fase 3+ vision)`
   - **Visibility**: ✅ **Public**
   - ❌ NO marques "Add a README" ni "Add .gitignore" ni "Choose a license" (ya los tenemos en local).
3. Click en **"Create repository"**.
4. Te aparecerá una página con instrucciones. Cópiate la URL HTTPS que se ve arriba (algo como `https://github.com/TU_USUARIO/quantum-resistance-blockchain.git`).

### Conectar el repo local con GitHub y subir

Abre PowerShell:

```powershell
cd "C:\Users\openc\quantum-resistance-blockchain"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/quantum-resistance-blockchain.git
git push -u origin main
```

(Reemplaza `TU_USUARIO` por tu username de GitHub.)

La primera vez te pedirá autenticación. La forma moderna es con un **Personal Access Token** o el **GitHub CLI** (`gh auth login`). Si tienes problemas, házmelo saber.

### Después de subir

1. Ve a la página de tu repo en GitHub.
2. Click en el icono de engranaje al lado de "About" (arriba a la derecha del listado de archivos).
3. Añade en "Description": el mismo texto del paso 2.
4. En "Topics" añade: `blockchain`, `post-quantum`, `ethereum`, `l2`, `cryptography`, `dilithium`, `stark`, `mica`, `quantum-resistant`, `open-source`.
5. En "Website" pon el dominio cuando lo tengas.

---

## 6. Plan de los próximos 7 días

| Día | Acción | Tiempo estimado |
|-----|--------|-----------------|
| **Hoy (29 mayo)** | Crear cuenta X · Crear cuenta GitHub si no tienes · Foto de perfil simple QRB | 1 h |
| **30 mayo** | Subir el repo a GitHub público · Verificar que el PDF se ve bien en línea · Configurar la cabecera y bio de X | 1-2 h |
| **31 mayo** | Publicar el hilo de lanzamiento en X · Compartir el repo en r/CryptoCurrency, r/ethereum, r/postquantum, Hacker News (Show HN) | 2 h |
| **1 junio** | Empezar el borrador de la aplicación NLNet (formulario en https://nlnet.nl/propose/) | 3-4 h |
| **2-3 junio** | Búsqueda activa de co-fundador técnico: Twitter DMs, LinkedIn, foros de criptografía PQ | 3 h/día |
| **4-5 junio** | Enviar aplicación NLNet · Compartir en Telegram/Discord de PQ-cripto comunidad | 2 h/día |

---

## 7. Hashtags / cuentas a mencionar en X

**Hashtags recomendados** (no satures un solo tuit, distribúyelos):

- `#PostQuantum` · `#PostQuantumCrypto` · `#PQC`
- `#Ethereum` · `#L2` · `#Layer2`
- `#Cryptography` · `#ZeroKnowledge` · `#STARKs`
- `#OpenSource` · `#Blockchain`
- `#MiCA` (para audiencia europea / regulación)

**Cuentas a etiquetar gradualmente** (sin spam, una o dos por hilo):

- `@VitalikButerin` — el cerebro detrás de Ethereum, ha hablado públicamente del riesgo cuántico
- `@ethereumfndn` — Ethereum Foundation
- `@StarkWareLtd` — referencia técnica de STARKs
- `@nlnet` — NLNet Foundation (grants)
- `@optimismFND` — Optimism Foundation (RetroPGF)
- `@solangegueiros` — divulgadora cripto en español
- `@bit2me` — exchange español, relevante audiencia

---

## 8. Respuestas preparadas para los críticos

Te van a salir. Aquí algunas réplicas preparadas:

**"Otro proyecto vaporware más"**
> El whitepaper técnico y el prototipo funcional están en GitHub público, MIT. Cero ICO, cero token todavía. Si te parece vaporware, abre el código.

**"Ethereum va a migrar a PQ, no necesitáis vuestra cadena"**
> Cierto, y eso es bueno para todos. Pero Ethereum estima 4-7 años para migrar L1. Mientras tanto, QRB cubre el hueco para quienes no pueden esperar (RWA tokenizado, custodios institucionales, compliance NIS2).

**"QRL ya hace esto"**
> QRL hace firmas PQ, no privacidad PQ. Y su EVM-compatibilidad es parcial y reciente. QRB cubre los tres ejes (auth PQ + privacy PQ + EVM nativa) que ningún proyecto del mercado combina.

**"Los STARKs son demasiado pesados para producción"**
> Lo eran. Plonky3 (Polygon) y los avances de StarkWare en 2024-2026 han reducido el coste 10×. Y aún así, Fase 3+. Por algo el roadmap es escalonado.

**"15% del fundador es mucho"**
> Es estándar de la industria (10-25%). Con cliff de 12 meses y vesting 36 meses adicional. Sin posibilidad de vender el día 1. Diseñado precisamente para alinear incentivos a largo plazo.

---

*Este documento se actualizará conforme avance la Fase 0. Sugerencias bienvenidas vía issue en el repo.*
