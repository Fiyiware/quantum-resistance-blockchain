# QRB — Quantum-Resistance Blockchain
## Whitepaper técnico-económico
**Versión 0.1 · Borrador inicial · Mayo 2026**

> ⚠️ **DOCUMENTO OBSOLETO — superado por la v0.2.** Esta es la primera versión, conservada solo como histórico. La versión vigente es [`whitepaper-v0.2.md`](whitepaper-v0.2.md) (español) · [`whitepaper-v0.2.en.md`](whitepaper-v0.2.en.md) (English).

---

## Resumen ejecutivo

QRB (Quantum-Resistance Blockchain) es una blockchain de capa 2 (L2) construida sobre Ethereum, diseñada para ser resistente a ataques con ordenadores cuánticos desde el primer bloque. Mientras que el resto del ecosistema cripto —Bitcoin, Ethereum, Solana, BNB Chain y prácticamente todas las cadenas relevantes— sigue dependiendo de firmas digitales (ECDSA, EdDSA, Schnorr) que un ordenador cuántico criptográficamente relevante podrá romper en cuestión de horas, QRB sustituye esa primitiva por esquemas post-cuánticos ya estandarizados por el NIST en 2024 (CRYSTALS-Dilithium / ML-DSA, FALCON / FN-DSA, SPHINCS+ / SLH-DSA) manteniendo compatibilidad total con la Máquina Virtual de Ethereum (EVM).

QRB se diferencia de los pocos proyectos post-cuánticos existentes (QRL, Quranium, Cellframe, Naoris) en cuatro puntos clave:

1. **Hereda la seguridad y la liquidez de Ethereum** vía un *bridge* nativo seguro, evitando el problema crítico de cualquier L1 nueva: arrancar una red de validadores y atraer capital desde cero.
2. **Es compatible con la EVM y las herramientas existentes** (Hardhat, Foundry, MetaMask con adaptador PQ), reduciendo a casi cero la barrera de entrada para los desarrolladores de Solidity.
3. **Implementa abstracción de cuenta (Account Abstraction) post-cuántica desde el primer día**, ocultando al usuario final la complejidad y el tamaño de las firmas PQ.
4. **Sigue una hoja de ruta de financiación responsable y legalmente sólida**: primero subvenciones públicas (NLNet, Ethereum Foundation, Optimism RetroPGF), luego comunidad y, solo cuando exista producto demostrable, una emisión de token registrada bajo MiCA.

Este documento describe el problema, la solución técnica, el modelo económico, la gobernanza, el *roadmap* y los riesgos del proyecto. Está dirigido a desarrolladores, posibles colaboradores técnicos, comités evaluadores de subvenciones y, en una fase posterior, a inversores institucionales.

---

## 1. El problema

### 1.1 La amenaza cuántica al consenso criptográfico

Toda la criptografía de clave pública que sostiene la economía digital actual —HTTPS, banca en línea, firmas digitales, blockchain— depende de dos suposiciones matemáticas: la **dificultad de factorizar enteros grandes** (RSA) y la **dificultad del logaritmo discreto en curvas elípticas** (ECDSA, EdDSA, Schnorr). En 1994, Peter Shor demostró que un ordenador cuántico de tamaño suficiente puede resolver ambos problemas en tiempo polinómico. No es una conjetura: es matemática demostrada.

Lo que no se sabe con precisión es **cuándo** existirá un ordenador cuántico criptográficamente relevante (CRQC, por sus siglas en inglés). Las estimaciones más conservadoras, recogidas por el Global Risk Institute en su informe anual *Quantum Threat Timeline*, sitúan la probabilidad de aparición de un CRQC entre **15% y 30% para 2033, y por encima del 50% para 2040**. IBM, Google y empresas como PsiQuantum han publicado *roadmaps* concretos hacia ordenadores con miles a millones de qubits físicos en la próxima década.

Cuando un CRQC exista, **cualquier dirección de blockchain cuya clave pública haya sido expuesta** —es decir, toda dirección desde la que se haya enviado alguna vez una transacción— podrá ser comprometida. Esto incluye los más de 4 millones de Bitcoin en direcciones P2PK y P2PKH reutilizadas, billones de dólares en Ethereum, prácticamente todos los contratos inteligentes existentes, y la totalidad del estado de las L2 actuales.

