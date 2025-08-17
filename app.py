from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    technologies = db.Column(db.String(200), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{'id': p.id, 'title': p.title, 'description': p.description, 'image': p.image, 'technologies': p.technologies.split(',')} for p in projects])

@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify({'id': project.id, 'title': project.title, 'description': project.description, 'image': project.image, 'technologies': project.technologies.split(',')})

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(title=data['title'], description=data['description'], image=data['image'], technologies=','.join(data['technologies']))
    db.session.add(project)
    db.session.commit()
    return jsonify({'id': project.id, 'title': project.title, 'description': project.description, 'image': project.image, 'technologies': project.technologies.split(',')}), 201

@app.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    project.title = data['title']
    project.description = data['description']
    project.image = data['image']
    project.technologies = ','.join(data['technologies'])
    db.session.commit()
    return jsonify({'id': project.id, 'title': project.title, 'description': project.description, 'image': project.image, 'technologies': project.technologies.split(',')}), 200

@app.route('/api/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return '', 204

@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    message = Message(name=data['name'], email=data['email'], message=data['message'])
    db.session.add(message)
    db.session.commit()
    return jsonify({'id': message.id, 'name': message.name, 'email': message.email, 'message': message.message}), 201

@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{'id': m.id, 'name': m.name, 'email': m.email, 'message': m.