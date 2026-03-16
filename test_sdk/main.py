import openai
from safeai import SafeAI


def main():

    # יצירת מופע של SafeAI עם מזהה פרופיל
    evaluator = SafeAI(profile_id="69add18e588e9d005a875804")

    # אתחול
    evaluator.initialize()

    # קבלת system prompt
    system_prompt = evaluator.get_system_prompt()

    # הערכת טקסט עם בדיקה מושבתת (אופציונלי)
    my_prompt = "אני רוצה לפתח קומפוננטה של הרשמה לאתר עם גוגל."
    result = evaluator.evaluate(my_prompt, audit_disabled=True)

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


if __name__ == "__main__":
    main()