### 1.2 "Harvest now, decrypt later"

El riesgo no es solo futuro. Existe la práctica documentada de **"cosecha ahora, descifra después"**: actores estatales y privados están almacenando hoy comunicaciones cifradas y transacciones blockchain con el plan de descifrarlas cuando dispongan de capacidad cuántica. Las transacciones blockchain, al ser **públicas y permanentes**, son especialmente vulnerables a esta estrategia: cualquier firma ECDSA emitida hoy estará disponible para ataque retrospectivo cuando exista un CRQC.

### 1.3 El gap regulatorio se está cerrando

Los reguladores ya están actuando:

- **NIST** publicó en agosto de 2024 los estándares FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) y FIPS 205 (SLH-DSA), marcando oficialmente el inicio de la era post-cuántica.
- **ANSSI** (Francia) y **BSI** (Alemania) exigen migración a criptografía post-cuántica para sistemas críticos antes de 2030.
- **NIS2** (Directiva europea de ciberseguridad, vigente desde octubre 2024) incluye explícitamente la resistencia cuántica como criterio de diligencia.
- **CNSA 2.0** (Estados Unidos, NSA) ordena la transición completa a PQ para sistemas clasificados antes de 2035.

Las cadenas que no se adapten quedarán **fuera de uso institucional**, perdiendo el segmento más rentable del mercado (custodia institucional, *tokenización* de activos reales, *settlement* interbancario).

### 1.4 El problema secundario: las L1 grandes no pueden migrar fácilmente

Bitcoin, Ethereum y similares **no pueden simplemente "cambiar de firma"**: una migración implica un *hard fork* coordinado entre miles de validadores y millones de usuarios, decidir qué hacer con las claves perdidas o no migradas, y un proceso político de años. Ethereum tiene PQ en su *roadmap* a largo plazo, pero realísticamente no estará migrada antes de 2030-2032. Es ahí donde existe una ventana clara para un proyecto que **nazca post-cuántico**.

---

## 2. Estado del arte

### 2.1 Proyectos existentes y sus limitaciones

| Proyecto | Esquema PQ | Estado | Limitación principal |
|----------|------------|--------|----------------------|
| QRL (Zond) | XMSS → Dilithium (en migración) | Mainnet desde 2018, EVM en testnet | UX deficiente, ecosistema mínimo, baja capitalización |
| Quranium | Dilithium | Testnet 2025 | Comunidad pequeña, sin tracción de devs |
| Cellframe | CRYSTALS, NTRU | Mainnet | Arquitectura compleja, *fork* difícil |
| Naoris Protocol | Híbrido | Pre-mainnet | Más mesh de seguridad que blockchain general |
| IOTA (clásico) | Winternitz | Mainnet (transición a EdDSA) | Abandonó PQ por problemas de UX |

Ninguno de los anteriores combina:
- **EVM-compatibilidad real** (Solidity directo, sin reescritura).
- **Account abstraction PQ** transparente para el usuario.
- **Bridge productivo a Ethereum** que aporte liquidez.
- **Tooling de desarrollador maduro** (SDKs, *explorer*, faucet, docs).

Ese es el hueco que QRB busca ocupar.

### 2.2 ¿Por qué L2 y no L1?

Una L1 propia obliga a resolver el problema de los **incentivos de validador**: convencer a operadores de nodos a destinar hardware y capital, lo cual exige una emisión inflacionaria significativa de token nativo y captación de comunidad. Para un proyecto que no parte de un fondo de 20-50 millones de euros, esto es prohibitivo y conduce históricamente a redes inseguras los primeros 1-3 años.

Una L2 sobre Ethereum, en cambio:
- **Hereda la seguridad** del *settlement layer* de Ethereum (más de 30 mil millones de USD asegurando consenso).
- **Hereda la liquidez** vía *bridges* establecidos.
- **Reduce el coste inicial** a un factor 10× respecto a una L1.
- **Permite enfocarse en lo diferencial** (la criptografía PQ y la UX) en vez de gastar recursos reinventando consenso.

---

## 3. Solución técnica

### 3.1 Pila criptográfica

QRB adopta los estándares NIST post-cuánticos como base:

