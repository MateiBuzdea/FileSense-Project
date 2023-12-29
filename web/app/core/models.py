from datetime import datetime
from app import db

class Document(db.Model):

    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    owner = db.relationship("User", backref=db.backref("documents", lazy=True))

    def __init__(self, title, content, owner):
        self.title = title
        self.content = content
        self.created_on = datetime.now()
        self.owner = owner

    def __repr__(self):
        return f"{self.owner} - {self.title}"