import logging
from typing import Dict, Any
from groq import AsyncGroq
from app.config import config

logger = logging.getLogger(__name__)

class LLMGenerator:
    def __init__(self):
        self.client = AsyncGroq(api_key=config.GROQ_API_KEY)
        self.model = config.LLM_MODEL
    
    async def generate(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        logger.info(f"Generating response with Groq {self.model}")
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            usage = response.usage
            
            result = {
                "answer": answer,
                "model": f"groq/{self.model}",
                "tokens_used": {
                    "prompt": usage.prompt_tokens,
                    "completion": usage.completion_tokens,
                    "total": usage.total_tokens
                }
            }
            
            logger.info(f"Generation complete. Tokens used: {usage.total_tokens}")
            return result
            
        except Exception as e:
            logger.error(f"Error in LLM generation: {str(e)}")
            raise