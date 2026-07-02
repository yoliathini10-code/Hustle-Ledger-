import bcrypt
from database import get_connection, create_tables


def hash_password(password):
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt())


def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password
    )


def register_user(fullname, email, password, business_name):

    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE email=?",
        (email,)
    )

   