# QRB — Quantum-Resistance Blockchain
## Whitepaper técnico-económico
**Versión 0.2 · Borrador · Mayo 2026**

> 🌐 **Idioma / Language:** **Español** · [English](whitepaper-v0.2.en.md)

> *"Todo el internet de los últimos 40 años será un libro abierto, y no hay nada que puedas hacer para salvar el pasado."*
>
> — **Gilles Brassard**, co-creador de la criptografía cuántica (protocolo BB84, 1984), ACM A.M. Turing Award 2025 (anunciado en marzo de 2026)

---

## Prólogo — El ataque de 9 minutos

Imagina una transacción de Bitcoin en vuelo. El emisor pulsa enviar. Los 10 minutos medios de confirmación empiezan a correr.

En el minuto 9, un atacante con un ordenador cuántico de tamaño suficiente ha derivado la clave privada del emisor a partir de su clave pública —visible para cualquiera en la cadena— y desvía los fondos a su propia cartera. La transacción original muere en el mempool, sin confirmar. El emisor cree que ha pagado. El receptor sigue esperando. El dinero se ha evaporado en 9 minutos.

Esto no es ciencia ficción. Es matemática que existe desde 1994 (el algoritmo de Shor) y hardware cuyo ritmo de avance se ha disparado en los últimos 18 meses:

- En **marzo de 2026**, Google publicó que romper la criptografía elíptica de Bitcoin requiere **menos de 500.000 qubits físicos**, frente a 20 millones que estimaba la misma compañía en 2019.
- Días después, investigadores de **Caltech** y la startup **Atomic** demostraron que con arquitectura basada en átomos controlados por láser, podrían bastar **10.000 qubits**.
- Los ordenadores cuánticos comerciales actuales **ya tienen entre 1.000 y 2.000 qubits**.
- En **abril de 2026**, el investigador independiente **Giancarlo Lelli** rompió la primera clave ECC pública (15 bits) con un ordenador cuántico de acceso comercial y ganó el **Q-Day Prize** de Project Eleven (1 BTC).
- En **enero de 2026**, el banco de inversión **Jefferies** retiró el 10% de su asignación a Bitcoin en sus carteras modelo, citando explícitamente el riesgo cuántico.
- **Google** ha adelantado su propio plazo interno de migración post-cuántica al **año 2029**, recortando seis años respecto al plazo del NIST (2035).
- **Vitalik Buterin** (fundador de Ethereum): *"cripto tiene hasta 2028 para evitar el colapso cuántico."*

El consenso experto se ha contraído brutalmente. Hace dos años se hablaba de 2040. Hoy se habla de **2028-2032**.

Mientras tanto, los datos cifrados de hoy ya se están cosechando — comunicaciones, transacciones blockchain, historiales médicos, correos clasificados — para descifrarlos cuando exista el hardware. Esta práctica tiene nombre: *Harvest Now, Decrypt Later*. Brassard, galardonado con el ACM A.M. Turing Award 2025 (anunciado en marzo de 2026) por inventar la criptografía cuántica cuarenta años antes de que el mundo lo necesitara, lo resume sin adornos: *"todo el internet de los últimos 40 años será un libro abierto, y no hay nada que puedas hacer para salvar el pasado."*

**QRB existe para que el futuro no sea ese libro abierto.**

---

## Resumen ejecutivo

QRB (Quantum-Resistance Blockchain) es una blockchain de capa 2 (L2) construida sobre Ethereum, diseñada desde el origen para ser resistente a ataques con ordenadores cuánticos en **dos dimensiones complementarias**:

1. **Autenticación post-cuántica**: las firmas digitales se sustituyen por algoritmos estandarizados por NIST en 2024 (ML-DSA / CRYSTALS-Dilithium, FN-DSA / FALCON, SLH-DSA / SPHINCS+). Esto neutraliza el ataque de Shor sobre claves elípticas — el ataque de 9 minutos descrito en el prólogo. **Implementado y demostrable en el prototipo de Fase 0 (mayo 2026).**

2. **Confidencialidad post-cuántica** (visión Fase 3+): una capa nativa de privacidad que combina *stealth addresses*, transacciones confidenciales con compromisos basados en retículos, pruebas de conocimiento cero (ZK) construidas sobre **STARKs** (hash-based, nativamente post-cuánticos), y *view keys* opcionales para compliance MiCA. Esto neutraliza el ataque de cosecha retroactiva sobre el historial de transacciones — los datos publicados hoy permanecen confidenciales aunque alguien tenga un cuántico mañana.

A estas dos dimensiones criptográficas se les suma:

- **Compatibilidad total con la EVM** y herramientas de desarrollo Ethereum (Solidity, Hardhat, Foundry, MetaMask con adaptador PQ): cualquier app de Ethereum migra sin reescribir.
- **Account Abstraction nativa**: oculta al usuario final la complejidad y el tamaño de las firmas post-cuánticas. UX equivalente a una cartera Ethereum normal.
- **Integración opcional con redes QKD** (Quantum Key Distribution) para clientes institucionales que ya operan sobre infraestructura cuántica física (línea de investigación, visión Fase 3+; no es un objetivo de Fase 0 ni Fase 1). Es una posibilidad exploratoria, no un compromiso de entrega temprana.
- **Estrategia de financiación responsable**: subvenciones públicas no dilutivas en Fase 1 (NLNet, Ethereum Foundation, Optimism), inversión seed en Fase 2, y solo entonces emisión de token registrada bajo whitepaper MiCA con asesoramiento legal.

