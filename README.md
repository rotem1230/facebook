# מערכת ניתוח לידים בפייסבוק

מערכת אוטומטית לניתוח וניהול לידים מקבוצות פייסבוק באמצעות AI.

## תכונות עיקריות

- חיבור לחשבון פייסבוק
- חיפוש וסריקת קבוצות אוטומטית
- ניתוח פוסטים באמצעות AI
- תגובות אוטומטיות חכמות
- שליחת הודעות פרטיות
- דשבורד לניהול וניתוח

## התקנה

1. התקן את הדרישות:
```bash
pip install -r requirements.txt
```

2. צור קובץ `.env` והגדר את המשתנים הבאים:
```
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_secret_key
```

3. הרץ את השרת:
```bash
python main.py
```

## שימוש

1. התחבר למערכת עם חשבון המשתמש שלך
2. חבר את חשבון הפייסבוק שלך
3. הגדר מילות מפתח לחיפוש
4. צור תבניות תגובה
5. התחל לנטר ולנהל לידים

## טכנולוגיות

- Python FastAPI
- Facebook API
- OpenAI API
- SQLite
- React (Frontend)