- **Firmas digitales primarias**: ML-DSA (CRYSTALS-Dilithium), específicamente **ML-DSA-65** como *default* (equivalente a 192 bits de seguridad clásica, ~2,5 KB de firma, ~1,3 KB de clave pública).
- **Firmas alternativas opt-in**: FN-DSA (FALCON) para casos que requieran firmas más compactas (~700 B) a costa de complejidad de generación, y SLH-DSA (SPHINCS+) para escenarios de máxima conservadurismo basados en hash.
- **Intercambio de claves**: ML-KEM (CRYSTALS-Kyber), específicamente ML-KEM-768, para cualquier capa de comunicación cifrada entre nodos.
- **Hash**: Keccak-256 (compatibilidad EVM) y SHA3-512 disponible como precompilado para aplicaciones que requieran margen post-cuántico explícito (Grover reduce la seguridad efectiva a la raíz cuadrada).

### 3.2 Firmas híbridas durante la transición

Durante los primeros 24 meses de mainnet, QRB ofrecerá un modo **firma híbrida** opcional: cada transacción puede ir firmada simultáneamente con ECDSA-secp256k1 (para compatibilidad con *wallets* y *bridges* legados) y con ML-DSA. La transacción solo se considera válida si **ambas** firmas lo son. Este mecanismo permite a usuarios migrar progresivamente sin requerir un *cutover* abrupto, y mitiga el riesgo de bugs en implementaciones jóvenes de PQ.

### 3.3 Abstracción de cuenta (Account Abstraction) PQ

Las firmas PQ son significativamente más grandes que ECDSA (Dilithium ~2,5 KB vs. 64 bytes). Para evitar que esto degrade la experiencia del usuario, QRB implementa **Account Abstraction nativa** (ERC-4337-like) desde el primer bloque:

- Cada cuenta es un contrato inteligente con su propia lógica de validación de firmas.
- Las firmas PQ se verifican vía **precompilado** dedicado en el cliente de ejecución, con coste de gas estable y predecible.
- Los usuarios pueden definir **rotación de claves**, **recuperación social**, **paymasters** (un tercero paga el gas), **multifirma PQ** y **firma delegada** sin cambios en el protocolo.
- Las direcciones se derivan del **hash** de la clave pública, no de la clave pública en sí, permitiendo que esta permanezca oculta hasta el primer gasto (igual que Bitcoin moderno).

### 3.4 EVM-compatibilidad

La capa de ejecución de QRB es un *fork* del cliente Reth (Rust) o Geth (Go) modificado para:

- Reemplazar el opcode de validación de firma ECRECOVER por MLDSAVERIFY (validación ML-DSA) en transacciones nativas.
- Añadir precompilados en `0x100`-`0x103` para ML-DSA-44, ML-DSA-65, ML-DSA-87 y FN-DSA-512 respectivamente.
- Mantener todos los opcodes EVM estándar inalterados para que cualquier contrato Solidity existente compile y se ejecute sin cambios.
- Mantener ECRECOVER funcional para *bridges* y compatibilidad histórica, pero marcado como obsoleto en herramientas oficiales.

Un desarrollador que migre desde Ethereum solo necesita: (1) reemplazar las llamadas a `ecrecover()` por `dsarecover()` en sus contratos si valida firmas off-chain; (2) generar wallets PQ. Todo lo demás —ABI, Solidity, herramientas— funciona idéntico.

### 3.5 Bridge a Ethereum

El *bridge* es el componente más crítico de seguridad de cualquier L2. QRB adopta el modelo **optimistic rollup** del OP Stack (Optimism) en su versión actual, con dos modificaciones:

- Las firmas de los proponedores y verificadores del *rollup* son PQ desde el día 1.
- El periodo de impugnación (*challenge period*) se mantiene en 7 días, alineado con Optimism.

A medio plazo (Fase 2+), se evaluará migración a un modelo **ZK-rollup** una vez existan probadores SNARK eficientes para firmas Dilithium (investigación activa en 2026).

---

