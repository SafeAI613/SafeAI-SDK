# SafeAI SDK

Python SDK עבור שרת סינון SafeAI.

## התקנה

### מה-PyPI (אם זמין)
```bash
pip install safeai-sdk
```

### מהקובץ המקומי .whl

[צפה ב‑Release ב‑GitHub](https://github.com/SafeAI613/SafeAI-SDK/releases/tag/v0.1.0)

אם יש לך קובץ .whl שנבנה מקומית:
```bash
pip install path/to/safeai_sdk-0.1.0-py3-none-any.whl
```

לדוגמה, אם הקובץ נמצא בתיקיית `dist`:
```bash
pip install dist/safeai_sdk-0.1.0-py3-none-any.whl
```

## שימוש

```python
import openai
from safeai import SafeAI

# יצירת מופע של SafeAI עם מזהה פרופיל
evaluator = SafeAI(profile_id="69add18e588e9d005a875804")

# אתחול
evaluator.initialize()

# קבלת system prompt
system_prompt = evaluator.get_system_prompt()

# הערכת טקסט עם בדיקה מושבתת (אופציונלי)
my_prompt = "מה יש בתמונה הזאת?"
result = evaluator.evaluate(my_prompt)
// result = evaluator.evaluate(my_prompt, audit_disabled=True)  // בפיתוח


print("תוצאת ההערכה:", result)

# אם לא עבר את הבדיקה, זרוק שגיאה
if not result.get("allowed", False):
    raise ValueError(f"הטקסט נחסם: {result.get('reason', 'סיבה לא ידועה')}")

# אם עבר, בצע קריאה ל-OpenAI עם ה-system prompt
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": my_prompt}
    ]
)

print("תשובת OpenAI:", response.choices[0].message.content)
```

### שימוש אסינכרוני (AsyncSafeAI)

```python
import asyncio
from safeai import AsyncSafeAI

async def main():
    evaluator = AsyncSafeAI(profile_id="69add18e588e9d005a875804")
    await evaluator.initialize()
    
    result = await evaluator.evaluate("טקסט לבדיקה")
    print("תוצאת ההערכה:", result)
    
    system_prompt = evaluator.get_system_prompt()
    print("System Prompt:", system_prompt)

asyncio.run(main())
```

## דרישות

- Python >= 3.8
- requests
- httpx
- openai (לשימוש עם OpenAI API)

## גרסה

גרסה נוכחית: 0.1.0
