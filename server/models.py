from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, default='Untitled Template')
    versions = db.relationship('TemplateVersion', backref='template', lazy=True)

class TemplateVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    title = db.Column(db.String(200), nullable=False, default='Untitled Version')
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 