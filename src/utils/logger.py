import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path

class CustomLogger:
    def __init__(self):
        # יצירת תיקיית logs אם לא קיימת
        self.logs_dir = Path("logs")
        self.logs_dir.mkdir(exist_ok=True)
        
        # הגדרת קובץ הלוג הראשי
        self.log_file = self.logs_dir / "facebook_system.log"
        
        # הגדרת פורמט הלוג
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # יצירת logger
        self.logger = logging.getLogger('FacebookSystem')
        self.logger.setLevel(logging.DEBUG)
        
        # הגדרת rotating file handler - יצירת קובץ חדש כל 5MB
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(self.formatter)
        file_handler.setLevel(logging.DEBUG)
        
        # הגדרת console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        console_handler.setLevel(logging.INFO)
        
        # הוספת handlers ל-logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # מילון לשמירת זמני הלוגים האחרונים לפי סוג
        self.last_logs = {}
    
    def _update_last_log(self, error_type: str):
        """עדכון זמן הלוג האחרון לסוג תקלה מסוים"""
        self.last_logs[error_type] = datetime.now()
    
    def get_last_log_time(self, error_type: str) -> datetime:
        """קבלת זמן הלוג האחרון לסוג תקלה מסוים"""
        return self.last_logs.get(error_type)
    
    def is_log_recent(self, error_type: str, minutes: int = 60) -> bool:
        """בדיקה האם הלוג האחרון מסוג מסוים הוא עדכני (בדקות האחרונות)"""
        last_time = self.get_last_log_time(error_type)
        if not last_time:
            return False
        
        time_diff = datetime.now() - last_time
        return time_diff.total_seconds() < minutes * 60
    
    def log_auth_error(self, user_id: str, error_msg: str):
        """תיעוד שגיאות אימות"""
        error_type = f"auth_error_{user_id}"
        self._update_last_log(error_type)
        self.logger.error(f"Authentication error for user {user_id}: {error_msg}")
    
    def log_facebook_api_error(self, endpoint: str, error_msg: str):
        """תיעוד שגיאות API של פייסבוק"""
        error_type = f"fb_api_error_{endpoint}"
        self._update_last_log(error_type)
        self.logger.error(f"Facebook API error at {endpoint}: {error_msg}")
    
    def log_database_error(self, operation: str, error_msg: str):
        """תיעוד שגיאות בסיס נתונים"""
        error_type = f"db_error_{operation}"
        self._update_last_log(error_type)
        self.logger.error(f"Database error during {operation}: {error_msg}")
    
    def log_template_error(self, template_id: str, error_msg: str):
        """תיעוד שגיאות בתבניות"""
        error_type = f"template_error_{template_id}"
        self._update_last_log(error_type)
        self.logger.error(f"Template error for ID {template_id}: {error_msg}")
    
    def log_lead_processing_error(self, lead_id: str, error_msg: str):
        """תיעוד שגיאות בעיבוד לידים"""
        error_type = f"lead_error_{lead_id}"
        self._update_last_log(error_type)
        self.logger.error(f"Lead processing error for ID {lead_id}: {error_msg}")
    
    def log_system_error(self, component: str, error_msg: str):
        """תיעוד שגיאות מערכת כלליות"""
        error_type = f"system_error_{component}"
        self._update_last_log(error_type)
        self.logger.error(f"System error in {component}: {error_msg}")
    
    def log_api_request(self, method: str, endpoint: str, status_code: int):
        """תיעוד בקשות API"""
        self.logger.info(f"API {method} request to {endpoint} - Status: {status_code}")
    
    def log_user_action(self, user_id: str, action: str):
        """תיעוד פעולות משתמש"""
        self.logger.info(f"User {user_id} performed action: {action}")
    
    def log_performance_metric(self, operation: str, duration_ms: float):
        """תיעוד מדדי ביצועים"""
        self.logger.debug(f"Performance metric - {operation}: {duration_ms}ms")

# יצירת instance יחיד של Logger
logger = CustomLogger()

# דוגמאות לשימוש:
if __name__ == "__main__":
    # דוגמה לתיעוד שגיאות שונות
    logger.log_auth_error("user123", "Invalid password")
    logger.log_facebook_api_error("/leads", "Rate limit exceeded")
    logger.log_database_error("insert", "Duplicate key violation")
    logger.log_template_error("template456", "Invalid template format")
    logger.log_lead_processing_error("lead789", "Missing required field")
    
    # בדיקה האם יש לוג עדכני
    is_recent = logger.is_log_recent("auth_error_user123")
    print(f"Is recent auth error? {is_recent}")
    
    # דוגמה לתיעוד פעולות רגילות
    logger.log_api_request("POST", "/api/templates", 200)
    logger.log_user_action("user123", "Created new template")
    logger.log_performance_metric("database_query", 150.5)
