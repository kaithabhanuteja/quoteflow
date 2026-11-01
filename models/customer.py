from datetime import datetime, timezone
from database import db

def utc_now():
    return datetime.now(timezone.utc)

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, index=True)
    company = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    projects = db.relationship("Project", backref="customer", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "company": self.company or "N/A",
            "phone": self.phone or "N/A",
            "address": self.address or "",
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
