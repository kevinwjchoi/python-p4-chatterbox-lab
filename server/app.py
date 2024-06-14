

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        messages = []
        for message in Message.query.all():
            message_dict = {
                "id": message.id,
                "body": message.body,
                "username": message.username,
                "created_at": message.created_at,
                "updated_at": message.updated_at
            }
            messages.append(message_dict)

        response = make_response(
            messages,
            200
        )
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data['body'],
            username=data['username'],
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = {
        "id": new_message.id,
        "body": new_message.body,
        "username": new_message.username,
        "created_at": new_message.created_at,
        "updated_at": new_message.updated_at
    }

        response = make_response(
            message_dict,
            201
        )

        return response


@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'GET':
        message_dict = message.to_dict()

        response = make_response(
            message_dict,
            200
        )
        return response

    elif request.method == 'PATCH':
        data = request.get_json()
        for attr, value in data.items():
            setattr(message, attr, value)

        db.session.commit()

        message_dict = message.to_dict()

        response = make_response(
            message_dict,
            200
        )

        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.commit()

        message_dict=message.to_dict()

        response = make_response(
            message_dict,
            200
        )
        return response



if __name__ == '__main__':
    app.run(port=5555)
