from datetime import datetime, timezone
from database import db

def utc_now():
    return datetime.now(timezone.utc)

class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey("quotations.id"), nullable=True)
    action = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=utc_now)
    details = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "quotation_id": self.quotation_id,
            "action": self.action,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S") if self.timestamp else None,
            "details": self.details,
        }
