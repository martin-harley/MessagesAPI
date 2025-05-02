from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Template, TemplateVersion
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///templates.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Drop and recreate all tables
with app.app_context():
    db.drop_all()
    db.create_all()

def find_variables(template):
    """Find all of the variables in the template that match the pattern"""
    return re.findall(r'/([a-zA-Z0-9.-][a-zA-Z0-9.-]*[a-zA-Z0-9])', template)

def resolve_variable_path(data, path):
    """Resolve nested variable paths in the data structure"""
    parts = path.split('.')
    current = data
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current

def process_templates(template, variables):
    """Process templates by replacing variables with values"""
    result = template
    errors = []

    for var in find_variables(template):
        value = resolve_variable_path(variables, var)
        if value is None:
            errors.append(f"Variable '/{var}' is not found in the data provided. Please try again.")
            continue
        result = result.replace(f'/{var}', str(value))
    
    return result, errors


@app.route('/api/templates', methods=['POST'])
def create_template():
    data = request.get_json()
    template_text = data.get('template')
    title = data.get('title', 'Untitled Template')
    description = data.get('description', 'Initial version')

    if not template_text:
        return jsonify({'error': 'Template text is required; please fill in the text box.'}), 400

    template = Template(title=title)
    db.session.add(template)
    db.session.commit()

    version = TemplateVersion(
        template_id=template.id,
        content=template_text,
        description=description,
        title=title
    )
    db.session.add(version)
    db.session.commit()

    return jsonify({
        'id' : template.id,
        'version_id' : version.id,
        'content' : template_text,
        'created_at' : version.created_at.isoformat()
    }), 201


@app.route('/api/templates/<int:template_id>/versions', methods=['POST'])
def create_version(template_id):
    data = request.get_json()
    template_text = data.get('template')
    title = data.get('title', 'Untitled Version')
    description = data.get('description', 'New Version')

    if not template_text:
        return jsonify({'error': 'Template text is required; please fill in the field.'}), 400
    
    template = Template.query.get_or_404(template_id)

    version = TemplateVersion(
        template_id=template.id,
        content=template_text,
        title=title,
        description=description
    )
    db.session.add(version)
    db.session.commit()

    return jsonify({
        'id': version.id,
        'content': template_text,
        'title': title,
        'description': description,
        'created_at': version.created_at.isoformat()
    }), 201


@app.route('/api/templates/<int:template_id>/versions', methods=['GET'])
def get_versions(template_id):
    Template.query.get_or_404(template_id)
    versions = TemplateVersion.query.filter_by(template_id=template_id).order_by(TemplateVersion.created_at.desc()).all()

    return jsonify([{
        'id': v.id,
        'content': v.content,
        'title': v.title,
        'description': v.description,
        'created_at': v.created_at.isoformat()
    } for v in versions])

@app.route('/api/templates/process', methods=['POST'])
def process_template_endpoint():
    data = request.get_json()
    template = data.get('template')
    variables = data.get('variables', {})

    if not template:
        return jsonify({'error': 'Template is required'}), 400

    result, errors = process_templates(template, variables)

    return jsonify({
        'result': result,
        'errors': errors
    })

@app.route('/api/templates/<int:template_id>/revert/<int:version_id>', methods=['POST'])
def revert_to_version(template_id, version_id):
    Template.query.get_or_404(template_id)
    old_version = TemplateVersion.query.get_or_404(version_id)

    if old_version.template_id != template_id:
        return jsonify({'error': 'This version does not belong to this template.'}), 400

    new_version = TemplateVersion(
        template_id=template_id,
        content=old_version.content,
        description=f'Reverted to version from {old_version.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    )
    db.session.add(new_version)
    db.session.commit()

    return jsonify({
        'id': new_version.id,
        'content': new_version.content,
        'description': new_version.description,
        'created_at': new_version.created_at.isoformat()
    })