## 4. Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                  Capa de Aplicación                          │
│  (DApps, DeFi, NFTs, identidad PQ, tokenización RWA)         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│           Capa de Cuenta (Account Abstraction PQ)             │
│  Wallets contractuales · Rotación de claves · Multisig PQ     │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│              Capa de Ejecución (EVM + Precompilados PQ)       │
│  Reth fork · MLDSAVERIFY · ML-DSA / FN-DSA / SLH-DSA precomps  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│       Capa de Disponibilidad de Datos y Settlement            │
│  Calldata en Ethereum (Fase 1) → EIP-4844 blobs (Fase 2)      │
│  Pruebas de fraude PQ · Bridge optimista                      │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                Ethereum L1 (settlement & DA)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Tokenomics

### 5.1 El token QRB

El token nativo del ecosistema se denominará **QRB**. Sus funciones son:

- **Pago de gas**: todas las transacciones en la red QRB se pagan en QRB.
- **Staking** para secuenciadores y verificadores descentralizados (Fase 2+).
- **Gobernanza** del protocolo (Fase 2+).
- **Acceso a servicios** del ecosistema (despliegue de tokens, *naming service*, etc.).

### 5.2 Suministro total y distribución

Suministro fijo (no inflacionario): **1.000.000.000 QRB**.

| Categoría | % | Cantidad | Vesting / Desbloqueo |
|-----------|---|----------|----------------------|
| Fundador y equipo inicial | 15% | 150.000.000 | *Cliff* 12 meses, vesting lineal 36 meses adicionales |
| Tesorería de la Fundación | 20% | 200.000.000 | Desbloqueada por gobernanza, ritmo máx. 2%/mes |
| Validadores / Stakers (recompensas) | 30% | 300.000.000 | Emisión gradual durante 10 años |
| Ecosistema y subvenciones a desarrolladores | 25% | 250.000.000 | Desbloqueada por gobernanza para grants, hackathons, integraciones |
| Liquidez inicial y oferta pública | 10% | 100.000.000 | Solo activada cuando exista mainnet operativa, sujeta a registro MiCA |

**Diseño explícitamente conservador**: 15% de fundador con vesting largo está por debajo del estándar de la industria (que suele oscilar entre 18-25%) precisamente para no levantar señales de centralización ni espantar a inversores ni a comités de grants.

### 5.3 Fees del protocolo

Los gastos de gas siguen el modelo EIP-1559:

- **Base fee**: quemada (deflacionaria sobre el suministro circulante).
- **Priority fee**: para el secuenciador / proponedor.
- **Protocol fee**: un **15% adicional** sobre el priority fee, dirigido a la tesorería del protocolo para sostener desarrollo, auditorías y subvenciones a largo plazo.

### 5.4 Captura de valor del ecosistema

Cualquier token desplegado en QRB (ERC-20-PQ, ERC-721-PQ, etc.) paga:

- Un **fee fijo de despliegue** en QRB (~5-50 QRB según tipo).
- Las transferencias y operaciones consumen gas en QRB.

Esto crea demanda orgánica de QRB conforme crece el ecosistema, **sin extraer valor de los tokens desplegados por terceros** (lo cual sería tóxico para la adopción).

---

## 6. Gobernanza

QRB seguirá un modelo de gobernanza **progresivamente descentralizada**:

- **Fase 0-1**: gobernanza centralizada en la Fundación QRB (entidad jurídica a constituir, probablemente en España o Suiza), con decisiones técnicas tomadas por el equipo core y publicadas abiertamente.
- **Fase 2**: introducción de propuestas on-chain (QRB Improvement Proposals, QIPs) vinculantes para parámetros del protocolo (gas, fees, tesorería).
- **Fase 3+**: gobernanza completamente on-chain con poder de veto residual de la Fundación para emergencias de seguridad, con plan explícito de eliminación de ese veto tras 5 años de mainnet estable.

---

## 7. Seguridad

### 7.1 Modelo de amenazas

QRB se diseña frente a un atacante con:

- Recursos computacionales cuánticos limitados pero crecientes (CRQC potencial a partir de 2030-2035).
- Capacidad de "cosecha ahora, descifra después" sobre el historial público de la cadena.
- Control de hasta 33% del *stake* (asunción estándar BFT).
- Acceso completo al código fuente (todo el proyecto es open source MIT).

### 7.2 Auditorías y verificación

Antes de mainnet (Fase 2):

