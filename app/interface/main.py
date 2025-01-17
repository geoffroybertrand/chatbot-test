import streamlit as st
from datetime import datetime
import asyncio
from app.chat.chain import ChatChain 

class ChatInterface:
    def __init__(self):
        self.chat_chain = ChatChain()
        
        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "user_id" not in st.session_state:
            st.session_state.user_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    async def process_message(self, message: str) -> Dict:
        """Process a message through the chat chain"""
        return await self.chat_chain.process_message(
            message=message,
            conversation_history=st.session_state.messages
        )
    
    def render(self):
        """Render the chat interface"""
        st.title("Mon Superviseur IA")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Comment puis-je vous aider ?"):
            # Add user message
            st.session_state.messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get and display response
            with st.chat_message("assistant"):
                with st.spinner("Réflexion..."):
                    response = asyncio.run(self.process_message(prompt))
                    st.session_state.messages.append(response)
                    st.markdown(response["content"])

if __name__ == "__main__":
    interface = ChatInterface()
    interface.render()