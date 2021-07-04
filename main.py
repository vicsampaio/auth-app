from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from auth_token import decode_token, encode_token

app = Flask(__name__, static_folder="static", static_url_path="")


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


db.create_all()


@app.post("/register")
def register():
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = data["password"]

    user = User(name=name, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return {
        "detail": "Successfully registered",
    }, 201


@app.post("/login")
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email, password=password).first()

    if not user:
        return {
            "error": "User not found",
        }, 404

    token = encode_token(user.id)

    return {"token": token}


@app.get("/user")
def get_user_info():
    bearer = request.headers.get("Authorization")

    if not bearer:
        return {
            "detail": "Authorization headers not provided",
        }, 401

    token = bearer.split(" ")[1]
    data = decode_token(token)

    user = User.query.filter_by(id=data["id"]).first()

    response = {
        "name": user.name,
        "email": user.email,
    }, 200

    return response


if __name__ == "__main__":
    app.run(debug=True)
