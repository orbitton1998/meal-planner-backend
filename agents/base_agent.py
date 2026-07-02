import anthropic
import os

class BaseAgent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def run(self, user_message: str) -> str:
        print(f"🤖 [{self.name}] running...")
        
        message = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=self.system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        result = message.content[0].text
        result = self._clean_json(result)
        print(f"✅ [{self.name}] done.")
        return result
    
    def _clean_json(self, text: str) -> str:
        """Strip markdown code fences if Claude added them"""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        return cleaned.strip()