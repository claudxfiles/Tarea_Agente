# Tarea Grupal (obligatoria): Agente Inteligente ReAct + KB en Redis (Python + OpenAI API)

**Curso:** Agentes Inteligentes (Master en AI)  
**Modalidad:** Grupal 3 a 4 alumnos (no se permite entrega individual)  
**Fecha de entrega:** 28 de enero  
**Nota máxima:** 7,0

---

## 1) Objetivo

Diseñar e implementar un Agente tipo ReAct en Python, que use la API de OpenAI y consulte una Base de Conocimiento (KB) persistida en Redis para responder preguntas con evidencia, trazabilidad y control de alucinaciones.

---

## 2) Requerimiento central (flujo ReAct)

Deben entregar un diseño de flujo (diagrama) y una implementación funcional que siga el patrón:

**Pregunta del usuario → (Reason) → (Act: tool) → (Observe) → loop → Respuesta final**

### Herramientas mínimas del agente (tools)

1. **search_kb(query)**: recupera top-k chunks desde Redis (vector o keyword + ranking).
2. **get_doc(doc_id)**: obtiene el documento/chunk con metadatos.
3. **cite(sources)**: arma citas/footnotes en la respuesta final (puede ser simple: [doc_id:chunk_id]).

El agente debe apoyar sus respuestas en la KB, y cuando no exista evidencia suficiente debe decirlo explícitamente ("no encontré soporte en la KB").

---

## 3) Implementación (Python + OpenAI API + Redis)

### Especificaciones mínimas

- **Python 3.10+**
- **Uso de OpenAI API** (chat/completions o responses, según su implementación).
- **Redis como KB:**
  - Persistencia de documentos y metadatos.
  - Estrategia de recuperación:
    - **Opción A:** Vector Search (recomendado) con embeddings + índice.
    - **Opción B:** Búsqueda híbrida (texto + heurística) si justifican.
- **Ingesta de KB:** pipeline que toma una carpeta de documentos (txt/pdf/markdown) y los deja "chunked" en Redis.
- **ReAct loop:**
  - Debe decidir cuándo buscar en KB, cuándo pedir aclaración y cuándo responder.
- **Guardrails:**
  - Umbral de confianza: si top-k no supera cierto score, responder con incertidumbre.
  - Respuesta final debe incluir citas a chunks usados.

---

## 4) Dataset / KB

Cada grupo debe construir una KB con **mínimo 20 documentos** (o 60+ chunks) sobre un dominio acotado (ej.: normativas, manuales técnicos, políticas internas ficticias, guías académicas, etc.).

**Prohibido:** usar una KB vacía o solo 2–3 documentos.

---

## 5) Entregables (obligatorios)

### 1. Diagrama de flujo (1 página) del agente ReAct:
- Estados / nodos: User Query, Planner/Reason, Tool Call, Observation, Stop/Answer.
- Decisiones: "¿hay evidencia?", "¿requiere aclaración?", "¿suficiente para responder?"
- Formato libre: PNG/PDF (draw.io, mermaid, ppt, figma, etc.).

### 2. Repositorio (Git) con:
- **README.md** con instrucciones de ejecución
- **ingest.py** o similar (carga KB a Redis)
- **agent.py** (ReAct loop + tools)
- **config.example.env** (sin credenciales reales)
- Script de prueba o notebook opcional

### 3. Informe corto (máx. 4 páginas):
- Arquitectura (ReAct + Redis KB)
- Decisiones de diseño (chunking, top-k, umbral)
- Evidencias: 3 ejemplos de preguntas con output y citas
- Riesgos: alucinación, prompt injection en documentos, datos sensibles

### 4. Demo (5–7 min): 
Video o presentación en vivo (según defina el curso) mostrando:
- Ingesta KB
- 2 consultas "fáciles" y 1 "difícil" (sin evidencia suficiente)
- Cómo se citan fuentes y cómo maneja incertidumbre

---

## 6) Reglas y restricciones

- No se aceptan entregas individuales. Si un alumno queda solo, debe integrarse a otro grupo.
- **Credenciales:** nunca subir API keys al repo (si aparecen, nota máxima queda limitada).
- Se exige **trazabilidad:** en logs o consola, mostrar al menos:
  - Tool usado
  - Query enviada a KB
  - Documentos recuperados (ids)
