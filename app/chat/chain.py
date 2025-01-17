from typing import Dict, List, Optional
from datetime import datetime
import anthropic
from app.config import settings  # Import absolu au lieu de relatif

class ChatChain:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.CLAUDE_API_KEY)
        
    async def process_message(
        self,
        message: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict:
        """Process a message and return a response"""
        try:
            # Format conversation history
            history_text = ""
            if conversation_history:
                history_text = "\n".join([
                    f"User: {msg['content']}\nAssistant: {msg['response']}"
                    for msg in conversation_history[-3:]  # Last 3 messages
                ])

            # Create prompt
            prompt = f"""Historique de la conversation:
{history_text}

Message actuel: {message}

Instructions:
{settings.SYSTEM_PROMPT}
"""

            # Get response from Claude
            response = await self.client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=settings.MAX_TOKENS,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            return {
                "role": "assistant",
                "content": response.content,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            print(f"Error: {str(e)}")
            return {
                "role": "assistant",
                "content": "Je suis désolé, j'ai rencontré une erreur. Pouvez-vous reformuler votre question ?",
                "error": str(e)
            }