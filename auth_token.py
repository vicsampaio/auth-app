import jwt
import datetime as dt

SECRET_KEY = "senha_secreta_do_backend"


def encode_token(user_id: int):
    expiration_date = dt.datetime.utcnow() + dt.timedelta(days=1)

    token = jwt.encode(
        {
            "id": user_id,
            "exp": expiration_date,
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return token


def decode_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data
    except Exception as e:
        print(e)
        return None
