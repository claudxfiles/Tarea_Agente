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
            "description": "Busca en la Ley de Copropiedad Inmobiliaria (KB) artículos y conceptos relevantes. Usa esto para encontrar evidencia legal.",
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
Eres un Agente ReAct especializado en la Ley de Copropiedad Inmobiliaria de Chile (Ley 21.442).
Tu objetivo es responder preguntas de los usuarios basándote estrictamente en la Base de Conocimiento (KB) que contiene el texto de la ley.

**Proceso:**
1. **Razonar**: Analiza la solicitud del usuario y decide qué información de la ley necesitas.
2. **Actuar**: Usa 'search_kb' para encontrar artículos o secciones relevantes de la ley.
3. **Observar**: Analiza los resultados de la búsqueda.
4. **Bucle**: Si es necesario, busca de nuevo o refina tu búsqueda.
5. **Responder**: Proporciona la respuesta final citando los artículos correspondientes.

**Reglas:**
- SIEMPRE permite "pensar" antes de llamar a una herramienta. Escribe una línea "Pensamiento:".
- Si los resultados de la búsqueda están vacíos o son irrelevantes, di explícitamente "No encontré evidencia en la KB".
- Si no estás seguro o la ley no lo menciona, expresa incertidumbre.
- VALIDAR: Tu respuesta final DEBE incluir citas (ej. "según el Artículo 5...", "basado en el chunk X").
- No inventes información legal.
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
                obs_preview = str(result)[:200] + "..." if len(str(result)) > 200 else str(result)
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
    print(">>> Test 1: Hecho Simple")
    run_agent("¿Cuáles son los requisitos para ser administrador?")
    
    print("\n>>> Test 2: Hecho Desconocido")
    run_agent("¿Cómo se regula la tenencia de mascotas en condominios?")
