# Informe de Diseño e Implementación: Agente ReAct + Redis KB

## 1. Arquitectura
El sistema sigue una arquitectura **ReAct (Reason + Act)** donde el LLM actúa como controlador central.
- **Planner (LLM)**: Decide qué acción tomar (buscar, leer, responder).
- **Herramientas**: 
  - `search_kb`: Búsqueda semántica usando embeddings (OpenAI `text-embedding-3-small` + Redis).
  - `get_doc`: Recuperación de metadatos.
- **Memoria**: Contexto conversacional limitado a la ejecución del loop actual.

## 2. Decisiones de Diseño
- **Base de Conocimiento**: Redis en VPS remoto. Se eligió Redis por su baja latencia.
- **Chunking**: Estrategia de **500 caracteres con 50 de overlap**.
  - Justificación: Tamaño suficiente para contener una regla completa sin perder contexto.
- **Localización**: Todo el flujo (datos, prompts, respuestas) está localizado al español.
- **Manejo de Incertidumbre**: El prompt del sistema fuerza al agente a decir "No encontré evidencia" si no hay datos relevantes.

## 3. Evidencias de Funcionamiento

### Caso 1: Hecho Conocido
**Consulta**: "¿Cuál es el impuesto a las importaciones de dilitio?"
**Respuesta Agente**: "El impuesto a las importaciones de dilitio es del 5%. [Fuentes: doc_01_Ley_de_Aranceles...]"
**Estado**: ✅ Correcto con cita.

### Caso 2: Hecho Desconocido
**Consulta**: "¿Dónde puedo comprar un sable de luz?"
**Respuesta Agente**: "No encontré evidencia en la KB sobre la compra de sables de luz."
**Estado**: ✅ Correcto (Manejo de huecos).

## 4. Riesgos y Seguridad
- **Prompt Injection**: Un documento podría contener instrucciones maliciosas.
  - *Mitigación*: En el prompt, delimitamos el contexto de documentos.
- **Alucinaciones**: El agente podría inventar reglas.
  - *Mitigación*: Prompt restrictivo "responder estrictamente basado en KB".

## 5. Conclusiones
El agente demuestra capacidad para razonar y buscar evidencia en español, cumpliendo el flujo ReAct.
