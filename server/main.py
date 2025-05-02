"""
Email Template Editor Server
This server provides API endpoints for managing email templates and their versions.
It handles template processing, storage, and retrieval.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import datetime
import sqlite3
import os

# Initialize Flask application
app = Flask(__name__)

# Configure CORS to allow frontend requests
CORS(app)

# Database initialization
def init_db():
    """Initialize the SQLite database and create necessary tables."""
    conn = sqlite3.connect('templates.db')
    c = conn.cursor()
    
    # Create templates table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create versions table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (template_id) REFERENCES templates (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Helper function to process template variables
def process_template(template, variables):
    """
    Process a template by replacing variables with their values.
    
    Args:
        template: The template string with variable placeholders
        variables: Dictionary of variables and their values
        
    Returns:
        tuple: (processed_template, list_of_errors)
    """
    errors = []
    result = template
    
    # Find all variable placeholders in the template
    placeholders = re.findall(r'\{([^}]+)\}', template)
    
    for placeholder in placeholders:
        try:
            # Split the placeholder into parts (e.g., 'user.firstName')
            parts = placeholder.split('.')
            value = variables
            
            # Navigate through the nested structure
            for part in parts:
                value = value[part]
                
            # Replace the placeholder with the value
            result = result.replace(f'{{{placeholder}}}', str(value))
        except (KeyError, TypeError):
            errors.append(f"Variable '{placeholder}' not found or invalid")
    
    return result, errors

# API Endpoints
@app.route('/api/templates', methods=['POST'])
def create_template():
    """
    Create a new template.
    
    Request Body:
        - template: The template content
        - title: The template title
        - description: Optional description
        
    Returns:
        JSON response with the created template data
        
    Raises:
        500 error if template creation fails
    """
    try:
        data = request.get_json()
        conn = sqlite3.connect('templates.db')
        c = conn.cursor()
        
        # Insert new template
        c.execute(
            "INSERT INTO templates (title, content) VALUES (?, ?)",
            (data['title'], data['template'])
        )
        template_id = c.lastrowid
        
        # Create initial version
        c.execute(
            "INSERT INTO versions (template_id, title, content, description) VALUES (?, ?, ?, ?)",
            (template_id, data['title'], data['template'], data.get('description', "Initial version"))
        )
        
        conn.commit()
        
        # Fetch and return the created template
        c.execute("SELECT * FROM templates WHERE id = ?", (template_id,))
        template = c.fetchone()
        
        conn.close()
        
        return jsonify({
            "id": template[0],
            "title": template[1],
            "content": template[2],
            "created_at": template[3]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/templates/<int:template_id>/versions', methods=['POST'])
def create_version(template_id):
    """
    Create a new version of an existing template.
    
    Args:
        template_id: ID of the template to version
        
    Request Body:
        - template: The new version content
        - title: The version title
        - description: Optional description
        
    Returns:
        JSON response with the created version data
        
    Raises:
        404 error if template not found
        500 error if version creation fails
    """
    try:
        data = request.get_json()
        conn = sqlite3.connect('templates.db')
        c = conn.cursor()
        
        # Verify template exists
        c.execute("SELECT id FROM templates WHERE id = ?", (template_id,))
        if not c.fetchone():
            return jsonify({"error": "Template not found"}), 404
        
        # Insert new version
        c.execute(
            "INSERT INTO versions (template_id, title, content, description) VALUES (?, ?, ?, ?)",
            (template_id, data['title'], data['template'], data.get('description'))
        )
        version_id = c.lastrowid
        
        conn.commit()
        
        # Fetch and return the created version
        c.execute("SELECT * FROM versions WHERE id = ?", (version_id,))
        version = c.fetchone()
        
        conn.close()
        
        return jsonify({
            "id": version[0],
            "template_id": version[1],
            "title": version[2],
            "content": version[3],
            "description": version[4],
            "created_at": version[5]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/templates/<int:template_id>/versions', methods=['GET'])
def get_versions(template_id):
    """
    Get all versions of a template.
    
    Args:
        template_id: ID of the template
        
    Returns:
        JSON response with list of versions
        
    Raises:
        404 error if template not found
        500 error if versions retrieval fails
    """
    try:
        conn = sqlite3.connect('templates.db')
        c = conn.cursor()
        
        # Verify template exists
        c.execute("SELECT id FROM templates WHERE id = ?", (template_id,))
        if not c.fetchone():
            return jsonify({"error": "Template not found"}), 404
        
        # Fetch all versions
        c.execute("SELECT * FROM versions WHERE template_id = ? ORDER BY created_at DESC", (template_id,))
        versions = c.fetchall()
        
        conn.close()
        
        return jsonify([{
            "id": v[0],
            "template_id": v[1],
            "title": v[2],
            "content": v[3],
            "description": v[4],
            "created_at": v[5]
        } for v in versions])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/templates/process', methods=['POST'])
def process_template_endpoint():
    """
    Process a template with variables.
    
    Request Body:
        - template: The template content
        - variables: Dictionary of variables and their values
        
    Returns:
        JSON response with processed template and any errors
        
    Raises:
        500 error if template processing fails
    """
    try:
        data = request.get_json()
        result, errors = process_template(data['template'], data['variables'])
        return jsonify({"result": result, "errors": errors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the server
if __name__ == "__main__":
    app.run(debug=True)