El presente documento describe el problema, la solución técnica, el modelo económico, la gobernanza, el *roadmap* y los riesgos del proyecto. Está dirigido a desarrolladores, criptógrafos, evaluadores de subvenciones y, en una fase posterior, a inversores institucionales.

---

## 1. El problema

### 1.1 Dos amenazas cuánticas, no una

Toda la criptografía de clave pública que sostiene la economía digital actual depende de dos suposiciones matemáticas: la dificultad de **factorizar enteros grandes** (RSA) y la dificultad del **logaritmo discreto en curvas elípticas** (ECDSA, EdDSA, Schnorr). En 1994, Peter Shor demostró que un ordenador cuántico de tamaño suficiente puede resolver ambos problemas en tiempo polinómico. No es conjetura: es matemática demostrada.

A partir de ese único algoritmo, se derivan **dos clases de amenaza distintas** que QRB neutraliza por separado:

| Amenaza | Qué rompe | Ejemplo concreto |
|---------|-----------|------------------|
| **A — Suplantación** (Shor sobre firmas) | El atacante deriva la clave privada del emisor y firma transacciones en su nombre | El ataque de 9 minutos sobre Bitcoin. Vaciado de carteras con clave pública expuesta |
| **B — Cosecha retroactiva** (Shor sobre cifrado de canal + descifrado de datos almacenados) | El atacante descifra contenido capturado años antes | *Harvest now, decrypt later*. Lectura retrospectiva del historial completo de la cadena |

La industria post-cuántica actual cubre fundamentalmente la **Amenaza A** (firmas resistentes). QRB se posiciona como la primera blockchain que cubre **A y B** simultáneamente. La sección 7.5 detalla la capa B.

### 1.2 La línea temporal se ha contraído

| Año | Estimación de qubits para romper RSA-2048 / ECC-256 | Fuente |
|-----|---------------------------------------------|--------|
| 2012 | ~1.000 millones (físicos, estimaciones era RSA-2048) | Estimaciones académicas |
| 2019 | ~20 millones (físicos, RSA-2048) | Gidney y Ekerå (Google) |
| Mayo 2025 | ~1 millón (físicos) | Google Research (revisión) |
| Marzo 2026 | **< 500.000** (físicos) | Google Quantum AI |
| Marzo 2026 | **~10.000** (lógicos, arquitectura atómica) | Caltech + Atomic |

> **Aviso metodológico — estas cifras no son comparables entre sí.** Mezclan *objetivos* (factorizar RSA-2048 vs logaritmo discreto en ECC-256 — la cifra de 2019, por ejemplo, es la estimación de Gidney y Ekerå para **factorizar RSA-2048**, no para romper ECC) y *tipos de qubit* (físicos ruidosos vs lógicos con corrección de errores). Un qubit lógico tolerante a fallos requiere hoy **del orden de cientos a miles de qubits físicos**; los ordenadores comerciales actuales (IBM, Google, Quantinuum, IonQ) tienen **1.000-2.000 qubits *físicos* ruidosos**, sin esa corrección de errores. Por tanto, la brecha real entre lo disponible hoy y lo necesario es **mucho mayor** de lo que sugiere comparar los números en bruto, y el coste de romper claves más grandes no escala de forma lineal. Lo relevante de la tabla es la **tendencia descendente en los recursos estimados**, no ninguna cifra comparable concreta.

La tendencia de las estimaciones, no obstante, es inequívocamente descendente: varios órdenes de magnitud de reducción en los recursos estimados a lo largo de una década. **La fecha exacta de llegada de un ordenador cuántico criptográficamente relevante (CRQC) es genuinamente incierta**; lo que no es incierto es la dirección, ni el hecho de que la infraestructura criptográfica tarda años en migrarse. Esa asimetría — migración lenta frente a amenaza creciente — es la que justifica actuar ahora.

Plazos publicados por actores serios:

- **Google**: migración interna completada en **2029**.
- **NIST**: estándar de transición fijado en 2035, pero superado por los plazos de la industria.
- **CNSA 2.0 (NSA, EEUU)**: sistemas clasificados completamente migrados antes de 2035.
- **ANSSI (Francia), BSI (Alemania)**: criptografía PQ obligatoria para sistemas críticos antes de 2030.
- **NIS2 (UE, vigente desde octubre 2024)**: resistencia cuántica como criterio de diligencia exigible.
- **MiCA (UE, vigente desde diciembre 2024)**: regula los emisores de criptoactivos, abriendo expectativa de requisitos PQ para tokens en infraestructuras críticas.

### 1.3 Harvest now, decrypt later: el robo que ya empezó

Las transacciones blockchain son **públicas y permanentes**. Una firma ECDSA emitida hoy quedará disponible para ataque retrospectivo cuando exista un ordenador cuántico criptográficamente relevante (CRQC). Las direcciones de las que ya se ha gastado tienen su clave pública expuesta en la cadena para siempre.

- En Bitcoin, **aproximadamente 6,9 millones de BTC** (≈ un tercio del suministro total) están en direcciones con clave pública expuesta, incluyendo el millón estimado del propio Satoshi Nakamoto. Conviene matizar: las estimaciones de cuánto es *explotable de inmediato* varían — por ejemplo, CoinShares defiende un subconjunto mucho menor (del orden de 10.000 BTC en direcciones legacy P2PK) — pero la superficie de claves expuestas crece con el tiempo a medida que se reutilizan direcciones. Lo relevante es la dirección de la curva, no la cifra exacta.
- En Ethereum, la situación es similar para toda cuenta que haya enviado al menos una transacción.
- Las **comunicaciones cifradas** del 99% del tráfico de internet (TLS sobre curvas elípticas) están siendo activamente almacenadas por actores estatales con incentivos de inteligencia a largo plazo.

