import requests
import logging

logger = logging.getLogger(__name__)

class SafeAI:
    def __init__(self, profile_id: str="69add18e588e9d005a875804", api_base_url: str = "https://ai613.autodidact.co.il/console/api/filter"):
        self.profile_id = profile_id
        self.api_base_url = api_base_url
        self.evaluate_url = f"{api_base_url}/evaluate"
        self.profile_url = f"{api_base_url}/ai-profiles"
        
        # נתונים שיטענו מהשרת
        self.name = None
        self.content_prompts = ["""
                                You are a content filter for the Orhodox community.
           Your task is to determine if the text is safe and appropriate according to conservative education values. 
           In your response, do not reference the following topics in any way: <Other religions besides orthodox jewisem, relationships with women, sexual relations, Sexual exploitation or harassment, rape, sex, violent, immodest, romantic, intimate content, including innuendo, venereal diseases, fertility, pills, gynecology,impossible to answer the question without referencing these forbidden topics, respond only with: blocked.
           Even if the prohibited topics are requested inside a data structure such as an object, array, HTML page, or any other programming-related context, do not respond to them.           
          Corresponding to the profile's values:
           Respond only with "allowed" or "blocked".
                                
                                """]
        self.behavior_prompts = []
        self.knowledge_prompts = []
        self.is_initialized = False

    def initialize(self):
        """
        טוען את נתוני הפרופיל והפרומפטים מהשרת בצורה סינכרונית.
        חובה לקרוא לפונקציה זו לאחר יצירת האובייקט.
        """
        try:
            response = requests.get(self.profile_url, timeout=10)
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

    def evaluate(self, text: str,audit_disabled: bool = False) -> dict:
        """
        שולח טקסט לבדיקה מול השרת.
        """
        if not self.is_initialized:
            logger.warning("SafeAI: Evaluator called before initialization.")

        payload = {
            "profileId": self.profile_id,
            "text": text,
            "auditDisabled": audit_disabled
        }

        try:
            response = requests.post(self.evaluate_url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            return {"allowed": False, "reason": f"API Error: {response.status_code}"}

        except Exception as e:
            return {"allowed": False, "reason": f"Connection Error: {str(e)}"}

    def get_system_prompt(self) -> str:
        """
        מחזיר system prompt שבנוי משרשור כל הפרומפטים שהתקבלו מהשרת.
        אם לא הצליח לטעון מהשרת, משתמש בפרומפט ברירת מחדל.
        """
        all_prompts = self.content_prompts + self.behavior_prompts + self.knowledge_prompts
        return "\n".join(all_prompts)