from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def serialize(self):
        return {"id": self.id, "name": self.name, "email": self.email}

@app.before_request
def create_tables():
    db.create_all()

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize())


@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400, description="Missing required fields: name and email")
    user = User(name=request.json['name'], email=request.json['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize()), 201


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if not request.json:
        abort(400, description="Missing JSON in request")
    user.name = request.json.get('name', user.name)
    user.email = request.json.get('email', user.email)
    db.session.commit()
    return jsonify(user.serialize())


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

