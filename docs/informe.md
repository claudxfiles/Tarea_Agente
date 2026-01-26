# Informe de Diseño e Implementación: Agente Experto en La Roja

## 1. Arquitectura
El sistema utiliza un flujo **ReAct (Reason + Act)** para actuar como un experto en la **Selección Chilena de Fútbol (La Roja)**.
- **Planner (OpenAI GPT-4o)**: Ejecuta el bucle de razonamiento, decide qué herramientas invocar y sintetiza la respuesta final con citas de la base de conocimiento.
- **Herramientas (Knowledge Base)**: 
  - `search_kb`: Implementa búsqueda vectorial (RAG) sobre Redis. Utiliza `text-embedding-3-small` para generar vectores de 1536 dimensiones.
  - `get_doc`: Permite al agente inspeccionar un fragmento específico para obtener contexto adicional.
- **Memoria**: El agente mantiene el hilo de razonamiento durante cada consulta.

## 2. Decisiones de Diseño
- **Fuentes de Datos**: Se procesaron 22 fragmentos de texto ubicados en `data/Doc`, los cuales contienen información sobre la identidad, historia y hitos de la selección chilena.
- **Estrategia de Chunking**: Debido a que la fuente ya venía segmentada, se utilizó un tamaño de fragmento de **90 caracteres con 0 de overlap**, lo que permite una recuperación granular de oraciones y conceptos específicos.
- **Base de Datos Vectorial**: Redis configurado con un índice `HNSW` para búsquedas de similitud precisas.
- **Restricciones**: El sistema tiene un prompt restrictivo que exige citas (ej. `chunk_0001.txt`) y evita alucinaciones sobre datos futbolísticos.

## 3. Evidencias de Funcionamiento

### Caso 1: Consulta sobre Identidad
**Consulta**: "¿Qué es la Roja?"
**Resultado**: "La Roja es la selección chilena, un símbolo de identidad y pasión... [Fuentes: chunk_0001.txt]"
**Estado**: ✅ Correcto.

### Caso 2: Consulta sobre Hitos Históricos
**Consulta**: "¿Qué es la Generación Dorada?"
**Resultado**: "Es la etapa más gloriosa de la selección, marcada por la obtención de dos Copas América... [Fuentes: chunk_0010.txt]"
**Estado**: ✅ Correcto.

## 4. Riesgos y Mitigación
- **Riesgo de Información incompleta**: El dominio del fútbol es vasto.
  - *Mitigación*: El agente está instruido para admitir si no encuentra información específica en los chunks proporcionados.

## 5. Conclusiones
El agente demuestra ser capaz de navegar por fragmentos breves de información para construir una narrativa coherente sobre la selección chilena, manteniendo la trazabilidad mediante citas directas a la base de conocimiento.