La asimetría temporal es lo que hace este ataque devastador: el atacante no necesita la capacidad cuántica **hoy**, solo necesita **almacenar**. El descifrado puede ocurrir cuando la tecnología madure, contra datos de 5, 10 o 20 años de antigüedad.

### 1.4 Migrar las L1 existentes a tiempo es matemáticamente improbable

Un análisis técnico reciente sobre Bitcoin estima que una migración completa del estado de la red a direcciones post-cuánticas requiere **un mínimo de 76 días de actividad continuada en la cadena**, asumiendo consenso unánime de la comunidad desde el primer día. La historia de Bitcoin demuestra que ese consenso no se alcanza nunca en menos de 1-3 años. Ethereum tiene un proceso de governance más ágil pero igualmente lento. Solana, BNB Chain, Avalanche y similares no han publicado plan operativo de migración.

En cambio, **una cadena PQ-nativa desde el día uno no tiene que migrar nada**: nace en el estado correcto. Esa es la ventana estructural en la que existe QRB.

---

## 2. Estado del arte

### 2.1 Comparativa ampliada

| Proyecto | Firmas PQ | Privacidad PQ | EVM | AA | QKD-ready | Limitación principal |
|----------|:---------:|:-------------:|:---:|:--:|:---------:|----------------------|
| Bitcoin / Ethereum L1 | ❌ | ❌ | parcial / ✅ | ❌ / parcial | ❌ | Migración políticamente bloqueada (76+ días, sin consenso) |
| QRL / Zond | ✅ (XMSS → Dilithium) | ❌ | parcial | ❌ | ❌ | UX deficiente, ecosistema mínimo |
| Quranium | ✅ (Dilithium) | ❌ | parcial | ❌ | ❌ | Comunidad y tracción de devs muy pequeñas |
| Cellframe | ✅ (CRYSTALS, NTRU) | parcial | ❌ | ❌ | ❌ | Arquitectura compleja, *fork* difícil |
| Naoris Protocol | ✅ (híbrido) | ❌ | ❌ | ❌ | ❌ | Más una red de seguridad que blockchain general |
| Aleo | ❌ (SNARK) | ✅ (no PQ) | ❌ | ❌ | ❌ | Privacidad no resistente a cuántico |
| Aztec | ❌ (SNARK) | ✅ (no PQ) | parcial | ✅ | ❌ | Privacidad no resistente a cuántico |
| Monero | ❌ | ✅ (no PQ) | ❌ | ❌ | ❌ | Privacidad no resistente a cuántico, sin smart contracts |
| **QRB (objetivo del roadmap)** | **✅ ML-DSA-65 (Fase 0)** | 🔬 STARKs (Fase 3+) | 📐 Fase 1 | 📐 Fase 1 | 🔬 Fase 3+ | Proyecto joven; núcleo L2 aún por construir |

> **Lectura honesta de esta tabla.** Las columnas describen la **combinación de capacidades que QRB persigue a lo largo de todo su roadmap**, no su estado actual. Solo la autenticación PQ (ML-DSA-65) está implementada hoy en el prototipo de Fase 0; EVM y Account Abstraction están diseñadas para Fase 1, y la privacidad PQ y la integración QKD son línea de investigación / visión Fase 3+. El valor de la tabla no es reclamar paridad de funciones hoy, sino señalar que **ningún proyecto conocido persigue las cinco dimensiones juntas**. El estado preciso de cada componente está en la sección de roadmap (§8) y en la tabla de estado del README del repositorio.

Ningún proyecto del mercado combina las cinco columnas. QRB se posiciona en ese hueco.

### 2.2 ¿Por qué L2 y no L1?

Una L1 propia obliga a resolver el problema de los **incentivos de validador**: convencer a operadores de nodos a destinar hardware y capital, lo cual exige una emisión inflacionaria significativa de token nativo y captación de comunidad. Para un proyecto que no parte de un fondo de 20-50 millones de euros, esto es prohibitivo y conduce históricamente a redes inseguras los primeros 1-3 años.

Una L2 sobre Ethereum, en cambio:
- **Hereda la seguridad** del *settlement layer* de Ethereum.
- **Hereda la liquidez** vía bridges establecidos.
- **Reduce el coste inicial** a un factor 10× respecto a una L1.
- **Permite enfocarse en lo diferencial** (la criptografía PQ, la privacidad y la UX) en vez de gastar recursos reinventando consenso.

---

## 3. Solución técnica — Capa de autenticación PQ

### 3.1 Pila criptográfica

QRB adopta los estándares NIST post-cuánticos como base de autenticación:

- **Firmas digitales primarias**: ML-DSA (FIPS 204, CRYSTALS-Dilithium), específicamente **ML-DSA-65** como *default*. Equivalente a 192 bits de seguridad clásica. Firma ~3.309 bytes; clave pública ~1.952 bytes.
- **Firmas alternativas opt-in**: FN-DSA (FALCON, FIPS 206) para casos que requieran firmas compactas (~700 bytes); SLH-DSA (SPHINCS+, FIPS 205) para escenarios de máxima conservación basados en hash.
- **Intercambio de claves**: ML-KEM (FIPS 203, CRYSTALS-Kyber), específicamente ML-KEM-768, para comunicación cifrada entre nodos.
- **Hash**: Keccak-256 (compatibilidad EVM) y SHA3-512 como precompilado para aplicaciones con margen post-cuántico explícito frente a Grover.