- **Auditoría criptográfica** del módulo de firmas PQ por una firma especializada (Trail of Bits, Least Authority o similar). Coste estimado: 60.000-120.000 €.
- **Auditoría EVM** del cliente de ejecución modificado. Coste estimado: 50.000-100.000 €.
- **Auditoría del bridge** (componente crítico). Coste estimado: 80.000-150.000 €.
- **Verificación formal** de las precompilaciones PQ con Coq o Lean (objetivo a 24 meses).
- Programa de **bug bounty** con techo de 500.000 QRB para fallos críticos.

### 7.3 Plan de emergencia

Multifirma de emergencia (5 de 9, Fundación + figuras externas reputadas del ecosistema) con poder de **pausa del bridge** durante 72 horas máximo. No tiene poder sobre el estado de la cadena ni sobre los fondos de usuarios.

---

## 8. Roadmap

| Fase | Periodo | Hitos | Presupuesto estimado |
|------|---------|-------|----------------------|
| **Fase 0 — Validación** | Q2-Q3 2026 | Whitepaper v1.0 · Prototipo en Rust (firmas Dilithium + bloques + tx) · GitHub público · Landing · Comunidad embrionaria | 0-2.000 € (autofinanciado) |
| **Fase 1 — Testnet pública** | Q4 2026 - Q3 2027 | Solicitud y obtención de grants (NLNet objetivo: 30-50K €) · Devnet interna · Testnet pública incentivada · Faucet · Explorer · SDK JS/Rust · Primeras 5-10 dApps demo | 50.000-150.000 € (vía grants) |
| **Fase 2 — Mainnet beta** | Q4 2027 - Q2 2028 | Auditorías completas · Bridge productivo · Token QRB emitido bajo MiCA · Lanzamiento exchanges descentralizados · 50+ contratos desplegados | 500.000-1.500.000 € (seed round o token launch regulado) |
| **Fase 3 — Mainnet GA** | H2 2028+ | Descentralización del secuenciador · Gobernanza on-chain · Integraciones con custodios institucionales · Migración optimista → ZK-rollup | Autosostenible vía fees |

---

## 9. Equipo y colaboradores

**Fundador**: [Nombre — completar]. Visión de producto, dirección estratégica y representación pública del proyecto.

**Colaboradores buscados activamente** (Fase 0):

- 1 desarrollador Rust/Go con experiencia en clientes blockchain (Geth, Reth, Erigon).
- 1 criptógrafo o estudiante de doctorado con conocimiento de retículos / Dilithium.
- 1 desarrollador frontend para *wallet* y explorer.
- 1 *technical writer* / comunicador en español e inglés.

El proyecto es desde su origen **open source y abierto a contribuciones**. Cualquier *contributor* significativo recibirá una asignación de la categoría "Ecosistema y subvenciones a desarrolladores" en términos a definir por la Fundación.

---

## 10. Financiación

### 10.1 Estrategia general

QRB sigue una estrategia de financiación **escalonada y conservadora**, evitando deliberadamente el modelo de "token primero, producto después" que caracterizó al ciclo ICO de 2017-2018 y que actualmente está penalizado tanto por regulación (MiCA, SEC) como por reputación.

### 10.2 Fuentes por fase

**Fase 0** — autofinanciación (~1.000 € del fundador, tiempo de colaboradores).

**Fase 1** — subvenciones (no dilutivas):

- **NLNet / NGI Zero Commons Fund** (Comisión Europea) — financiación de infraestructura criptográfica abierta. Tramos típicos: 5.000-50.000 €. Encaje perfecto para PQ-cripto. Primera prioridad.
- **Ethereum Foundation Ecosystem Support** — *grants* de investigación e *tooling*.
- **Optimism RetroPGF / Arbitrum Foundation** — bienes públicos sobre OP Stack.
- **Web3 Foundation** (Polkadot) — investigación criptográfica.
- **NIST Post-Quantum programs** — investigación pura aplicada.

**Fase 2** — combinación de:

- Ronda *seed* con inversores enfocados en infraestructura cripto y/o seguridad cuántica.
- Emisión pública del token QRB, registrada formalmente bajo **MiCA** mediante whitepaper notificado a la CNMV, con asesoramiento legal especializado (presupuesto previsto: 5.000-15.000 € en honorarios legales).

**Fase 3+** — autosostenible vía protocol fees + tesorería.

---

## 11. Riesgos y mitigaciones

