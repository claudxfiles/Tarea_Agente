# Informe de Diseño e Implementación: Agente de Copropiedad Inmobiliaria

## 1. Arquitectura
El sistema utiliza un flujo **ReAct (Reason + Act)** para actuar como un experto legal en la **Ley 21.442 de Copropiedad Inmobiliaria de Chile**.
- **Planner (OpenAI GPT-4o)**: Ejecuta el bucle de razonamiento, decide qué herramientas invocar y sintetiza la respuesta final con citas legales.
- **Herramientas (Knowledge Base)**: 
  - `search_kb`: Implementa búsqueda vectorial (RAG) sobre Redis. Utiliza `text-embedding-3-small` para generar vectores de 1536 dimensiones.
  - `get_doc`: Permite al agente inspeccionar un documento específico para obtener contexto adicional si la búsqueda inicial es insuficiente.
- **Memoria**: El agente mantiene el hilo de razonamiento durante cada consulta para refinar sus búsquedas si es necesario.

## 2. Decisiones de Diseño
- **Fuentes de Datos**: Se migró de un único PDF masivo a **20 archivos de texto especializados** ubicados en `data/Doc_2`. Cada archivo aborda un pilar de la ley (Administración, Mascotas, Gastos Comunes, etc.).
- **Estrategia de Chunking**: Se emplea un tamaño de fragmento de **90 caracteres con 0 de overlap**.
  - *Justificación*: Los documentos fuente ya vienen pre-segmentados en fragmentos de este tamaño, por lo que esta configuración garantiza una correspondencia 1:1 con la estructura original.
- **Base de Datos Vectorial**: Redis alojado de forma persistente, configurado con un índice `HNSW` para búsquedas de similitud de coseno eficientes.
- **Localización y Restricciones**: El sistema opera 100% en español y posee un prompt restrictivo para evitar alucinaciones, exigiendo citas obligatorias de la KB.

## 3. Evidencias de Funcionamiento

### Caso 1: Consulta Legal Específica
**Consulta**: "¿Cómo se regula la tenencia de mascotas?"
**Razonamiento**: El agente identifica la necesidad de buscar en la sección de convivencia.
**Resultado**: "La Ley 21.442 establece el marco general para la convivencia... [Fuentes: 15_tenencia_de_mascotas_chunked.txt]"
**Estado**: ✅ Correcto. Recupera el documento especializado y responde basándose en el marco legal.

### Caso 2: Manejo de Out-of-Domain
**Consulta**: "¿Dónde puedo comprar un sable de luz?"
**Resultado**: "No tengo información sobre productos específicos como un sable de luz. Mi especialización es asistir con consultas sobre la Ley de Copropiedad Inmobiliaria de Chile."
**Estado**: ✅ Correcto. El agente reconoce sus límites y no intenta inventar información fuera de su dominio.

## 4. Riesgos y Mitigación
- **Riesgo de Desactualización**: La ley podría sufrir modificaciones.
  - *Mitigación*: La arquitectura modular permite reemplazar archivos específicos en `data/Doc_2` y re-ejecutar `ingest.py` en segundos.
- **Seguridad**: Prevención de inyecciones de prompt mediante la delimitación estricta del contexto de los documentos recuperados.

## 5. Conclusiones
La transición a múltiples documentos de texto ha mejorado la precisión de las citas, permitiendo al agente apuntar a archivos temáticos específicos. El flujo ReAct garantiza que el usuario reciba respuestas razonadas y fundamentadas en la legislación vigente.