### 3.2 Firmas híbridas durante la transición

Durante los primeros 24 meses de mainnet, QRB ofrecerá un modo **firma híbrida** opcional: cada transacción puede ir firmada simultáneamente con ECDSA-secp256k1 y con ML-DSA. La transacción solo se considera válida si **ambas** firmas lo son. Este mecanismo permite migración progresiva sin *cutover* abrupto.

### 3.3 Abstracción de cuenta (Account Abstraction) PQ

Las firmas PQ son ~50× más grandes que ECDSA. Para evitar que esto degrade la experiencia del usuario, QRB implementa **Account Abstraction nativa** (ERC-4337-like) desde el primer bloque:

- Cada cuenta es un contrato inteligente con su propia lógica de validación de firmas.
- Las firmas PQ se verifican vía **precompilado** dedicado con coste de gas estable.
- Los usuarios pueden definir **rotación de claves**, **recuperación social**, **paymasters**, **multifirma PQ** y **firma delegada** sin cambios en el protocolo.
- Las direcciones se derivan del **hash** de la clave pública (SHA3-256, últimos 20 bytes en hex), permitiendo que esta permanezca oculta hasta el primer gasto desde la dirección — protección elemental contra *harvest now, decrypt later* en su forma básica.

### 3.4 EVM-compatibilidad

La capa de ejecución de QRB es un *fork* del cliente Reth (Rust) o Geth (Go) modificado para:

- Reemplazar el opcode `ECRECOVER` por `DSARECOVER` en transacciones nativas.
- Añadir precompilados en `0x100`-`0x103` para ML-DSA-44, ML-DSA-65, ML-DSA-87 y FN-DSA-512 respectivamente.
- Mantener todos los demás opcodes EVM estándar inalterados — cualquier contrato Solidity compila sin cambios.
- Mantener `ECRECOVER` funcional para bridges y compatibilidad histórica, marcado como obsoleto.

### 3.5 Bridge a Ethereum

El bridge es el componente más crítico de seguridad de cualquier L2. QRB adopta el modelo **optimistic rollup** del OP Stack en su versión actual, con:

- Firmas de proponedores y verificadores en ML-DSA-65 desde día 1.
- Periodo de impugnación de 7 días, alineado con Optimism.
- Plan de migración a **ZK-rollup con STARKs** una vez existan probadores eficientes para firmas Dilithium (investigación activa en 2026).

---

## 4. Arquitectura

```
┌────────────────────────────────────────────────────────────────┐
│                  Capa de Aplicación                             │
│  (DeFi, NFTs, identidad PQ, tokenización RWA, juegos)           │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│         Capa de Confidencialidad PQ (Fase 3+ — §7.5)            │
│  Stealth addresses · Confidential tx · STARK proofs · View keys │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│            Capa de Cuenta (Account Abstraction PQ)               │
│   Wallets contractuales · Rotación de claves · Multisig PQ       │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│           Capa de Ejecución (EVM + Precompilados PQ)             │
│ Reth fork · DSARECOVER · ML-DSA / FN-DSA / SLH-DSA precompilados │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│         Capa de Submission (estándar HTTPS + QKD-opcional §4.6) │
│         Mempool público + canales QKD-secured institucionales    │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│        Capa de Disponibilidad de Datos y Settlement              │
│   Calldata en Ethereum (Fase 1) → EIP-4844 blobs (Fase 2)        │
│   Pruebas de fraude PQ · Bridge optimista                        │
└────────────────────────────────────────────────────────────────┘
                              │
┌────────────────────────────────────────────────────────────────┐
│                Ethereum L1 (settlement & DA)                     │
└────────────────────────────────────────────────────────────────┘
```

### 4.6 Integración QKD para clientes institucionales (Fase 3+ visión)

La criptografía post-cuántica matemática (PQ) y la criptografía cuántica física (QKD, *Quantum Key Distribution*) son **complementarias, no competidoras**. PQ funciona sobre cualquier red TCP/IP. QKD requiere fibra dedicada o satélites (como Micius en China; redes de Telefónica/Deutsche Telekom en la UE; servicios de Amazon Braket y AWS Center for Quantum Networking en EEUU).

QRB integra opcionalmente canales QKD para el **submission de transacciones** desde clientes institucionales:

- **Caso de uso**: un banco europeo con red QKD interna (varios ya las tienen desplegadas tras NIS2) puede enviar sus transacciones a QRB sobre canal QKD-seguro, garantizando confidencialidad perfecta del propio acto de enviar la transacción, no solo del contenido.
- **Cómo funciona**: la wallet institucional firma con ML-DSA-65 igual que cualquier usuario, pero el canal de envío al nodo más cercano va cifrado con clave establecida por BB84. El nodo receptor reenvía a su mempool normal.
- **Posible interés diferencial**: no nos consta otra blockchain que haya publicado una integración formal con la pila QKD existente. Si los despliegues de QKD en Europa (acelerados por NIS2) maduran, podría abrirse un mercado B2B institucional. Lo presentamos como hipótesis a explorar, no como ventaja ya conquistada.
- **Limitaciones honestas**: QKD protege únicamente el *canal de envío*, no el contenido on-chain (que es público salvo que se use la capa de confidencialidad §7.5); QKD por sí sola no autentica (de ahí que se combine con firmas ML-DSA); y requiere fibra dedicada o enlaces satelitales, lo que la restringe a clientes institucionales. No es una bala de plata.
- **Estado**: línea de investigación / visión Fase 3+. Requeriría una alianza con uno o varios operadores QKD europeos (posibles caminos: pilotos vía Cellnex, Telefónica Tech o Deutsche Telekom T-Systems). No es un objetivo de Fase 0 ni Fase 1.