| Riesgo | Impacto | Probabilidad | Mitigación |
|--------|---------|--------------|------------|
| El ML-DSA es comprometido por avance criptoanalítico | Catastrófico | Baja | Plan de migración a SLH-DSA (hash-based, más conservador) preestablecido. Modularidad del módulo de firma desde día 1. |
| Ethereum acelera su migración PQ y absorbe la propuesta de valor | Alto | Media | QRB se posiciona como el espacio "PQ-first" mientras Ethereum migra (proceso de mínimo 4-7 años). Cuando Ethereum migre, QRB ya tendrá ecosistema y puede pivotar a especialización (RWA institucional, identidad). |
| No se obtienen grants en Fase 1 | Alto | Media-Baja | Estrategia paralela: NLNet + EF + Optimism simultáneamente. Probabilidad combinada de obtener al menos uno: >70%. Si todos fallan, Fase 1 se ejecuta en versión reducida ($5-10K propios). |
| Cambios regulatorios MiCA endurecen requisitos | Medio | Alta | Asesoría legal continua. Modelo de token utilidad puro (no security). Disposición a registrar como CASP si fuera necesario. |
| Bug crítico en el bridge | Catastrófico | Baja-Media | Auditorías múltiples antes de mainnet. Modo *withdrawal-only* de emergencia. Seguro de protocolo (Nexus Mutual o similar) para Fase 2+. |
| El fundador no consigue dedicación a tiempo completo | Medio | Media | El proyecto está diseñado para ser dirigible con dedicación parcial en Fase 0-1. Una vez obtenido el primer grant, dedicación se vuelve fulltime. |

---

## 12. Conclusión

QRB no aspira a sustituir a Ethereum ni a Bitcoin. Aspira a ser **la red por defecto cuando una organización, un protocolo o un usuario necesiten garantías post-cuánticas**: cuando una entidad financiera regulada necesite custodiar activos con compliance NIS2; cuando un protocolo de identidad necesite firmas digitales válidas a 30 años vista; cuando un usuario quiera proteger su patrimonio del riesgo de "cosecha ahora, descifra después".

El proyecto combina:

- Un **problema real y creciente** (la amenaza cuántica documentada por NIST, ANSSI, BSI).
- Una **solución técnica sólida** (estándares post-cuánticos ya disponibles, sin dependencia de investigación futura).
- Una **estrategia de mercado realista** (L2 sobre Ethereum, no L1 desde cero).
- Una **financiación conservadora y legal** (grants → producto → token regulado, no al revés).
- Un **equipo abierto y modesto** que prioriza la ejecución sobre el *hype*.

La invitación está abierta a desarrolladores, criptógrafos, evaluadores de subvenciones y, en su momento, inversores: este es el momento adecuado para construir la infraestructura criptográfica que el mundo necesitará en la próxima década.

---

## Apéndices

### A. Glosario abreviado

- **CRQC**: Cryptographically Relevant Quantum Computer. Ordenador cuántico de tamaño suficiente para romper criptografía asimétrica clásica.
- **ML-DSA**: Module-Lattice Digital Signature Algorithm (estándar NIST FIPS 204, derivado de CRYSTALS-Dilithium).
- **FN-DSA**: FFT over NTRU Digital Signature Algorithm (derivado de FALCON).
- **SLH-DSA**: Stateless Hash-based Digital Signature Algorithm (FIPS 205, derivado de SPHINCS+).
- **ML-KEM**: Module-Lattice Key Encapsulation Mechanism (FIPS 203, Kyber).
- **L2 / Rollup**: capa de escalado construida sobre Ethereum que ejecuta transacciones fuera de cadena y deposita pruebas o datos en Ethereum.

### B. Referencias clave (a completar en v1.0)

- NIST FIPS 203, 204, 205 (agosto 2024).
- Global Risk Institute, *Quantum Threat Timeline Report*, ediciones 2023-2025.
- Reglamento (UE) 2023/1114 MiCA.
- Buterin, V. et al., *Account Abstraction via Entry Point Contract Specification (ERC-4337)*.
- Optimism Bedrock specifications.
- Documentación técnica de CRYSTALS-Dilithium y FALCON.

---

*Este documento es un borrador inicial (v0.1) abierto a revisión técnica y económica. Comentarios, correcciones y propuestas de colaboración son bienvenidos en el repositorio público de QRB.*
