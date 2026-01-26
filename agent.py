from openai import OpenAI
import json
from config import Config
from tools.search_kb import search_kb
from tools.get_doc import get_doc
from tools.cite import cite

client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Define Tools Schema for OpenAI (Translated)
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_kb",
            "description": "Busca información sobre la selección chilena de fútbol (La Roja), su historia, jugadores y logros. Usa esto para encontrar datos específicos vinculados a la selección.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "La consulta de búsqueda, ej. 'requisitos para ser administrador' o 'quórum de asamblea'"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doc",
            "description": "Recupera detalles de un documento específico por su ID. Úsalo si necesitas más contexto de un doc encontrado.",
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "El ID del Documento"
                    }
                },
                "required": ["doc_id"]
            }
        }
    }
]

SYSTEM_PROMPT = """
Eres un Agente ReAct experto en la Selección Chilena de Fútbol (La Roja).
Tu objetivo es responder preguntas de los usuarios basándote estrictamente en la Base de Conocimiento (KB) que contiene información sobre la selección.

**Proceso:**
1. **Razonar**: Analiza la solicitud del usuario y decide qué información sobre La Roja necesitas.
2. **Actuar**: Usa 'search_kb' para encontrar datos sobre historia, jugadores, o hitos del equipo.
3. **Observar**: Analiza los resultados de la búsqueda.
4. **Bucle**: Si es necesario, busca de nuevo o refina tu búsqueda.
5. **Responder**: Proporciona la respuesta final citando los archivos correspondientes (ej. chunk_0001.txt).

**Reglas Críticas de Veracidad e Incertidumbre:**
- SIEMPRE permite "pensar" antes de llamar a una herramienta. Escribe una línea "Pensamiento:".
- **Exactitud Detallada**: Si la pregunta pide un detalle específico (ej. un estadio, un marcador exacto, una fecha) y la KB menciona el evento pero NO ese detalle, DEBES informarlo. Ejemplo: "La KB menciona que Chile ganó en 2016 en Estados Unidos, pero no especifica el nombre del estadio".
- **No Extrapolar**: No utilices tu conocimiento general para rellenar vacíos. Si no está en el texto citado, no existe para este agente.
- **Incertidumbre**: Si los resultados son irrelevantes, di explícitamente "No encontré información en la KB sobre [tema]".
- **Citas Obligatorias**: Tu respuesta final DEBE incluir citas (ej. "según el archivo chunk_00XX.txt").
- RESPONDE SIEMPRE EN ESPAÑOL.
"""

def process_query(user_query):
    """
    Generator that yields events from the ReAct loop.
    Events are dicts: {"type": "thought"|"tool_call"|"observation"|"answer", "content": ...}
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    yield {"type": "thought", "content": f"Iniciando proceso para: {user_query}"}
    
    step = 0
    max_steps = 5
    
    while step < max_steps:
        step += 1
        
        # 1. Call LLM
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto"
        )
        
        msg = response.choices[0].message
        
        # 2. Check for Tool Calls
        if msg.tool_calls:
            # Print Thought if existing
            if msg.content:
                yield {"type": "thought", "content": msg.content}
                
            messages.append(msg) # Add assistant message with tool calls
            
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                yield {"type": "tool_call", "content": f"Llamando a {func_name} con {args}"}
                
                # Execute Tool
                result = None
                if func_name == "search_kb":
                    result = search_kb(args["query"])
                elif func_name == "get_doc":
                    result = get_doc(args["doc_id"])
                
                # Observation
                obs_preview = str(result)[:1000] + "..." if len(str(result)) > 1000 else str(result)
                yield {"type": "observation", "content": obs_preview}
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
        else:
            # No tool calls, final answer
            answer = msg.content
            yield {"type": "answer", "content": answer}
            return
            
    yield {"type": "answer", "content": "Error: Se alcanzó el máximo de pasos sin respuesta definitiva."}

def run_agent(user_query):
    """
    CLI wrapper for process_query
    """
    print(f"\n--- Nueva Solicitud: {user_query} ---")
    for event in process_query(user_query):
        if event["type"] == "thought":
            print(f"[Razonamiento] {event['content']}")
        elif event["type"] == "tool_call":
            print(f"[Actuar] {event['content']}")
        elif event["type"] == "observation":
            print(f"[Observar] Resultado: {event['content']}")
        elif event["type"] == "answer":
            print(f"[Respuesta] {event['content']}")

if __name__ == "__main__":
    # Test Queries in Spanish
    print(">>> Test 1: Historia")
    run_agent("¿Qué es la Roja?")
    
    print("\n>>> Test 2: Generación Dorada")
    run_agent("¿Qué es la Generación Dorada?")