---

## 5. Tokenomics

> **Marco previo — el token es Fase 2+, contingente y fuera del alcance de cualquier subvención.** Lo que sigue describe el modelo económico *previsto a largo plazo*, no algo activo hoy. El token QRB no se emite ni interviene en las Fases 0 y 1, que son de código abierto (MIT) y se financian con fondos propios y subvenciones públicas no dilutivas. Ningún entregable de Fase 1 depende del token. Su eventual emisión queda condicionada a (a) la existencia de un producto en funcionamiento, (b) un proceso de registro conforme a MiCA y (c) asesoramiento legal. Las subvenciones recibidas no se destinan en ningún caso a actividades relacionadas con el token.

### 5.1 El token QRB

El token nativo del ecosistema se denominará **QRB**. Sus funciones son:

- **Pago de gas**: todas las transacciones se pagan en QRB.
- **Staking** para secuenciadores y verificadores descentralizados (Fase 2+).
- **Gobernanza** del protocolo (Fase 2+).
- **Acceso a servicios** del ecosistema (despliegue de tokens, *naming service*, paymasters, integración QKD institucional).

### 5.2 Suministro total y distribución

Suministro fijo (no inflacionario): **1.000.000.000 QRB**.

| Categoría | % | Cantidad | Vesting / Desbloqueo |
|-----------|---|----------|----------------------|
| Fundador y equipo inicial | 15% | 150.000.000 | *Cliff* 12 meses + vesting lineal 36 meses |
| Tesorería de la Fundación | 20% | 200.000.000 | Liberada por gobernanza, ritmo máx. 2%/mes |
| Validadores / Stakers (recompensas) | 30% | 300.000.000 | Emisión gradual durante 10 años |
| Ecosistema y subvenciones a devs | 25% | 250.000.000 | Liberada por gobernanza |
| Liquidez inicial y oferta pública | 10% | 100.000.000 | Activada con mainnet, sujeta a registro MiCA |

Diseño conservador a propósito: 15% de fundador con vesting largo está por debajo del estándar de la industria para no levantar señales de centralización.

### 5.3 Fees del protocolo

Gas siguiendo el modelo EIP-1559:

- **Base fee**: quemada (deflacionaria).
- **Priority fee**: para el secuenciador / proponedor.
- **Protocol fee**: 15% sobre el priority fee, dirigido a la tesorería para sostener desarrollo, auditorías y subvenciones a largo plazo.

### 5.4 Captura de valor del ecosistema

Cualquier token desplegado en QRB (ERC-20-PQ, ERC-721-PQ, etc.) paga:

- Un fee fijo de despliegue en QRB (~5-50 QRB según tipo).
- Las transferencias y operaciones consumen gas en QRB.
- (Fase 3+) El uso de transacciones confidenciales consume un múltiplo de gas para reflejar el coste de generar la prueba STARK.

---

## 6. Gobernanza

QRB seguirá un modelo de gobernanza **progresivamente descentralizada**:

- **Fase 0-1**: gobernanza centralizada en la Fundación QRB (entidad jurídica a constituir, probablemente en España o Suiza). Decisiones técnicas tomadas por el equipo core, publicadas abiertamente.
- **Fase 2**: introducción de propuestas on-chain (QRB Improvement Proposals, QIPs) vinculantes para parámetros del protocolo (gas, fees, tesorería).
- **Fase 3+**: gobernanza completamente on-chain con poder de veto residual de la Fundación para emergencias de seguridad. Plan explícito de eliminación de ese veto tras 5 años de mainnet estable.

---

## 7. Seguridad

### 7.1 Modelo de amenazas

QRB se diseña frente a un atacante con:

- Recursos computacionales cuánticos crecientes (CRQC potencial 2028-2032 según consenso experto actualizado).
- Capacidad de *harvest now, decrypt later* sobre el historial público de la cadena.
- Control de hasta 33% del *stake* (asunción estándar BFT).
- Acceso completo al código fuente (todo el proyecto es open source MIT/Apache-2.0).

### 7.2 Auditorías y verificación

Antes de mainnet (Fase 2):

- **Auditoría criptográfica** del módulo de firmas PQ por una firma especializada (Trail of Bits, Least Authority, NCC Group). Coste estimado: 60.000-120.000 €.
- **Auditoría EVM** del cliente de ejecución modificado. 50.000-100.000 €.
- **Auditoría del bridge**. 80.000-150.000 €.
- **Verificación formal** de las precompilaciones PQ con Coq o Lean (objetivo a 24 meses).
- **Bug bounty** con techo de 500.000 QRB para fallos críticos.

### 7.3 Plan de emergencia

Multifirma de emergencia (5 de 9, Fundación + figuras externas reputadas del ecosistema) con poder de **pausa del bridge** durante 72 horas máximo. Sin poder sobre el estado de la cadena ni sobre los fondos de usuarios.

### 7.4 Riesgo de la propia primitiva PQ

Las firmas post-cuánticas son criptografía joven. Es posible que se descubra un ataque clásico contra Dilithium en los próximos años. QRB mitiga este riesgo:

- Diseño **agnóstico de algoritmo**: la precompilación de validación es intercambiable.
- **Plan B preestablecido**: migración a SLH-DSA (hash-based, supuestos criptográficos más conservadores) en menos de 30 días si Dilithium fuera comprometido.
- **Firmas híbridas opcionales** durante los primeros 24 meses como cinturón de seguridad adicional.

### 7.5 Capa de Confidencialidad (Fase 3+ visión)

Esta sección describe la respuesta de QRB a la **Amenaza B** (cosecha retroactiva). Es la pieza que distingue a QRB de toda otra blockchain post-cuántica del mercado y la convierte en una propuesta de privacidad real, no solo de autenticación segura.

#### 7.5.1 Stealth addresses

Cada vez que un usuario recibe una transacción, la wallet del emisor deriva una **dirección de un solo uso** a partir de un par de claves de visión y gasto del receptor (modelo análogo al EIP-5564 de Ethereum y al de Monero, adaptado a primitivas PQ). Resultado: ningún observador puede vincular dos pagos diferentes al mismo usuario. La dirección pública que QRB publica para recibir nunca aparece directamente en la cadena.

#### 7.5.2 Transacciones confidenciales

El importe de cada transacción va **cifrado** mediante un compromiso criptográfico lattice-based (variante post-cuántica de Pedersen). Solo emisor y receptor conocen la cantidad. La cadena verifica que la suma de entradas iguala a la suma de salidas sin desvelar las cantidades concretas, mediante una prueba *range proof* construida sobre STARKs.

#### 7.5.3 ZK-proofs sobre STARKs (decisión técnica crítica)

**SNARKs (Groth16, PLONK, BN254) NO son post-cuánticos** — sus parámetros descansan en suposiciones de curvas elípticas. El riesgo exacto depende de la construcción: los compromisos *ocultadores* en sentido teórico-informacional (p.ej. Pedersen) **no** filtran el valor comprometido a un futuro ordenador cuántico — pero su *binding* puede romperse (permitiendo inflación indetectable), y cualquier payload cifrado con intercambio de claves elíptico (note encryption, ECDH de stealth addresses) **sí** es descifrable retroactivamente — *harvest now, decrypt later* real. En todo caso, la privacidad que descansa en suposiciones de curvas elípticas no aguanta a largo plazo. Es el riesgo subestimado de proyectos como Aleo y Aztec: su privacidad protege hoy, pero sobre supuestos que un CRQC rompe. Los STARKs lo evitan por completo porque solo dependen de la resistencia a colisiones de hash.

**STARKs son nativamente post-cuánticos**: solo dependen de funciones hash colision-resistentes (modelable como oráculo aleatorio) y de códigos Reed-Solomon. Tamaño de prueba mayor (~50-200 KB hoy, en mejora rápida), pero seguridad sólida sobre las suposiciones más conservadoras conocidas.

QRB construye toda su capa de privacidad sobre STARKs. Implementaciones de referencia: StarkWare (Cairo, ya en producción en Starknet), RISC Zero, Plonky3 (Polygon).

#### 7.5.4 Selective disclosure / view keys

El usuario puede generar una clave de **solo lectura** de su historial y entregarla a su banco, asesor fiscal o autoridad reguladora cuando lo requiera. Esto proporciona el equilibrio entre **privacidad por defecto** y **compliance MiCA / AML** sin volver el sistema transparente para todos.

Para empresas reguladas (bancos tokenizando activos, custodios institucionales), QRB soporta también un modo **transparencia opt-in** por contrato — el contrato declara su saldo y movimientos abiertamente, manteniendo confidencial el resto del ecosistema.

#### 7.5.5 Forward secrecy y rotación periódica de claves

La capa de privacidad se diseña con **forward secrecy** estructural: las claves de visión pueden rotarse periódicamente sin perder acceso al historial anterior, limitando el daño que puede causar la fuga de una clave en un momento concreto.

#### 7.5.6 Impacto sobre el modelo de gas

Las pruebas STARK son intensivas en cómputo. El usuario pagará un múltiplo de gas (~10-50×) para transacciones confidenciales respecto a transacciones transparentes. Esto incentiva el uso consciente: pagos pequeños del día a día pueden ir en modo transparente; transacciones grandes, sensibles o institucionales en modo confidencial. El usuario elige.

---

## 8. Roadmap

| Fase | Periodo | Hitos | Presupuesto |
|------|---------|-------|-------------|
| **Fase 0 — Validación** | Q2-Q3 2026 | Whitepaper v0.2 · Prototipo Rust/Python con firmas Dilithium funcionales · GitHub público · Landing · Comunidad embrionaria | 0-2.000 € (autofinanciado) |
| **Fase 1 — Testnet pública** | Q4 2026 - Q3 2027 | Subvenciones (NLNet, EF, Optimism RetroPGF) · Devnet interna · Testnet pública incentivada · Faucet · Explorer · SDK JS/Rust · Primeras 5-10 dApps demo · Bridge inicial Ethereum | 100.000-250.000 € (grants) |
| **Fase 2 — Mainnet beta** | Q4 2027 - Q2 2028 | Auditorías completas · Bridge productivo · Token QRB emitido bajo MiCA · Cotización en DEXs · 50+ contratos desplegados · Account Abstraction productiva | 500.000-2.000.000 € (seed o token regulado) |
| **Fase 3 — Mainnet GA + Capa de privacidad** | H2 2028 - 2030 | Descentralización del secuenciador · Gobernanza on-chain · Pilotos QKD institucionales · Capa de confidencialidad STARK · Stealth addresses · View keys · Migración optimistic → ZK rollup | Autosostenible vía fees + integraciones B2B |

