import json
from datetime import datetime, timezone
from database import db

def utc_now():
    return datetime.now(timezone.utc)

class Quotation(db.Model):
    __tablename__ = "quotations"

    id = db.Column(db.Integer, primary_key=True)
    reference_no = db.Column(db.String(60), unique=True, nullable=False, index=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    current_version = db.Column(db.Integer, default=1)
    status = db.Column(db.String(50), default="Draft", index=True) # Draft, In Review, Approved, Sent, Revised, Rejected
    total_cost = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default="INR")
    created_at = db.Column(db.DateTime, default=utc_now)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    versions = db.relationship(
        "QuotationVersion",
        backref="quotation",
        cascade="all, delete-orphan",
        order_by="QuotationVersion.version_number.desc()",
        lazy=True,
    )
    activities = db.relationship("ActivityLog", backref="quotation", cascade="all, delete-orphan", lazy=True)

    def to_dict(self):
        latest_ver = self.versions[0] if self.versions else None
        return {
            "id": self.id,
            "reference_no": self.reference_no,
            "project_id": self.project_id,
            "project_name": self.project.name if self.project else "Unknown",
            "industry": self.project.industry if self.project else "General",
            "customer_name": self.project.customer.name if self.project and self.project.customer else "Unknown",
            "customer_company": self.project.customer.company if self.project and self.project.customer else "N/A",
            "customer_email": self.project.customer.email if self.project and self.project.customer else "",
            "current_version": self.current_version,
            "status": self.status,
            "total_cost": self.total_cost,
            "currency": self.currency,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
            "pdf_url": f"/api/quotations/{self.id}/pdf" if latest_ver and latest_ver.pdf_path else None,
        }


class QuotationVersion(db.Model):
    __tablename__ = "quotation_versions"

    id = db.Column(db.Integer, primary_key=True)
    quotation_id = db.Column(db.Integer, db.ForeignKey("quotations.id"), nullable=False)
    version_number = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(50), default="Draft")
    pdf_path = db.Column(db.String(300), nullable=True)
    data_json = db.Column(db.Text, nullable=False) # Serialized full quotation structure
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now)

    def get_data(self):
        try:
            return json.loads(self.data_json)
        except Exception:
            return {}

    def set_data(self, data_dict):
        self.data_json = json.dumps(data_dict, indent=2)

    def to_dict(self):
        return {
            "id": self.id,
            "quotation_id": self.quotation_id,
            "version_number": self.version_number,
            "status": self.status,
            "pdf_path": self.pdf_path,
            "notes": self.notes,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "data": self.get_data(),
        }
