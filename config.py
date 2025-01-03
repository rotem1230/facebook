from dotenv import load_dotenv
import os

# טעינת משתני הסביבה מקובץ .env
load_dotenv()

# הגדרות פייסבוק
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")

# הגדרות OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# הגדרות אבטחה
SECRET_KEY = os.getenv("SECRET_KEY")

# הגדרות בסיס נתונים
DATABASE_URL = "sqlite:///./facebook_leads.db"

# הגדרות JWT
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