---

## 9. Equipo y colaboradores

**Fundador**: Luiggi Leonel Cedeño Bermeo. Visión de producto, dirección estratégica, representación pública.

**Colaboradores buscados activamente (Fase 0)**:

- 1 desarrollador Rust/Go con experiencia en clientes blockchain (Geth, Reth, Erigon).
- 1 criptógrafo o doctorando con conocimiento de retículos / Dilithium.
- 1 desarrollador frontend para wallet y explorer.
- 1 *technical writer* / comunicador (ES/EN).

**Colaboradores buscados en Fase 1 (con grants ya asegurados)**:

- 1 ingeniero ZK con experiencia en STARKs (StarkWare, RISC Zero, Polygon).
- 1 especialista en QKD / criptografía cuántica física para piloto institucional.
- 1 responsable legal / regulatorio especializado en MiCA y digital assets.

Cualquier contribuidor significativo recibe asignación de la categoría "Ecosistema" en términos a definir con la Fundación.

El proyecto es de fundador único *por diseño* en la Fase 0, pero ya no de una sola *persona* en la práctica: a junio de 2026 ya ha recibido contribuciones externas fusionadas (tests de regresión, correcciones) de desarrolladores independientes — ver el grafo de contribuidores del repositorio. Convertir esa base de contribuidores en un equipo permanente de Fase 1 es justamente el propósito del grant y de la búsqueda anterior.

---

## 10. Financiación

### 10.1 Estrategia general

QRB sigue una estrategia de financiación **escalonada y conservadora**, evitando el modelo *ICO-pre-producto* de 2017-2018.

### 10.2 Fuentes por fase

**Fase 0** — autofinanciación (~1.000 € del fundador + tiempo).

**Fase 1** — subvenciones no dilutivas. Programas objetivo:

