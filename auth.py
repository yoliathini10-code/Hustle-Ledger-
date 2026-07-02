import bcrypt
from database import get_connection, create_tables


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )


def verify_password(password, hashed_password):
    # SQLite may return bytes, bytearray or str

    if isinstance(hashed_password, bytearray):
        hashed_password = bytes(hashed_password)

    elif isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")

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

    if cursor.fetchone():
        conn.close()
        return False

    hashed = hash_password(password)

    cursor.execute("""
        INSERT INTO users
        (fullname, email, password, business_name)
        VALUES (?, ?, ?, ?)
    """, (
        fullname,
        email,
        hashed,
        business_name
    ))

    conn.commit()
    conn.close()

    return True


def login_user(email, password):

    create_tables()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, fullname, email, password, business_name
        FROM users
        WHERE email=?
    """, (email,))

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return None

    if verify_password(password, user[3]):
        return {
            "id": user[0],
            "fullname": user[1],
            "email": user[2],
            "business_name": user[4]
        }

    return None