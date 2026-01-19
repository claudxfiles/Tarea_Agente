# ReAct Agent + Redis KB

Este proyecto implementa un agente inteligente tipo **ReAct** (Reason+Act) que utiliza **OpenAI API** para razonamiento y **Redis** como Base de Conocimiento (KB) vectorial.

## 🚀 Instalación y Ejecución

### 1. Configuración
Asegúrate de tener un archivo `.env` configurado (ver `config.example.env`):
```bash
REDIS_HOST=147.93.3.53
REDIS_PORT=6379
OPENAI_API_KEY=sk-...
```

### 2. Generar Datos e Ingesta
Carga los documentos simulados a Redis:
```bash
# Genera docs
python generate_data.py

# Ingesta (Chunking + Embeddings + Redis Index)
python ingest.py
```

### 3. Ejecutar Agente
```bash
python agent.py
```

### 4. Interfaz Web (Streamlit)
Para una experiencia conversacional:
```bash
python -m streamlit run app.py
```

## 📂 Estructura
- `agent.py`: Loop principal del agente (ReAct).
- `tools/`: Herramientas (`search_kb`, `get_doc`, `cite`).
- `utils/`: Utilidades (`chunking`, `embeddings`).
- `data/documents/`: Documentos de la KB.

## 🧠 Diseño
- **Patrón**: ReAct (Reason -> Act -> Observe).
- **KB**: Redis Stack (Vector Search).
- **Modelo**: GPT-4 Turbo.
