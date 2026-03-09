import httpx
import logging

logger = logging.getLogger(__name__)

class AsyncSafeAI:
    def __init__(self, profile_id: str="69add18e588e9d005a875804", api_base_url: str  = "https://ai613.autodidact.co.il/console/api/filter"):
        self.profile_id = profile_id
        self.api_base_url = api_base_url
        self.evaluate_url = f"{api_base_url}/evaluate"
        self.profile_url = f"{api_base_url}/ai-profiles"
        
        # נתונים שיטענו מהשרת
        self.name = None
        self.content_prompts = []
        self.behavior_prompts = []
        self.knowledge_prompts = []
        self.is_initialized = False

    async def initialize(self):
        """
        טוען את נתוני הפרופיל והפרומפטים מהשרת בצורה אסינכרונית.
        חובה לקרוא לפונקציה זו לאחר יצירת האובייקט.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.profile_url)
                response.raise_for_status()
                profiles = response.json()
                
                # חיפוש הפרופיל המתאים ברשימה
                profile = next((p for p in profiles if p.get("_id") == self.profile_id), None)
                
                if profile:
                    self.name = profile.get("name")
                    self.content_prompts = profile.get("contentPrompts", [])
                    self.behavior_prompts = profile.get("behaviorPrompts", [])
                    self.knowledge_prompts = profile.get("knowledgePrompts", [])
                    self.is_initialized = True
                    logger.info(f"SafeAI: Profile '{self.name}' initialized successfully.")
                else:
                    logger.error(f"SafeAI: Profile ID {self.profile_id} not found.")
            except Exception as e:
                logger.error(f"SafeAI: Failed to initialize profile: {e}")

    async def evaluate(self, text: str):
        """
        שולח טקסט לבדיקה מול השרת.
        """
        if not self.is_initialized:
            logger.warning("SafeAI: Evaluator called before initialization.")

        payload = {
            "profileId": self.profile_id,
            "text": text
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.evaluate_url, json=payload, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"allowed": False, "reason": f"API Error: {e.response.status_code}"}
            except Exception as e:
                return {"allowed": False, "reason": f"Connection Error: {str(e)}"}