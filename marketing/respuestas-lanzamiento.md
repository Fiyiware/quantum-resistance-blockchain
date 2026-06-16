# QRB — Banco de respuestas para el lanzamiento

Respuestas listas para copiar-pegar durante las primeras horas del hilo.
Tono: honesto, técnico, sin defensividad. Los devs detectan el "humo" al instante —
nuestra ventaja es que NO inflamos nada.

Regla de oro: si no sabes algo, di "buena pregunta, aún no está resuelto, está en
Fase X" — eso da MÁS credibilidad que improvisar.

---

## 🔬 Preguntas técnicas duras (las que más importan)

**"Las firmas ML-DSA-65 / Dilithium ocupan ~3 KB. Eso multiplica el coste y mata el throughput de una L2."**
> Cierto, es el mayor trade-off de la criptografía post-cuántica. Por eso justamente una L2: el coste de la firma se amortiza en el batch y la prueba que se publica en L1. Estamos estudiando agregación de firmas para reducirlo más. No lo escondo: es el precio de sobrevivir al cuántico, y lo asumimos con los ojos abiertos.

**"Los STARKs se apoyan en hashes. Grover da speedup cuántico sobre hashes, así que tampoco son 100% PQ."**
> Exacto, y por eso es importante el detalle: Grover solo da una aceleración cuadrática, que se neutraliza doblando el tamaño de salida del hash (p.ej. 256 bits de seguridad efectiva). Es el enfoque estándar y aceptado por NIST. Los STARKs siguen siendo PQ-seguros bajo ese ajuste; los SNARKs basados en emparejamientos, no — esos caen del todo con Shor.

**"La criptografía de retículos (lattices) también podría romperse algún día."**
> Es una posibilidad real y honesta. Ningún esquema tiene prueba de seguridad absoluta. Por eso la estrategia es defensa en capas: PQ matemática (retículos) HOY + QKD físico como capa adicional a largo plazo. Si un día cae una, la otra aguanta. No apostamos todo a un solo caballo.

**"¿Por qué no usar el propio roadmap PQ de Ethereum (account abstraction, EIP-7560) en vez de una cadena nueva?"**
> Lo usaremos cuando llegue — somos L2, heredamos de Ethereum. Pero la migración PQ de L1 son 4-7 años (lo dice la propia EF). QRB cubre ese hueco temporal para quien no puede esperar: RWA tokenizado, custodios, compliance. Complementamos, no competimos con Ethereum.

**"QKD necesita fibra dedicada y hardware especial. No es práctico para una blockchain."**
> Totalmente de acuerdo, y por eso es **Fase 3+ y para casos institucionales**, no para el usuario de a pie. La red MadQCI de Telefónica (validada en Nature, 2024) ya conecta nodos en Madrid por fibra. La visión es que custodios e instituciones con esa infraestructura puedan asegurar claves con QKD. No prometemos QKD en tu móvil — sería mentira.

**"STARKs son demasiado pesados para producción."**
> Lo eran. Plonky3 (Polygon) y los avances de StarkWare 2024-2026 han bajado el coste ~10×. Aun así, lo ponemos en Fase 3+ por prudencia. El roadmap es escalonado precisamente para no prometer lo que hoy no es viable.

**"El ataque de '9 minutos' es teórico, las claves rotas son de 15 bits."**
> Correcto, y lo digo en el propio hilo: hoy son claves pequeñas. El punto no es que tu wallet caiga mañana — es la **trayectoria**: 6 bits en sept 2025, 15 bits en abril 2026. Migrar criptografía a escala global lleva años. Por eso se empieza antes de que sea tarde, no después.

---

## 🤨 Escépticos / "vaporware"

**"Otro proyecto vaporware más."**
> Whitepaper técnico + prototipo funcional en GitHub público, MIT. Cero ICO, cero token. Si te parece humo, abre el código y dime qué falla — te lo agradezco de verdad.

**"Solo tienes 4 seguidores / acabas de empezar."**
> Cierto, es el día 1. Júzgame por el código y el whitepaper, no por el contador de seguidores. Todo proyecto serio empezó en cero.

**"Esto lo ha escrito una IA."**
> Uso asistencia de IA y está declarado abiertamente en el README. Las decisiones de diseño, la criptografía y la dirección son mías y son verificables en el código. La transparencia sobre las herramientas es parte del proyecto.

**"No hay equipo, eres tú solo."**
> Fase 0, y lo digo sin maquillar: busco co-fundador técnico (Rust/Go, criptógrafo). Prefiero ser honesto sobre dónde estoy que fingir un equipo que no existe. DMs abiertos.

**"¿Por qué confiaría mi dinero a una cadena nueva?"**
> No deberías — y no te lo pido. No hay token, no hay mainnet, no hay nada que comprar. Es investigación en fase temprana, abierta. Si algún día hay producto, lo evaluarás entonces.

---

## ⚔️ Comparación con competidores

**"QRL ya hace esto."**
> QRL hace firmas PQ, no privacidad PQ, y su compatibilidad EVM es parcial y reciente. QRB busca cubrir los tres ejes — auth PQ + privacidad PQ + EVM nativa — que ningún proyecto combina hoy.

**"¿En qué te diferencias de Aleo / Aztec?"**
> Aleo y Aztec son excelentes en privacidad, pero sus SNARKs usan emparejamientos de curvas que Shor rompe. Su privacidad protege hoy, no a 30 años. QRB apunta a privacidad con STARKs, que sí resisten al cuántico. Es una diferencia de horizonte temporal, no de calidad de su trabajo.

**"Quranium / otros ya lo están haciendo."**
> Hay varios proyectos PQ y es buena señal: el problema es real. Cada uno toma un enfoque distinto. El de QRB es L2 sobre Ethereum (no L1 nueva) + las dos capas de defensa. Cuantos más construyamos, mejor para todos.

---

## 🏛️ Negocio / regulación / financiación

**"¿Cómo vas a ganar dinero / cuándo el token?"**
> Orden estricto: grants no dilutivos primero (Ethereum Foundation, NLnet, Optimism) → producto + comunidad → solo entonces token, registrado bajo MiCA. Nunca token antes de producto. La sostenibilidad viene del valor, no de la especulación.

**"Ethereum va a migrar a PQ, no os necesita."**
> Cierto, y es bueno para todos. Pero la EF estima 4-7 años para migrar L1. QRB cubre ese hueco para quien no puede esperar: RWA, custodios institucionales, compliance NIS2/MiCA.

**"15% para el fundador es mucho."**
> Es estándar de industria (10-25%), con cliff de 12 meses y vesting de 36 más. Nada vendible el día 1. Diseñado para alinear incentivos a largo plazo.

**"¿Esto es legal? ¿MiCA?"**
> El planteamiento es PQ-compliant by design: cualquier token futuro se registraría bajo MiCA, y la arquitectura contempla requisitos de NIS2 sobre resiliencia criptográfica. La regulación no es un obstáculo, es parte del diseño.

---

## 🛟 Comodines (cuando no sabes la respuesta)

- "Muy buena pregunta — no está resuelto todavía, está en Fase X del roadmap. ¿Te interesa el problema? Hablemos por DM."
- "No lo sé con certeza y prefiero no inventarme una cifra. Lo miro y te respondo con la fuente."
- "Tienes razón en eso, es una limitación conocida. Así lo planteamos en el whitepaper, sección X."
- (Para trolls) Un like y seguir. No alimentar. La comunidad técnica valora más una respuesta sólida a un escéptico de buena fe que diez peleas.

---

*Actualizar tras el lanzamiento con las preguntas reales que vayan saliendo.*
