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
            "description": "Busca en la Base de Conocimiento regulaciones y documentos relevantes. Usa esto para encontrar evidencia.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "La consulta de búsqueda, ej. 'regulaciones sobre motores warp'"
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
Eres un Agente ReAct especializado en Regulaciones de Comercio Galáctico.
Tu objetivo es responder preguntas de los usuarios basándote estrictamente en la Base de Conocimiento (KB).

**Proceso:**
1. **Razonar**: Analiza la solicitud del usuario y decide qué información necesitas.
2. **Actuar**: Usa 'search_kb' para encontrar información.
3. **Observar**: Analiza los resultados de la búsqueda.
4. **Bucle**: Si es necesario, busca de nuevo o refina tu búsqueda.
5. **Responder**: Proporciona la respuesta final con citas.

**Reglas:**
- SIEMPRE permite "pensar" antes de llamar a una herramienta. Escribe una línea "Pensamiento:".
- Si los resultados de la búsqueda están vacíos o son irrelevantes, di explícitamente "No encontré evidencia en la KB".
- Si no estás seguro, expresa incertidumbre.
- VALIDAR: Tu respuesta final DEBE incluir citas usando el formato [doc_id] provisto por la lógica de 'cite' (o referencias de ID).
- No inventes información.
- RESPONDE SIEMPRE EN ESPAÑOL.
"""

def run_agent(user_query):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    print(f"\n--- Nueva Solicitud: {user_query} ---")
    
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
                print(f"[Razonamiento] {msg.content}")
                
            messages.append(msg) # Add assistant message with tool calls
            
            for tool_call in msg.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"[Actuar] Llamando a {func_name} con {args}")
                
                # Execute Tool
                result = None
                if func_name == "search_kb":
                    result = search_kb(args["query"])
                    # Filter/Rank results logic could go here
                elif func_name == "get_doc":
                    result = get_doc(args["doc_id"])
                
                # Observation
                print(f"[Observar] Resultado: {str(result)[:200]}...") # Truncate for log
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
        else:
            # No tool calls, final answer
            answer = msg.content
            print(f"[Respuesta] {answer}")
            return answer
            
    return "Error: Se alcanzó el máximo de pasos."

if __name__ == "__main__":
    # Test Queries in Spanish
    print(">>> Test 1: Hecho Simple")
    run_agent("¿Cuál es el impuesto a las importaciones de dilitio?")
    
    print("\n>>> Test 2: Hecho Desconocido")
    run_agent("¿Dónde puedo comprar un sable de luz?")
