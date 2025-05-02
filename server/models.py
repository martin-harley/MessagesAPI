"""
Database Models for Email Template Editor
This module defines the SQLAlchemy models for templates and versions.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class Template(db.Model):
    """
    Template model representing an email template.
    
    Attributes:
        id: Primary key
        title: Title of the template
        versions: Relationship to template versions
        created_at: Timestamp of template creation
    """
    __tablename__ = 'templates'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    versions = db.relationship('TemplateVersion', backref='template', lazy=True, cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
        Convert template object to dictionary.
        
        Returns:
            dict: Template data including id, title, and creation timestamp
        """
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat()
        }

class TemplateVersion(db.Model):
    """
    TemplateVersion model representing a version of an email template.
    
    Attributes:
        id: Primary key
        template_id: Foreign key to parent template
        title: Title of the version
        content: The actual template content
        description: Description of changes in this version
        created_at: Timestamp of version creation
    """
    __tablename__ = 'versions'
    
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
        Convert version object to dictionary.
        
        Returns:
            dict: Version data including id, template_id, title, content,
                  description, and creation timestamp
        """
        return {
            'id': self.id,
            'template_id': self.template_id,
            'title': self.title,
            'content': self.content,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        } 