- **NLNet / NGI Zero Commons Fund** (Comisión Europea, https://nlnet.nl/commonsfund/) — financiación de tecnología abierta para internet, incluida la criptografía abierta. Tramos de 5.000-50.000 €, con posibilidad de escalar si hay potencial demostrado (hasta 500.000 € por proyecto a lo largo de la vida del fondo).
- **Ethereum Foundation Ecosystem Support** — grants de investigación y tooling, PQ research específicamente bienvenida.
- **Optimism RetroPGF** — pagos retroactivos por bienes públicos sobre OP Stack.
- **Arbitrum Foundation Grants**.
- **Web3 Foundation** (Polkadot).
- **Horizon Europe** programas relacionados con cuántica y ciberseguridad.

**Fase 2** — combinación de:

- Ronda seed con inversores enfocados en infraestructura cripto y/o ciberseguridad cuántica (foco: a16z crypto, Variant, Hashed, fondos europeos especializados).
- Emisión pública del token QRB registrada formalmente bajo **MiCA**: whitepaper notificado a la CNMV, asesoría legal especializada (presupuesto 5.000-15.000 €).

**Fase 3+** — autosostenible vía protocol fees + integraciones B2B (clientes QKD institucionales) + tesorería.

---

## 11. Riesgos y mitigaciones

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|:-------:|:------------:|------------|
| Rotura criptoanalítica de ML-DSA | Catastrófico | Baja | Plan B preestablecido: migración a SLH-DSA. Diseño modular. |
| Ethereum acelera su migración PQ y absorbe la propuesta de valor | Alto | Media | QRB se posiciona como espacio PQ-first mientras Ethereum migra (4-7 años). Cuando Ethereum migre, QRB pivota a especialización: privacidad PQ + QKD institucional. |
| No se obtienen grants en Fase 1 | Alto | Media-Baja | Estrategia paralela en 4-5 programas. Probabilidad combinada de obtener al menos uno: >75%. Si fallan todos, Fase 1 reducida con presupuesto propio. |
| Cambios regulatorios MiCA endurecen requisitos | Medio | Alta | Asesoría legal continua. Modelo de token utility puro (no security). Disposición a registrar como CASP si fuera necesario. |
| Bug crítico en el bridge | Catastrófico | Baja-Media | Auditorías múltiples antes de mainnet. Modo *withdrawal-only* de emergencia. Seguro de protocolo (Nexus Mutual o similar) para Fase 2+. |
| Capa de privacidad genera escrutinio regulatorio adverso | Medio-Alto | Media | Diseño con view keys nativas y modo opt-in transparente. Compliance MiCA como principio rector. |
| Fundador no consigue dedicación a tiempo completo | Medio | Media | Proyecto diseñado para gestión parcial en Fase 0-1. Tras primer grant, dedicación fulltime. |
| QKD no madura como mercado B2B en plazos esperados | Bajo | Media | Visión Fase 3+, no crítica para el producto. Capa de privacidad PQ sigue siendo diferenciador suficiente. |

---

## 12. Conclusión

QRB no aspira a sustituir a Ethereum ni a Bitcoin. Aspira a ser **la red por defecto cuando una organización, un protocolo o un usuario necesiten garantías post-cuánticas reales**: cuando una entidad financiera regulada necesite custodiar activos con compliance NIS2 y MiCA; cuando un protocolo de identidad requiera firmas válidas a 30 años vista; cuando un usuario quiera proteger no solo sus fondos sino su historial financiero del riesgo de cosecha retroactiva.

El proyecto combina:

- Un **problema real y verificable**: la amenaza cuántica documentada por NIST, Google, Caltech, Project Eleven y reconocida por la propia industria (Jefferies, Google, Vitalik).
- Una **solución técnica sólida y doble**: PQ para autenticación, STARKs + lattice para privacidad, ambas estandarizadas o sobre supuestos criptográficos conservadores.
- Una **estrategia de mercado realista**: L2 sobre Ethereum, no L1 desde cero.
- Una **diferenciación única**: única blockchain con autenticación PQ + privacidad PQ + EVM + Account Abstraction + integración QKD planificada.
- Una **financiación legal y escalonada**: grants no dilutivos → seed → token regulado, no al revés.
- Un **equipo abierto y modesto** que prioriza ejecución sobre *hype*.

La ventana para construir esto se cierra cada mes que pasa. Los algoritmos están estandarizados, el hardware cuántico avanza más rápido de lo previsto, y la regulación europea empieza a exigir lo que QRB ofrecerá. La invitación está abierta a desarrolladores, criptógrafos, evaluadores de subvenciones e inversores: este es el momento.

---

## Apéndices

### A. Glosario abreviado

- **CRQC**: Cryptographically Relevant Quantum Computer.
- **ML-DSA**: Module-Lattice Digital Signature Algorithm (FIPS 204, derivado de CRYSTALS-Dilithium).
- **FN-DSA**: FFT over NTRU Digital Signature Algorithm (FALCON).
- **SLH-DSA**: Stateless Hash-based Digital Signature Algorithm (FIPS 205, SPHINCS+).
- **ML-KEM**: Module-Lattice Key Encapsulation Mechanism (FIPS 203, Kyber).
- **STARK**: Scalable Transparent ARgument of Knowledge — pruebas ZK basadas en hash, nativamente post-cuánticas.
- **SNARK**: Succinct Non-interactive ARgument of Knowledge — pruebas ZK típicamente basadas en curvas elípticas, vulnerables a cuántico salvo variantes hash-only.
- **QKD**: Quantum Key Distribution — distribución de claves usando propiedades cuánticas de la luz (protocolos BB84, E91).
- **L2 / Rollup**: capa de escalado construida sobre Ethereum.
- **Account Abstraction**: modelo donde las cuentas son contratos con lógica de validación arbitraria.
- **Harvest now, decrypt later (HNDL)**: práctica de almacenar datos cifrados hoy para descifrarlos cuando exista capacidad cuántica.
- **Stealth address**: dirección derivada de un solo uso para un pago concreto, oculta la identidad del receptor.
- **View key**: clave de solo lectura sobre el historial de una cuenta, usada para *selective disclosure*.

### B. Cronología de hitos cuánticos relevantes

- **1984** — Bennett y Brassard publican el protocolo BB84.
- **1994** — Peter Shor publica el algoritmo de factorización cuántica.
- **1996** — Lov Grover publica el algoritmo de búsqueda cuántica.
- **1989** — Primer experimento físico de BB84 en IBM (32 cm).
- **2017** — China lanza el satélite cuántico Micius.
- **2019** — Google estima 20M qubits para romper ECDSA-256.
- **2022** — Comienza la finalización de los estándares NIST PQ.
- **Agosto 2024** — Publicación oficial de FIPS 203, 204, 205.
- **Octubre 2024** — NIS2 entra en vigor en la UE.
- **Diciembre 2024** — MiCA entra en vigor en la UE.
- **Mayo 2025** — Google revisa su estimación a 1M qubits.
- **Noviembre 2025** — Investigadores alemanes teleportan información cuántica sobre fibra comercial (Nature).
- **Enero 2026** — Jefferies reduce 10% de Bitcoin en carteras modelo por riesgo cuántico.
- **Marzo 2026** — Google publica estimación <500K qubits.
- **Marzo 2026** — Caltech + Atomic publican arquitectura con 10.000 qubits.
- **Marzo 2026** — Google adelanta su plazo interno de migración a 2029.
- **Abril 2026** — Giancarlo Lelli gana el Q-Day Prize rompiendo ECC-15 en cuántico público.
- **Marzo 2026** — ACM anuncia el A.M. Turing Award 2025 para Bennett y Brassard.
- **Mayo 2026** — QRB inicia Fase 0.

### C. Referencias clave

- NIST FIPS 203 (ML-KEM), 204 (ML-DSA), 205 (SLH-DSA), 206 (FN-DSA). Agosto 2024.
- Reglamento (UE) 2023/1114 MiCA.
- Directiva (UE) 2022/2555 NIS2.
- Buterin, V. et al., *Account Abstraction via Entry Point Contract Specification (ERC-4337)*.
- Optimism Bedrock specifications.
- Bennett, C. H., & Brassard, G. (1984). *Quantum cryptography: Public key distribution and coin tossing*. Proc. IEEE International Conference on Computers, Systems and Signal Processing.
- Shor, P. (1994). *Algorithms for quantum computation: discrete logarithms and factoring*.
- Google Quantum AI (2026). Estimaciones revisadas de qubits para romper ECDSA-256.
- Project Eleven, *Q-Day Prize* (abril 2026).
- Post-Quantum Cryptography Coalition (MITRE et al.), *PQC Migration Roadmap* (mayo 2025).
- Documentación técnica de CRYSTALS-Dilithium, FALCON y SPHINCS+.
- StarkWare Cairo specifications.
- Bit2Me Academy, *Los mayores robos de Bitcoin y criptomonedas de la historia*.

---

*Este documento es un borrador (v0.2) abierto a revisión técnica y económica. Comentarios, correcciones y propuestas de colaboración son bienvenidos en el repositorio público de QRB.*

*Open source · MIT / Apache-2.0*
