from app import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.is_admin = is_admin

    def __repr__(self):
        return f"{self.username}"

