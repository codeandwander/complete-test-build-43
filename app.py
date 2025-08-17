from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    technologies = db.Column(db.String(200), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'image': project.image,
        'technologies': project.technologies.split(',')
    } for project in projects])

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(
        title=data['title'],
        description=data['description'],
        image=data['image'],
        technologies=','.join(data['technologies'])
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'image': project.image,
        'technologies': project.technologies.split(',')
    })

@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    message = Message(
        name=data['name'],
        email=data['email'],
        message=data['message']
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({
        'id': message.id,
        'name': message.name,
        'email': message.email,
        'message': message.message
    })

@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([{
        'id': message.id,
        'name': message.name,
        'email': message.email,
        'message': message.message
    } for message in messages])

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

FILENAME: client/src/App.js