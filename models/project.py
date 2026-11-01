from datetime import datetime, timezone
from database import db

def utc_now():
    return datetime.now(timezone.utc)

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    industry = db.Column(db.String(120), nullable=False, index=True)
    category = db.Column(db.String(120), nullable=False)
    complexity = db.Column(db.String(50), default="Medium")
    complexity_score = db.Column(db.Integer, default=50)
    business_objectives = db.Column(db.Text, nullable=True)
    email_source_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    quotations = db.relationship("Quotation", backref="project", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "name": self.name,
            "industry": self.industry,
            "category": self.category,
            "complexity": self.complexity,
            "complexity_score": self.complexity_score,
            "business_objectives": self.business_objectives,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }
