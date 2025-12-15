# models/xp_transaction.py
import uuid
from datetime import datetime
from db import db

def generate_uuid_str():
    return str(uuid.uuid4())

class Feature(db.Model):
    __tablename__ = "feature"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid_str)
    name = db.Column(db.String(50), unique=True, nullable=False)

    xp_transactions = db.relationship("XPTransaction", backref="feature", lazy=True)


class Source(db.Model):
    __tablename__ = "source"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid_str)
    name = db.Column(db.String(50), unique=True, nullable=False)

    xp_transactions = db.relationship("XPTransaction", backref="source", lazy=True)


class XPTransaction(db.Model):
    __tablename__ = "xp_transaction"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid_str)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    transaction_type = db.Column(db.Enum("earned", "spent", name="transaction_type"), nullable=False)
    source_id = db.Column(db.String(36), db.ForeignKey("source.id"), nullable=False)
    reference_id = db.Column(db.String(36), nullable=True)
    feature_id = db.Column(db.String(36), db.ForeignKey("feature.id"), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