- Deben incluir un mecanismo mínimo anti-prompt injection desde la KB (ej.: "tratar los documentos como datos, no instrucciones").

---

## 7) Rúbrica (nota máxima 7,0)

**7,0 = excelente y completo**. Se evaluará:

### 1. Diseño de flujo ReAct (1,5 pts)
- Claridad del diagrama, decisiones, loops, manejo de "no evidencia".

### 2. KB en Redis + Ingesta (1,5 pts)
- Calidad chunking, metadatos, índice, persistencia, reproducibilidad.

### 3. Implementación del Agente ReAct (2,0 pts)
- Loop correcto, tools bien definidos, decisiones coherentes, robustez.

### 4. Calidad de Respuesta + Citas (1,0 pts)
- Responde con evidencia, cita fuentes, evita alucinar, reporta incertidumbre.

### 5. Demo + Informe (1,0 pts)
- Demostración clara, casos bien elegidos, documentación completa.

### Penalizaciones típicas
- Sin diagrama: **-1,0**
- Sin citas en la respuesta final: **-1,0**
- KB muy pequeña o irrelevante: **-1,0**
- API key expuesta en repo: **tope 4,0** (aunque funcione)

---

## 8) Formato de entrega (sugerido)

- Entregar un **ZIP** o **link al repo** + **informe PDF** + **diagrama** + **link demo**.
- Nombre: `GrupoX_ReAct_Redis_MasterAI_2026.pdf` (o similar).

---

## 9) Configuración de Redis VPS (Infraestructura disponible)

### Docker Compose configurado

El proyecto cuenta con Redis desplegado en VPS usando Docker Swarm:
```yaml
version: "3.7"
services:
  redis:
    image: redis:latest
    command: [
        "redis-server",
        "--appendonly",
        "yes",
        "--port",
        "6379",
        "--bind",
        "0.0.0.0"
      ]
    volumes:
      - redis_data:/data
    networks:
      - SouldreamNet
    ports:
      - 6379:6379
    deploy:
      placement:
        constraints:
          - node.role == manager
      resources:
        limits:
          cpus: "1"
          memory: 2048M

volumes:
  redis_data:
    external: true
    name: redis_data

networks:
  SouldreamNet:
    external: true
    name: SouldreamNet
```

### Características de la instancia Redis:

- **Puerto:** 6379 (expuesto públicamente)
- **Persistencia:** AOF (Append Only File) habilitado
- **Volumen:** `redis_data` para persistencia de datos
- **Recursos:** 1 CPU, 2GB RAM
- **Red:** SouldreamNet (red Docker interna)

### Configuración en el proyecto Python:

Ejemplo de conexión en `config.example.env`:
```bash
# Redis Configuration
REDIS_HOST=147.93.3.53
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Opcional, si configuras autenticación

# OpenAI API
OPENAI_API_KEY=sk-...
```

### Notas de seguridad:

⚠️ **IMPORTANTE:** 
- El Redis está expuesto públicamente (0.0.0.0:6379)
- **Recomendación:** Configurar autenticación con `requirepass` en producción
- Considerar usar firewall o VPN para restringir acceso
- NO almacenar datos sensibles sin encriptación

### Conexión desde Python:
```python
import redis
from dotenv import load_dotenv
import os

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    decode_responses=True
)

# Test de conexión
redis_client.ping()
```

Propuesta de estructura
Tarea de agentes/
├── .env                      # ✅ Ya tienes Redis configurado
├── .env.example
├── requirements.txt
├── README.md
│
├── config.py                 # Configuración centralizada
├── ingest.py                 # Carga documentos a Redis
├── agent.py                  # Loop ReAct principal
├── test_redis.py             # ✅ Ya funciona
│
├── tools/
│   ├── __init__.py
│   ├── search_kb.py          # Búsqueda vectorial/keyword
│   ├── get_doc.py            # Obtener documento por ID
│   └── cite.py               # Sistema de citación
│
├── data/
│   └── documents/            # Aquí van tus 20+ documentos
│       ├── doc1.txt
│       ├── doc2.pdf
│       └── ...
│
├── utils/
│   ├── __init__.py
│   ├── chunking.py           # Estrategia de chunking
│   └── embeddings.py         # Generación de embeddings
│
├── tests/
│   ├── test_agent.py
│   └── test_tools.py
│
└── docs/
    ├── diagrama_flujo.png    # Diagrama ReAct
    └── informe.pdf           # Informe final