from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import app, db
from core.models import Document
from forms import UploadForm

core_bp = Blueprint("core", __name__)


@login_required
@app.route("/search", methods=["GET", "POST"])
def search():
    pass


@login_required
@app.route("/document/<int:document_id>")
def view(document_id):
    document = Document.query.get_or_404(document_id)

    # check if the document belongs to user
    if document.owner != current_user:
        abort(403)

    return render_template("view.html", document=document)


@login_required
@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm(request.form)

    if form.validate_on_submit():
        document = Document(
            title=form.title.data,
            content=form.content.data,
            owner=current_user
        )
        db.session.add(document)
        db.session.commit()

        flash("Successfully uploaded document!", "success")
        return redirect(url_for("core.view", document_id=document.id))

    return render_template("upload.html", form=form)