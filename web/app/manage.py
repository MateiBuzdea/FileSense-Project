from flask.cli import FlaskGroup

from app import app, db
from app.accounts.models import User
from app.core.models import Document
from app.ai_utils import add_document

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(User(username="admin", password="admin", is_admin=True))
    db.session.add(User(username="john", password="p@ssword"))

    document = Document(
        title="First Document",
        content="This is my first document. It's not very long, but it's good.",
        owner=User.query.filter_by(username="john").first()
    )

    db.session.add(document)
    db.session.commit()

    # Add document to txtai
    add_document(document)


@cli.command("init_db")
def init_db():
    create_db()
    seed_db()


if __name__ == "__main__":
    cli()
