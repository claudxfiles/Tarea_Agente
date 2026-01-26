import streamlit as st
import time
from agent import process_query

st.set_page_config(page_title="Agente La Roja", page_icon="⚽")

st.title("⚽ Agente Experto en La Roja")
st.markdown("Todo sobre la Selección Chilena de Fútbol. Historia, jugadores, la Generación Dorada y más.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("¿En qué puedo ayudarte hoy?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Container for thoughts/tools
        with st.expander("Proceso de Razonamiento (Internals)", expanded=False):
            thought_container = st.empty()
            thoughts_text = ""
            
            # Stream from generator
            for event in process_query(prompt):
                if event["type"] == "thought":
                    new_thought = f"🤔 **Razonamiento:** {event['content']}\n\n"
                    thoughts_text += new_thought
                    thought_container.markdown(thoughts_text)
                    
                elif event["type"] == "tool_call":
                    new_tool = f"🛠️ **Acción:** {event['content']}\n\n"
                    thoughts_text += new_tool
                    thought_container.markdown(thoughts_text)
                    
                elif event["type"] == "observation":
                    new_obs = f"👀 **Observación:** {event['content']}\n\n"
                    thoughts_text += new_obs
                    thought_container.markdown(thoughts_text)
                    
                elif event["type"] == "answer":
                    full_response = event["content"]
                    
        # Final answer display
        if full_response:
            message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
